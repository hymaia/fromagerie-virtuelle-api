import json
import boto3
import os
import logging

logging.basicConfig()

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')

TABLE_NAME = os.environ["GAME_TABLE_NAME"]
BUCKET_NAME = os.environ["PLAYERS_ANSWERS_BUCKET_NAME"]


def lambda_handler(event, context):
    body = json.loads(event["body"])
    user_id = event['requestContext']['authorizer']['claims']['sub']

    try:
        data = body["data"]
    except KeyError as e:
        logging.error(e)
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": f"data is missing from body : {event['body']}",
            }),
        }

    s3.put_object(Bucket=BUCKET_NAME,
                  Key=f"answers/player={user_id}/data.json",
                  Body=data,)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Bien reçu !",
            "data": data,
        }),
    }
