import boto3
import os
import json
from botocore.exceptions import ClientError

userpool_id = os.environ['USER_POOL_ID']
client_id = os.environ['USER_POOL_CLIENT_ID']

# Créer le client Cognito
client = boto3.client('cognito-idp')


def lambda_handler_signup(event, context):
    try:
        # Récupérer les informations de l'utilisateur depuis l'événement
        body = json.loads(event["body"])
        username = body['username']
        email = body['email']
        password = body['password']

        # Créer un nouvel utilisateur dans Cognito
        client.sign_up(
            ClientId=client_id,
            Username=username,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                {
                    'Name': 'name',
                    'Value': username
                },
            ]
        )

        return {
            'statusCode': 200,
            'body': 'Ajout de l\'e-mail réussie. Un code de confirmation vous y a été envoyé.'
        }
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return {
            'statusCode': 400,
            'body': f"Erreur lors de l'inscription de l'e-mail : {error_message}"
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': f"Champs manquant : {e}"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Erreur interne du serveur : {str(e)}'
        }


def lambda_handler_confirm(event, context):
    try:
        # Récupérer les informations de l'utilisateur depuis l'événement
        body = json.loads(event["body"])
        username = body['username']
        verification_code = body['verification_code']

        # Vérifier le code de vérification de l'e-mail
        response = client.confirm_sign_up(
            ClientId=client_id,
            Username=username,
            ConfirmationCode=verification_code
        )

        return {
            'statusCode': 200,
            'body': 'Vérification de l\'e-mail réussie'
        }
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return {
            'statusCode': 400,
            'body': f'Erreur lors de la vérification de l\'e-mail : {error_message}'
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': f"Champs manquant : {e}"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Internal error server : {str(e)}'
        }


def lambda_handler_refresh(event, context):
    try:
        # Récupérer les informations de l'utilisateur depuis l'événement
        body = json.loads(event["body"])
        refresh_token = body['refresh_token']

        # Vérifier le code de vérification de l'e-mail
        response = client.initiate_auth(
            AuthFlow='REFRESH_TOKEN_AUTH',
            ClientId=client_id,
            AuthParameters={
                'REFRESH_TOKEN': refresh_token
            }
        )

        # Récupérer le jeton d'accès et autres informations d'authentification
        access_token = response['AuthenticationResult']['AccessToken']
        expires_in = response['AuthenticationResult']['ExpiresIn']

        # Faites quelque chose avec les tokens d'authentification (par exemple, renvoyez-les dans la réponse)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'accessToken': access_token,
                'expiresIn': expires_in,
            })
        }
    except client.exceptions.NotAuthorizedException as e:
        return {
            'statusCode': 401,
            'body': 'Unauthorized'
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': f"Champs manquant : {e}"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Internal error server : {str(e)}'
        }
