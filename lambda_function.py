import boto3
import os
from botocore.exceptions import ClientError
from datetime import datetime
from urllib.request import urlopen

SITES = []

for url in os.environ['SITES'].split(','):
    SITES.append(url.strip())

TOPIC = os.environ['TOPIC']
REGION = os.environ['AWS_REGION']

client = boto3.client('sns', region_name=REGION)


def fail(site, msg):

    # Publish event to SNS
    try:
        print("Publishing to SNS")
        client.publish(
            TopicArn=TOPIC,
            Message='{} failed.\n\nReason: {}'.format(site, msg)
        )
    except ClientError as e:
        print('Exception when publishing to SNS')
        print(e)


def validate(site):

    try:
        res = urlopen(site)
    except Exception as e:
        print('Check failed!')
        fail(site, e)
    else:

        code = res.getcode()

        if code != 200:
            fail(site, 'Got status code {} instead of 200'.format(code))

        content = res.read().decode()

        if 'Error establishing a database connection' in content:
            fail(site, 'Got content: Error establishing a database connection')


def lambda_handler(event, context):

    for site in SITES:
        now = str(datetime.now())
        print('Checking {} at {}...'.format(site, now))
        validate(site)

    print('Check complete at {}'.format(str(datetime.now())))


if __name__ == "__main__":
    lambda_handler(None, None)
