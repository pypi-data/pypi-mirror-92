import os
import json
import logging
import hmac
import hashlib
import base64
import json

import boto3
import requests
from dotenv import load_dotenv

load_dotenv()


def get_secret_hash(username, client_id, client_secret):
    msg = username + client_id
    dig = hmac.new(str(client_secret).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def initiate_auth(client, username, password, pool_id, client_id, client_secret):
    secret_hash = get_secret_hash(username, client_id, client_secret)

    res = client.admin_initiate_auth(
        UserPoolId=pool_id,
        ClientId=client_id,
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            'USERNAME': username,
            'SECRET_HASH': secret_hash,
            'PASSWORD': password,
        },
        ClientMetadata={
            'username': username,
            'password': password,
        })

    return res


def login():
    USER_POOL_ID = os.environ["USER_POOL_ID"]
    CLIENT_ID = os.environ["CLIENT_ID"]
    CLIENT_SECRET = os.environ["CLIENT_SECRET"]
    COGNITO_PASSWORD = os.environ["COGNITO_PASSWORD"]
    COGNITO_USERNAME = os.environ["COGNITO_USERNAME"]
    AWS_REGION = os.environ["AWS_REGION"]
    ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    SECRET_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

    client = boto3.client('cognito-idp', region_name=AWS_REGION,
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)

    auth = initiate_auth(client, COGNITO_USERNAME,
                         COGNITO_PASSWORD, USER_POOL_ID, CLIENT_ID, CLIENT_SECRET)
    return auth


class Loader:
    def __init__(self, ticker, datatype):
        base_url = os.environ["API_BASE_URL"]
        url = f"{base_url}/{datatype}/{ticker}"
        self.url = url

        self.idToken = login()["AuthenticationResult"]["IdToken"]

    def load(self, data):
        headers = {
            "Authorization": f"Bearer {self.idToken}"
        }

        try:
            response = requests.post(self.url, data=data, headers=headers)

            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            logging.error(str(e) + " ––– " + response.text)
            raise

        return response.json()
