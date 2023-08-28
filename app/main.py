import base64
import hashlib
import hmac
import json
import time
import uuid

import botocore
import botocore.session
import requests
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig


def get_token_and_secret():
  # ref. https://github.com/aws/aws-secretsmanager-caching-python

  client = botocore.session.get_session().create_client('secretsmanager')
  cache_config = SecretCacheConfig()
  cache = SecretCache( config = cache_config, client = client)

  secretString = cache.get_secret_string('switchbot')
  token = json.loads(secretString)['token']
  secret = json.loads(secretString)['secret']

  return token, secret


def get_headers():
  # ref. https://github.com/OpenWonderLabs/SwitchBotAPI

  apiHeader = {}
  
  token, secret = get_token_and_secret()

  nonce = uuid.uuid4()
  t = int(round(time.time() * 1000))
  string_to_sign = '{}{}{}'.format(token, t, nonce)

  string_to_sign = bytes(string_to_sign, 'utf-8')
  secret = bytes(secret, 'utf-8')

  sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

  apiHeader['Authorization']=token
  apiHeader['Content-Type']='application/json'
  apiHeader['charset']='utf8'
  apiHeader['t']=str(t)
  apiHeader['sign']=str(sign, 'utf-8')
  apiHeader['nonce']=str(nonce)

  return apiHeader


def main():
  deviceId = ''
  url = f'https://api.switch-bot.com/v1.1/devices/{deviceId}/status'
  headers = get_headers()
  response = requests.get(url, headers=headers)
  responseBody = response.json()['body']

  print ('{}'.format(responseBody))


if __name__ == "__main__":
  main()
