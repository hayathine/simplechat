# lambda/index.py
import json
import os
import boto3
import re  # 正規表現モジュールをインポート
import urllib.request

URL = 'https://841f-34-143-229-198.ngrok-free.app'
API_URL = f'{URL}/generate'

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        # リクエストボディの解析
        body = json.loads(event['body'])
        message = body['message']
        conversation_history = body.get('conversationHistory', [])
        
        # API_Requestデータの準備
        request_data = {
            'prompt' : message,
            'max_new_tokens' : 512,
            'temperature' : 0.9,
            'top_p' : 0.9,
            'do_sample' : True,
        }

        # HTTP Request
        request = urllib.request.Request(
            API_URL,
            data = json.dumps(request_data).encode('utf-8'),
            headers = {"Content-Type": "application/json"},
            method = "POST"
        )
        
        # Responseを受け取る
        with urllib.request.urlopen(request) as response:
            response_body = response.read()
            result = json.loads(response_body)

        print("response:", json.dumps(response_body, default=str))

        # 応答の検証
        try:
            assistant_response = result['output']['message']['content'][0]['text']
        except (KeyError, IndexError) as e:
            raise Exception(f"Invalid response structure: {e}")

        

        # # conversation_history に追加
        # messages = ({
        #     "role": "assistant",
        #     "content": assistant_response
        # })

        # 成功レスポンスの返却
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
            })
        }
        
    except Exception as error:
        print("Error:", str(error))
        
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }
