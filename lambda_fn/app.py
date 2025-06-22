import os
import json
import logging
import boto3
from datetime import datetime

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")

    try:
        table_name = os.environ.get("TABLE_NAME")
        if not table_name:
            raise ValueError("TABLE_NAME environment variable is not set.")

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(table_name)

        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
        elif not isinstance(body, dict):
            raise ValueError("Invalid request body format.")

        message_uuid = body.get("messageUUID")
        message_text = body.get("messageText")
        message_datetime = body.get("messageDatetime")

        if not isinstance(message_text, str):
            raise ValueError("messageText must be a string.")
        if not (10 <= len(message_text) <= 100):
            raise ValueError("messageText must be between 10 and 100 characters.")

        try:
            datetime.strptime(message_datetime, "%Y-%m-%d %H:%M:%S")
        except Exception:
            raise ValueError("messageDatetime must be in YYYY-MM-DD HH:MM:SS format.")

        table.put_item(Item={
            "messageUUID": message_uuid,
            "messageText": message_text,
            "messageDatetime": message_datetime
        })

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Saved successfully."})
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }