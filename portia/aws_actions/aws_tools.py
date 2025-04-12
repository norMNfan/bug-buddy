from typing import List
from portia import Tool, ToolRunContext
from pydantic import BaseModel, Field
from .aws_client import AWSClientManager


class InitAWSClientSchema(BaseModel):
    access_key: str = Field(..., description="AWS access key ID")
    secret_key: str = Field(..., description="AWS secret access key")
    region: str = Field("us-east-1", description="AWS region for operations")

class InitializeAWSClient(Tool):
    id: str = "initialize_aws_client"
    name: str = "initialize_aws_client"
    description: str = "Initialize the AWS client with credentials and region"
    args_schema: type[BaseModel] = InitAWSClientSchema
    output_schema: tuple[str, str] = ("str", "Success or failure message upon connection attempt")

    def run(self, _:ToolRunContext, access_key: str, secret_key: str, region: str = "us-east-1"):
        self.client = AWSClientManager.initialize(access_key=access_key, secret_key=secret_key, region=region)
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
    id: str = "list_aws_log_groups"
    name: str = "list_aws_log_groups"
    description: str = "List all CloudWatch log groups for a specified AWS account."
    args_schema: type[BaseModel] = ListLogGroupsSchema  # Define the schema for this tool
    output_schema: tuple[str, str] = ("List", "Return list of string representing the list of log groups")

    def run(self) -> List[str]:
        client = AWSClientManager.get_client()
        return client.list_log_groups()


# Example Tool: Get Most Recent Log Stream
class GetMostRecentLogStream(Tool):
    id: str = "get_most_recent_log_stream"
    name: str = "get_most_recent_log_stream"
    description: str = "Get the most recent log stream for a given CloudWatch log group."
    args_schema: type[BaseModel] = GetLogStreamSchema  # Define schema for this tool
    output_schema: tuple[str, str] = ("str", "Get the name of the most recent log stream")

    def run(self, _:ToolRunContext, log_group_name: str) -> str:
        client = AWSClientManager.get_client()
        return client.get_most_recent_log_stream(log_group_name)


# Example Tool: Listen for Error Logs
class ListenForErrorLogs(Tool):
    id: str = "listen_for_error_logs"
    name: str = "listen_for_error_logs"
    description: str = "Listen for error logs in a specific CloudWatch log group and stream."
    args_schema: type[BaseModel] = ListenForErrorLogsSchema  # Define schema for this tool
    output_schema: tuple[str, str] = ("List", "Poll and listen for error logs and return a list of error logs")

    def run(self, _:ToolRunContext, log_group_name: str, log_stream_name: str) -> List[str]:
        client = AWSClientManager.get_client()
        return client.listen_for_error_logs(log_group_name, log_stream_name)
