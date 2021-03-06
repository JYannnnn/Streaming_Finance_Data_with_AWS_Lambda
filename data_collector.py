import json
import boto3
import os
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "--target", "/tmp", 'yfinance'])
sys.path.append('/tmp')
import yfinance as yf

tickers = ['FB', 'SHOP', 'BYND', 'NFLX', 'PINS', 'SQ', 'TTD', 'OKTA', 'SNAP', 'DDOG']
def lambda_handler(event, context):
    fh = boto3.client("firehose", "us-east-2")
    for ticker in tickers:
        data = yf.download(ticker, start="2020-05-14", end="2020-05-15", interval = "1m")
        for datetime, row in data.iterrows():
            output = {'name': ticker}
            output['high'] = row['High']
            output['low'] = row['Low']
            output['ts'] = str(datetime)
            as_jsonstr = json.dumps(output)
            fh.put_record(
                DeliveryStreamName="finance-delivery-stream", 
                Record={"Data": as_jsonstr.encode('utf-8')})
    return {
        'statusCode': 200,
        'body': json.dumps(f'Done! Recorded: {as_jsonstr}')
    }