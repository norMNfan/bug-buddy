import boto3
import time
import json
from typing import List, Optional
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from threading import Lock
import logging

# boto3.set_stream_logger(name='botocore', level=logging.DEBUG)

class AWSClient:
    def __init__(self, access_key: str = None, secret_key: str = None, region: str = "us-east-1"):
        self.region = region
        
        # Use environment variables or credentials directly if passed
        if access_key and secret_key:
            self.client = boto3.client('logs', 
                                       aws_access_key_id=access_key, 
                                       aws_secret_access_key=secret_key,
                                       region_name=region)
        else:
            self.client = boto3.client('logs', region_name=region)

    def list_log_groups(self) -> List[str]:
        try:
            response = self.client.describe_log_groups()
            log_groups = [log_group['logGroupName'] for log_group in response['logGroups']]
            return log_groups
        except (NoCredentialsError, PartialCredentialsError):
            raise ValueError("Invalid or missing AWS credentials.")
        except Exception as e:
            raise RuntimeError(f"Error listing log groups: {e}")
    
    def get_most_recent_log_stream(self, log_group_name: str) -> str:
        try:
            response = self.client.describe_log_streams(
                logGroupName=log_group_name,
                orderBy='LastEventTime',
                descending=True,
                limit=1
            )
            if 'logStreams' in response and response['logStreams']:
                return response['logStreams'][0]['logStreamName']
            else:
                raise RuntimeError(f"No log streams found for log group {log_group_name}")
        except Exception as e:
            raise RuntimeError(f"Error fetching log streams: {e}")
    
    def listen_for_error_logs(self, log_group_name: str, log_stream_name: str) -> List[str]:
        error_logs = []
        try:
            # Poll logs for new entries
            while True:
                response = self.client.get_log_events(
                    logGroupName=log_group_name,
                    logStreamName=log_stream_name,
                    startFromHead=False  # Get the latest events
                )

                for event in response.get('events', []):
                    message = event['message']
                    if 'error' in message.lower():  # Simple error check, can be more advanced
                        error_logs.append(message)
                
                # Break after finding errors or continue depending on your needs
                if error_logs:
                    break

                # Poll every 5 seconds
                time.sleep(5)
            
            return error_logs
        except Exception as e:
            raise RuntimeError(f"Error listening for error logs: {e}")

class AWSClientManager:
    _client: AWSClient = None

    @classmethod
    def initialize(cls, access_key: str = None, secret_key: str = None, region: str = "us-east-1") -> None:
        cls._client = AWSClient(access_key, secret_key, region)

    @classmethod
    def get_client(cls) -> AWSClient:
        if cls._client is None:
            raise RuntimeError("AWS client has not been initialized. Call initialize() first.")
        return cls._client
