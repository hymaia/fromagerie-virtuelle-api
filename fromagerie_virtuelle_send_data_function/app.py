import json
import boto3
import os
import logging

logging.basicConfig()

dynamodb = boto3.client('dynamodb')

TABLE_NAME = os.environ["GAME_TABLE_NAME"]

def lambda_handler(event, context):
    body = json.loads(event["body"])
    player_secret_key = body["secret_key"]
    data = body["data"]

    if not is_user_exist(player_secret_key):
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "Secret key not found (à prononcer avec l'accent français) !"
            }),
        }

    for elem in json.loads(data):
        print(elem)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Bien reçu !",
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
    print(items)
    return 'Items' in items


