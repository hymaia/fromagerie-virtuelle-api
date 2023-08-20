import json
import boto3
import os
import logging
from boto3.dynamodb.types import TypeDeserializer

logging.basicConfig()

dynamodb = boto3.client('dynamodb')

TABLE_NAME = os.environ["GAME_TABLE_NAME"]

deserializer = TypeDeserializer()

def mapLeaderboard(score):
    del score["PK"]
    del score["SK"]
    del score["GSI1PK"]
    del score["GSI1SK"]
    del score["month"]
    score["rank"] = int(score["rank"])
    score["score"] = int(score["score"])

def lambda_handler(event, context):
    user_id = event['requestContext']['authorizer']['claims']['username']
    top = get_top_score()
    player_score = get_player_score(user_id)

    if "PK" in player_score:
        mapLeaderboard(player_score)

    for item in top:
        mapLeaderboard(item)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Voici le top 10 des joueurs ainsi que votre position par rapport à eux",
            "top": top,
            "player_score": player_score,
        }),
    }


def get_player_score(player_id):
    res = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            'PK': {"S": f"PLAYER#{player_id}"},
            'SK': {"S": "1"},
        }
    )
    if "Item" in res:
        item = res["Item"]
        deserialized_response = deserialize_dynamo_object(item)
        return deserialized_response
    else:
        return {}


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
