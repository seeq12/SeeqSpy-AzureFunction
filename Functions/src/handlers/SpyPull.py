import logging
from seeq import spy
import pandas as pd
import azure.functions as func
import sys
import traceback
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Recieved request')
    resp = ''
    grid_param = '15m'
    try:
        req_body = req.get_json()
    except ValueError as e:
        return func.HttpResponse(body = json.dumps("error: Error parsing body: " + str(e) + "}"), status_code=400)
    search_params = req_body.get('search-params')
    grid_param = req_body.get('grid')
    access_key = req_body.get('key')
    pass_key = req_body.get('secret')
    start_time = req_body.get('start')
    end_time = req_body.get('end')
    try:
        logging.info('Logging into Seeq')
        spy.login(url="<your_server>", access_key=access_key, password=pass_key, ignore_ssl_errors=True)
    except RuntimeError as e:
        return func.HttpResponse(body = json.dumps("error: Error Logging into Seeq: " + str(e) + "}"), status_code=400)
    logging.info('Logged in. Starting search.')

    items = None
    try:
        items = spy.search(search_params)
    except RuntimeError as e:
        return func.HttpResponse(body = json.dumps("error: Could not execute SPy Search: " + str(e) + "}"), status_code=400)
    logging.info('recieved search response: ' + str(items.count))
    logging.info('Starting pull.')
    try:
        data = spy.pull(items, end=end_time, start=start_time, grid=grid_param)
    except RuntimeError as e:
        return func.HttpResponse(body = json.dumps("error: Could not execute SPy Pull: " + str(e) + "}"), status_code=400)  
    logging.info('recieved pull response. serializing pull results dataframe')
    resp = data.to_json()
    logging.info('finished serializing dataframe. Returning now.')
    return func.HttpResponse(resp)