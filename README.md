# async_web_scraper
This is a webscaper that takes in a csv file of websites and regular expressions.

The Scrapper will request all the webpages from the csv and then store time of check, response code, response time and whether regex was a match or not to mongodb.

CSV file has to have two columns one named websites and one named regex

Example csv shows how csv is supposed to be formated.


# Installation:

Script needs python version 3.6 or 3.7 to work

Script also needs:

pip install aiohttp

pip install pandas

pip install pymongo


# Running the script

Script takes in the name of csv as the second argument so the whole command is

python final_script.py example.csv

It also needs mongodb running on the computer. Here is a guide how to set that up: https://medium.com/@saivittalb/introduction-to-mongodb-859ed4426994 only installation part is required.
