import logging

import boto3

logger = logging.getLogger()

def lambda_handler(event, context):
    logger.info(f"event: {event}", extra=dict(event=event))
    logger.info(f"context: {context}", extra=dict(context=context))
    print("Lambda handled!")
