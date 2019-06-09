import final_script
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
import pytest

@pytest.mark.asyncio
async def test_clean_data():
    list_for_input = [['www.google.com', "hi"], ['', "hi"], ['www.b.com']]
    list_for_output = [['www.google.com', "hi"], ['www.b.com']]
    input_df = pd.DataFrame(list_for_input, columns = ['websites', 'regex'])
    df = pd.DataFrame(list_for_output, columns = ['websites', 'regex'])
    res = await final_script.clean_data(input_df)
    res.reset_index()
    assert type(res) == pd.DataFrame
    res = res.reset_index(drop=True)
    df = df.reset_index(drop=True)
    assert res.values.tolist()== df.values.tolist()




@pytest.mark.asyncio
async def test_compare_url_regex():
    SRE_MATCH_TYPE = type(re.match("", ""))
    response = "I am here"
    regex = "am"
    res = await final_script.compare_url_regex(response, regex)
    assert type(res) == SRE_MATCH_TYPE


