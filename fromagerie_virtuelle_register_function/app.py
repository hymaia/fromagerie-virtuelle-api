import json
import boto3
import os
import logging
import uuid

logging.basicConfig()

dynamodb = boto3.client('dynamodb')

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
            "secret_key": player_secret_key,
            "instructions": "Récupérez votre secret_key et gardez la précieusement sans la divulguer.",
        }),
    }


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
            'mail': {"S": mail},
            'user': {"S": pseudo},
        }
    )
    return response

