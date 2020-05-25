## Streaming Finance Data with AWS Lambda

#### Goal: 
- Go through the process of consuming “real time” data, processing the data and then dumping it in a manner that facilitates querying and further analysis, either in real time or near real time capacity.

#### Infrastructure:
This project consists of three major infrastructure elements that work in tandem:
- A lambda function that collects our data (DataCollector)
- A lambda function that transforms and places data into S3 (DataTransformer)
- A serverless process that allows us to query our s3 data (DataAnalyzer)

#### Process:
- Step 1: Create a Kinesis Firehose Delivery Stream which should have a lambda function that transforms your record and streams it into an S3 bucket. (DataTransformer)
- Step 2: Write another Lambda function that is triggered from a simple URL call. On trigger, it will grab stock price data and place it into the delivery defined in the DataTransformer. (DataCollector)
- Step 3: Configure AWS Glue, pointing it to the S3 Bucket created in DataTransformer. This will allow us to now interactively query the S3 files generated by the DataTransformer using AWS Athena to gain insight into our streamed data. (DataAnalyzer)

#### Lambda Function URL (DataCollector):
- https://0b461p8c6d.execute-api.us-east-2.amazonaws.com/default/data-collector

#### Data Collector AWS Lambda Configuration Page:
<img width="1541" alt="Screen Shot 2020-05-25 at 1 02 46 PM" src="https://user-images.githubusercontent.com/60801548/82832080-231c0080-9e88-11ea-9fe0-f2d33c4c12d7.png">

#### Kinesis Data Firehose Delivery Stream Monitoring:
<img width="1762" alt="Screen Shot 2020-05-25 at 1 13 54 PM" src="https://user-images.githubusercontent.com/60801548/82832631-a5f18b00-9e89-11ea-9a98-523fb4320c87.png">

#### S3 Files:
<img width="1775" alt="Screen Shot 2020-05-25 at 1 15 18 PM" src="https://user-images.githubusercontent.com/60801548/82832694-d33e3900-9e89-11ea-86bb-2fd024e323a1.png">




