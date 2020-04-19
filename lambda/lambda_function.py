import os
import boto3
import json

import subscription_data

client = boto3.client('sns')
church_newsletter_topic = 'arn:aws:sns:us-west-2:325011596675:church-newsletter'
API_KEY = 'b132492f-d929-4a1e-bfc5-939a83da8a60'

# https://medium.com/perfektio/google-sheets-aws-lambda-json-backend-d5e67ab4f660

def lambda_handler(event, context):
    print('## EVENT')
    # print(event)

    cells = subscription_data.get_subscription_cells()

    params = event.get('queryStringParameters')
    api_key = params and params.get('api_key')
    message = params and params.get('message')

    if api_key is None or api_key != API_KEY:
        print('Invalid API Key')
        return {
           "statusCode": 404,
            "body": json.dumps({'status': 'Invalid API Key'})
        }

    if message is None:
        return {
           "statusCode": 401,
            "body": json.dumps({'status': 'No message is found'})
        }



    # update subscriptions
    for cell in cells.values():

        # if cell.get('Email Address'):
        #     client.subscribe(
        #         TopicArn=church_newsletter_topic,
        #         Protocol='email',
        #         Endpoint=cell['Email Address']
        #     )

        # sms only for now
        if cell.get('Phone Number'):
            client.subscribe(
               TopicArn=church_newsletter_topic,
                Protocol='sms',
                Endpoint=cell['Phone Number']
            )


    # publish
    client.publish(
        TopicArn=church_newsletter_topic,
        Message=message,
        Subject='Church in Burlingame Notification'
    )

    # we need to include statusCode and a body with serialized json
    return {
        "statusCode": 200,
        "body": json.dumps({'message': message})
    }
