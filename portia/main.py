import os
from dotenv import load_dotenv
from portia import (
    Config,
    LLMModel,
    LLMProvider,
    Portia,
    PortiaToolRegistry,
    example_tool_registry
)
from github_actions import *
from aws_actions import *

github_tools = PortiaToolRegistry([
    InitializeGitHubClient(),
    ListGitHubRepos(),
    ListGitHubRepoFiles(),
    ReadGitHubFile(),
    GetGitHubFileWithMetadata(),
    CreateGitHubIssue(),
    GitHubAddCommitFile(),
    CreateGitHubPullRequest(),
])

aws_tools = PortiaToolRegistry([
    InitializeAWSClient(),
    ListAWSLogGroups(),
    GetMostRecentLogStream(),
    ListenForErrorLogs()
])


load_dotenv()

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

anthropic_config = Config.from_default(
    llm_provider=LLMProvider.ANTHROPIC,
    llm_model_name=LLMModel.CLAUDE_3_5_SONNET,
    anthropic_api_key=ANTHROPIC_API_KEY
)

def instantiate_portia():
    # TODO: Pass tool registry
    portia = Portia(config=anthropic_config, tools=github_tools + aws_tools)
    return portia

def execute_query(portia_instance, query: str):
    plan_run = portia_instance.run(query)
    return plan_run

