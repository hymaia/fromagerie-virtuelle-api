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
    player_secret_key = body["secret_key"]
    data = json.loads(body["data"])

    if not is_user_exist(player_secret_key):
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "Secret key not found (à prononcer avec l'accent français) !"
            }),
        }

    s3.put_object(Bucket=BUCKET_NAME,
                  Key="answers",
                  Body=json.dumps(data),)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Bien reçu !",
            "data": json.dumps(data),
        }),
    }


def is_user_exist(secret_key):
    items = dynamodb.query(
        TableName=TABLE_NAME,
        IndexName='GSI1',
        ExpressionAttributeValues={
            ':pk': {"S": f"UUID#{secret_key}"},
            ':sk': {"S": '1'},
        },
        KeyConditionExpression='(GSI1PK = :pk) AND (GSI1SK = :sk)',
    )
    return 'Items' in items
