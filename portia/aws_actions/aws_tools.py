from typing import List
from portia.tool import Tool
from pydantic import BaseModel, Field
from aws_client import AWSClient


class InitAWSClientSchema(BaseModel):
    access_key: str = Field(..., description="AWS access key ID")
    secret_key: str = Field(..., description="AWS secret access key")
    region: str = Field("us-east-1", description="AWS region for operations")

class InitializeAWSClient(Tool):
    name = "initialize_aws_client"
    description = "Initialize the AWS client with credentials and region"
    parameters_class = InitAWSClientSchema

    def run(self, access_key: str, secret_key: str, region: str = "us-east-1"):
        self.client = AWSClient(access_key=access_key, secret_key=secret_key, region=region)
        return f"AWS client initialized for region {region}."


class ListLogGroupsSchema(BaseModel):
    """Schema to list CloudWatch log groups."""
    region: str = Field(..., description="AWS region to fetch log groups from")

class GetLogStreamSchema(BaseModel):
    """Schema to get log streams from a specified log group."""
    log_group_name: str = Field(..., description="Name of the CloudWatch log group to get streams from")

class ListenForErrorLogsSchema(BaseModel):
    """Schema to listen for error logs in a CloudWatch log stream."""
    log_group_name: str = Field(..., description="Log group name")
    log_stream_name: str = Field(..., description="Log stream name to listen for errors")



# Example Tool: List AWS CloudWatch Log Groups
class ListAWSLogGroups(Tool):
    name = "list_aws_log_groups"
    description = "List all CloudWatch log groups for a specified AWS account."
    parameters_class = ListLogGroupsSchema  # Define the schema for this tool

    def run(self) -> List[str]:
        return self.client.list_log_groups()


# Example Tool: Get Most Recent Log Stream
class GetMostRecentLogStream(Tool):
    name = "get_most_recent_log_stream"
    description = "Get the most recent log stream for a given CloudWatch log group."
    parameters_class = GetLogStreamSchema  # Define schema for this tool

    def run(self, log_group_name: str) -> str:
        return self.client.get_most_recent_log_stream(log_group_name)


# Example Tool: Listen for Error Logs
class ListenForErrorLogs(Tool):
    name = "listen_for_error_logs"
    description = "Listen for error logs in a specific CloudWatch log group and stream."
    parameters_class = ListenForErrorLogsSchema  # Define schema for this tool

    def run(self, log_group_name: str, log_stream_name: str) -> List[str]:
        return self.client.listen_for_error_logs(log_group_name, log_stream_name)
