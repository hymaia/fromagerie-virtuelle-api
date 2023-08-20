import json
from json import JSONDecodeError

import boto3
import os
import logging

logging.basicConfig()

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')

BUCKET_NAME = os.environ["PLAYERS_ANSWERS_BUCKET_NAME"]


def lambda_handler(event, context):

    try:
        body = json.loads(event["body"])
        user = event['requestContext']['authorizer']['claims']['username']

        month = body['month']

        cheeses = [
            "roquefort",
            "raclette",
            "camembert",
            "emmental",
            "brie",
            "parmesan",
            "comté",
            "mimolette",
            "gouda",
            "fourme de Montbrison"
        ]

        parsed_cheese = {}
        output = ""
        for cheese in cheeses:
            parsed_cheese[cheese] = body["predictions"][cheese]
            parsed_cheese[cheese]["cheese"] = cheese
            output = f"""{json.dumps(parsed_cheese[cheese], ensure_ascii=False)}
{output}"""

        s3.put_object(Bucket=BUCKET_NAME,
                      Key=f"data/answers/player={user}/month={month}/data.json",
                      Body=output)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Bien reçu !",
                "data": body,
            }),
        }
    except KeyError as e:
        logging.error(e)
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": f"Un fromage manque à l'appel : {e}",
            }),
        }
    except JSONDecodeError as e:
        logging.error(e)
        return {
            'statusCode': 400,
            'body': f'Le json est mal formaté : {str(e)}'
        }
    except Exception as e:
        logging.error(e)
        return {
            'statusCode': 500,
            'body': f'Erreur interne du serveur : {str(e)}'
        }
