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


def _get_secrets():
  # ref. https://github.com/aws/aws-secretsmanager-caching-python

  client = botocore.session.get_session().create_client('secretsmanager')
  cache_config = SecretCacheConfig()
  cache = SecretCache( config = cache_config, client = client)

  secret_string = cache.get_secret_string('switchbot')
  secret_json = json.loads(secret_string)
  device_id = secret_json['device_id']
  token = secret_json['token']
  secret = secret_json['secret']

  return device_id, token, secret


def get_data():
  # ref. https://github.com/OpenWonderLabs/SwitchBotAPI

  device_id, token, secret = _get_secrets()

  url = f'https://api.switch-bot.com/v1.1/devices/{device_id}/status'

  apiHeader = {}

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

  response = requests.get(url, headers=apiHeader)
  response_body = response.json()['body']

  return response_body


if __name__ == "__main__":
  data = get_data()
  print ('{}'.format(data))
