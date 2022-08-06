import sys
sys.path.append('/var/task/modules')

import os
import json
import requests
import cek
from cek.core import ApplicationIdMismatch
from cryptography.exceptions import InvalidSignature

beebotte_url = os.getenv('BEEBOTTE_URL')
extension_id = os.getenv('CLOVA_EXTENSION_ID')
response_builder = cek.ResponseBuilder()
clova = cek.Clova(
    application_id=extension_id,
    default_language='ja',
    debug_mode=True
)

def handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))

    try:
        if event['request']['type'] == 'LaunchRequest':
            return launch_request_handler()
        elif event['request']['type'] == 'IntentRequest':
            called_solts = event['request']['intent']['slots'].keys() 

            # Command Intent 
            if 'switchon' in called_solts:
                return switchon_intent_handler()
            elif 'switchoff' in called_solts:
                return switchoff_intent_handler()
            elif 'sleep' in called_solts:
                return sleep_intent_handler()
            elif 'dry' in called_solts:
                return dry_intent_handler()
            
            return clova.response('もう一度お願いします')
        elif event['request']['type'] == 'SessionEndedRequest':
            return clova.response('それではごゆっくり')
    except InvalidSignature:
        return get_lambda_response(401, {"error": "InvalidSignature"})
    except ApplicationIdMismatch as e:
        return get_lambda_response(401, {"error": "WrongApplicationId"})
    except Exception as e:
        print(e)
        return get_lambda_response(500)


def launch_request_handler():
    welcome_message = cek.Message(message='ホームハッカーへようこそ!', language="ja")
    return clova.response([welcome_message])

def switchon_intent_handler():
    result = requests.post(
        beebotte_url,
        json={
            "data":[{"cmd":"on"}]
        }
    )
    print("call_result: " + str(result.status_code))
    if result.status_code == 200:
        message = cek.Message(message='スイッチを入れました', language="ja")
    else:
        message = cek.Message(message='スイッチを入れることができませんでした', language="ja")
    return clova.response([message]) 

def switchoff_intent_handler():
    result = requests.post(
        beebotte_url,
        json={
            "data":[{"cmd":"off"}]
        }
    )
    print("call_result: " + str(result.status_code))
    if result.status_code == 200:
        message = cek.Message(message='スイッチを切りました', language="ja")
    else:
        message = cek.Message(message='スイッチを切ることができませんでした', language="ja")
    return clova.response([message])

def sleep_intent_handler():
    result = requests.post(
        beebotte_url,
        json={
            "data":[{"cmd":"sleep"}]
        }
    )
    print("call_result: " + str(result.status_code))
    if result.status_code == 200:
        message = cek.Message(message='スリープモードになりました', language="ja")
    else:
        message = cek.Message(message='スリープモードになることができませんでした', language="ja")
    return clova.response([message]) 

def dry_intent_handler():
    result = requests.post(
        beebotte_url,
        json={
            "data":[{"cmd":"dry"}]
        }
    )
    print("call_result: " + str(result.status_code))
    if result.status_code == 200:
        message = cek.Message(message='除湿になりました', language="ja")
    else:
        message = cek.Message(message='除湿になることができませんでした', language="ja")
    return clova.response([message])

def get_lambda_response(status_code, response={}):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response),
        "isBase64Encoded": False
    }
