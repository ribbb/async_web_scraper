import asyncio
import sys
import re
import time
import pandas as pd
import signal
import functools
from pymongo import MongoClient
from concurrent.futures import CancelledError
import aiohttp
import datetime
import numpy as np
from concurrent.futures import CancelledError


async def send_data(data):
    #Data = List of values [Regex_match, response_time, response_code]
    client = MongoClient()
    db=client.urls_test
    urls = db.urls
    t = time.time()
    for d in data:
        if type(d) is list:
        	#Sometimes data might contain None elements because of server side connection errors.
            connection_data = {
                "response_time_in_seconds" : d[1],
                "regex_found" : str(d[0]),
                "response_code": str(d[2]),
                "time_of_check": d[3]
            }
        else:
            connection_data = {
            "Unknown_data" : d
            }

        result = urls.insert_one(connection_data)


async def clean_data(data):
    data['websites'].replace('', np.nan, inplace=True)
    data = data.dropna(subset=['websites'])
    return data

async def gather(websites,session):
    tasks = asyncio.gather(*[handle(get_website(url, session)) for url in websites], return_exceptions=True)
    return tasks

async def fetch(session, url):
    async with session.get(url) as response:
        print(url)
        return await response.text(), response.status

async def get_website(url, session):
    result = []
    t = time.time()
    html, status = await fetch(session, url[0])
    t = time.time() - t

        #Empty regex is float.
    if type(url[1]) == str:
        result.append(await compare_url_regex(html, url[1]))
    else:
        result.append("")
    result.append(t)
    result.append(status)
    result.append(datetime.datetime.today())
    return result

async def compare_url_regex(response, regex):
    #print(regex)
    #print(type(regex))
    return re.search(regex, response)


async def handle(task):
    try:
        await task
    except:
        print("Error handling hit")
        raise

async def main(batch, LOOP):
    conn = aiohttp.TCPConnector(limit=30)
    async with aiohttp.ClientSession(connector=conn) as session:
        batch = await clean_data(batch)
        websites = batch.values.tolist()
        tasks = await gather(websites, session)
        result = await tasks
        #print(time.time()-t)
        await send_data(result)


'''
Program flow is: Loop through the csv --> Clean data from csv --> Asyncronously call websites -
-> Check regex against response body --> Save statistics to database.
''' 
if __name__ == '__main__':
    try:
        LOOP = asyncio.get_event_loop()
        CSV_NAME = sys.argv[1]
        #asyncio.ensure_future(main("./input.csv", LOOP))
        while True:
            print("Starting url check")
            for batch in pd.read_csv(CSV_NAME, chunksize=6):
                LOOP.run_until_complete(handle(main(batch, LOOP)))
            print("Going to sleep")
            time.sleep(15)
            print("I am here")
    except KeyboardInterrupt:
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        print("Canceled tasks")
    except CancelledError:
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        print("Canceled tasks")
    finally:
        complete_please = asyncio.gather(*asyncio.Task.all_tasks())
        print("Waiting for tasks to complete")
        asyncio.wait(complete_please)
        print("Closing the loop")
        LOOP.close()
        sys.exit(1)
