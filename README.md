## Streaming Finance Data with AWS Lambda

### Goal: 
- Go through the process of consuming “real time” data, processing the data and then dumping it in a manner that facilitates querying and further analysis, either in real time or near real time capacity.

### Infrastructure:
This project consists of three major infrastructure elements that work in tandem:
- A lambda function that collects our data (DataCollector)
- A lambda function that transforms and places data into S3 (DataTransformer)
- A serverless process that allows us to query our s3 data (DataAnalyzer)

### Step 1: Data Transformer
- Create a Kinesis Firehose Delivery Stream which should have a lambda function that transforms the record and streams it into an S3 bucket. 
- Outcome: finance_data folder

#### Lambda Source Code:
```py
import json

def lambda_handler(event, context):
    output_records = []
    for record in event["records"]:
        output_records.append({
            "recordId": record['recordId'],
            "result": "Ok",
            "data": record["data"] + "Cg==" # this is the key here
        })
        
    return { "records": output_records }
```
#### Kinesis Data Firehose Delivery Stream Monitoring:
<img width="1762" alt="Screen Shot 2020-05-25 at 1 13 54 PM" src="https://user-images.githubusercontent.com/60801548/82832631-a5f18b00-9e89-11ea-9a98-523fb4320c87.png">

#### S3 Files:
<img width="1775" alt="Screen Shot 2020-05-25 at 1 15 18 PM" src="https://user-images.githubusercontent.com/60801548/82832694-d33e3900-9e89-11ea-86bb-2fd024e323a1.png">


### Step 2: Data Collector
- Write another Lambda function that is triggered from a simple URL call. On trigger, it will grab stock price data and place it into the delivery defined in the DataTransformer. 
- Use the yfinance module to grab pricing information for each of the following stocks:'FB', 'SHOP', 'BYND', 'NFLX', 'PINS', 'SQ', 'TTD', 'OKTA', 'SNAP', 'DDOG'. Collect one full day’s worth of stock HIGH and LOW prices for each company listed above on Thursday, May 14th 2020, at an one minute interval. Note that by “full day” we mean one day of stock trading, which is not 24 hours.


#### Lambda Source Code:
```py
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
```
#### AWS Lambda Function URL:
- https://0b461p8c6d.execute-api.us-east-2.amazonaws.com/default/data-collector

#### AWS Lambda Configuration Page:
<img width="1541" alt="Screen Shot 2020-05-25 at 1 02 46 PM" src="https://user-images.githubusercontent.com/60801548/82832080-231c0080-9e88-11ea-9fe0-f2d33c4c12d7.png">


### Step 3: Data Analyzer
- Configure AWS Glue, pointing it to the S3 Bucket created in DataTransformer. This will allow us to now interactively query the S3 files generated by the DataTransformer using AWS Athena to gain insight into our streamed data. 
- Outcome: results.csv file

#### SQL Query:
```sql
SELECT * 
FROM 
(SELECT T1.Company, T2.High_Stock_Price, T1.DateTime, T1.Hour
 FROM 
 (SELECT name AS Company, high, ts AS DateTime, SUBSTRING(ts, 12, 2) AS Hour FROM finance_stream_data) T1
INNER JOIN 
 (SELECT name, SUBSTRING(ts, 12, 2) AS hour, MAX(high) AS High_Stock_Price 
  FROM finance_stream_data
  GROUP BY name, SUBSTRING(ts, 12, 2)) T2
ON T1.Company = T2.name AND T1.high = T2.High_Stock_Price AND T1.Hour = T2.hour)
ORDER BY Company, Hour, DateTime
```








