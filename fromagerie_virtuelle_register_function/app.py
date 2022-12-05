import json
import boto3
import os
import logging
import uuid
from cachetools import TTLCache, cached

logging.basicConfig()

dynamodb = boto3.client('dynamodb')
secret_client = boto3.client('secretsmanager')

TABLE_NAME = os.environ["GAME_TABLE_NAME"]

def lambda_handler(event, context):
    body = json.loads(event["body"])
    pseudo = body["pseudo"]
    mail = body["mail"]
    player_secret_key = str(uuid.uuid4())

    if is_user_exist(pseudo):
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Player already registered"
            }),
        }

    store_user_in_dynamo_db(pseudo, mail, player_secret_key)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "mail": mail,
            "pseudo": pseudo,
            "secret_key": player_secret_key
        }),
    }


def get_dynamo_map_content(items):
    res = {}
    for key, value in items["M"].items():
        res[key] = value["S"]
    return res


def is_user_exist(pseudo):
    return 'Item' in dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            'PK': {"S": f"USER#{pseudo}"},
            'SK': {"S": f"1"},
        }
    )


def store_user_in_dynamo_db(pseudo, mail, player_secret_key):
    response = dynamodb.put_item(
        TableName=TABLE_NAME,
        Item={
            'PK': {"S": f"USER#{pseudo}"},
            'SK': {"S": f"1"},
            'GSI1PK': {"S": f"UUID#{player_secret_key}"},
            'GSI1SK': {"S": f"1"},
            'uuid': {"S": player_secret_key},
            'mail': {"S": mail}
        }
    )
    return response

