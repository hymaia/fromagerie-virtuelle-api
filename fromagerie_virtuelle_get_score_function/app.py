import json
import boto3
import os
import logging
from boto3.dynamodb.types import TypeDeserializer

logging.basicConfig()

dynamodb = boto3.client('dynamodb')

TABLE_NAME = os.environ["GAME_TABLE_NAME"]

deserializer = TypeDeserializer()


def lambda_handler(event, context):
    user_id = event['requestContext']['authorizer']['claims']['username']
    top = get_top_score()
    player_score = get_player_score(user_id)

    del player_score["PK"]
    del player_score["SK"]
    del player_score["GSI1PK"]
    del player_score["GSI1SK"]
    del player_score["month"]
    player_score["rank"] = int(player_score["rank"])
    player_score["score"] = int(player_score["score"])

    for item in top:
        del item["PK"]
        del item["SK"]
        del item["GSI1PK"]
        del item["GSI1SK"]
        del item["month"]
        item["rank"] = int(item["rank"])
        item["score"] = int(item["score"])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Voici le top 10 des joueurs ainsi que votre position par rapport à eux",
            "top": top,
            "player_score": player_score,
        }),
    }


def get_player_score(player_id):
    item = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            'PK': {"S": f"PLAYER#{player_id}"},
            'SK': {"S": "1"},
        }
    )["Item"]
    deserialized_response = deserialize_dynamo_object(item)
    return deserialized_response


def deserialize_dynamo_object(item):
    return {k: deserializer.deserialize(v) for k, v in item.items()}


def get_top_score():
    items = dynamodb.query(
        TableName=TABLE_NAME,
        IndexName='GSI1',
        ExpressionAttributeValues={
            ':pk': {"S": "TOP"},
        },
        KeyConditionExpression='(GSI1PK = :pk)',
    )["Items"]

    deserialized_response = []
    for item in items:
        deserialized_response.append(deserialize_dynamo_object(item))
    return deserialized_response
