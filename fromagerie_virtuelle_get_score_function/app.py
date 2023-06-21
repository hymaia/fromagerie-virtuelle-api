import json
import boto3
import os
import logging

logging.basicConfig()

dynamodb = boto3.client('dynamodb')

TABLE_NAME = os.environ["GAME_TABLE_NAME"]


def lambda_handler(event, context):
    user_id = event['requestContext']['authorizer']['claims']['sub']
    top = get_top_score()
    player_score = get_player_score(user_id)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Voici le top 10 des joueurs ainsi que votre position par rapport à eux",
            "top": top,
            "player_score": player_score,
        }),
    }


def get_player_score(player_id):
    return dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            'PK': {"S": f"PLAYER#{player_id}"},
            'SK': {"S": "1"},
        }
    )


def get_top_score():
    items = dynamodb.query(
        TableName=TABLE_NAME,
        IndexName='GSI1',
        ExpressionAttributeValues={
            ':pk': {"S": "TOP"},
        },
        KeyConditionExpression='(GSI1PK = :pk)',
    )
    return items
