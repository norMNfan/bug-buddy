import os
from dotenv import load_dotenv
from portia import (
    Config,
    InMemoryToolRegistry,
    LLMModel,
    LLMProvider,
    Portia,
    PortiaToolRegistry,
    example_tool_registry
)
from .github_actions import *
from .aws_actions import *

github_tools = InMemoryToolRegistry.from_local_tools([
    InitializeGitHubClient(),
    ListGitHubRepos(),
    ListGitHubRepoFiles(),
    ReadGitHubFile(),
    GetGitHubFileWithMetadata(),
    CreateGitHubIssue(),
    GitHubAddCommitFile(),
    CreateGitHubPullRequest(),
])

aws_tools = InMemoryToolRegistry.from_local_tools([
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
    plan_run = portia_instance.run(ctx, query)
    return plan_run



def run():
    # === SET THESE VALUES ===
    GITHUB_TOKEN = "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"
    GITHUB_USERNAME = "williamdarkocode"

    # === Example values for testing ===
    REPO_NAME = "go-shopify-williamdarkocode"
    FILE_PATH = "README.md"
    NEW_FILE_PATH = "bug-buddy/new_file.txt"
    NEW_FILE_CONTENT = "This is a test file."
    COMMIT_MESSAGE = "Add new test file"
    ISSUE_TITLE = "Sample Issue"
    ISSUE_BODY = "This is a test issue created via the bug-buddy tool."
    HEAD_BRANCH = "feature-branch"
    BASE_BRANCH = "master"
    PULL_REQUEST_TITLE = "Test PR"
    PULL_REQUEST_BODY = "This PR was created as a test."

    # === Initialize Portia and GitHub Client ===
    portia = instantiate_portia()
    ctx = {}  
    initialize_tool = InitializeGitHubClient()
    print("Initializing GitHub Client...")
    print(initialize_tool.run(ctx, token=GITHUB_TOKEN, username=GITHUB_USERNAME))

    # === Tool Instances ===
    list_repos_tool = ListGitHubRepos()
    list_files_tool = ListGitHubRepoFiles()
    read_file_tool = ReadGitHubFile()
    metadata_tool = GetGitHubFileWithMetadata()
    create_issue_tool = CreateGitHubIssue()
    commit_tool = GitHubAddCommitFile()
    pr_tool = CreateGitHubPullRequest()

    # print("\nListing repositories:")
    # print(list_repos_tool.run(ctx, user=GITHUB_USERNAME))

    # print("\nListing files in repo:")
    # print(list_files_tool.run(ctx, owner=GITHUB_USERNAME, repo=REPO_NAME, path=""))

    # print("\nReading file from repo:")
    # print(read_file_tool.run(ctx, owner=GITHUB_USERNAME, repo=REPO_NAME, path=FILE_PATH))

    # print("\nGetting file with metadata:")
    # print(metadata_tool.run(ctx, owner=GITHUB_USERNAME, repo=REPO_NAME, path=FILE_PATH))

    # print("\nCreating GitHub issue:")
    # print(create_issue_tool.run(ctx, 
    #     owner=GITHUB_USERNAME,
    #     repo=REPO_NAME,
    #     title=ISSUE_TITLE,
    #     body=ISSUE_BODY
    # ))

    print("\nAdding and committing file:")
    print(commit_tool.run(ctx, 
        owner=GITHUB_USERNAME,
        repo=REPO_NAME,
        path=NEW_FILE_PATH,
        content=NEW_FILE_CONTENT,
        message=f"NEWWW {COMMIT_MESSAGE}",
        branch=HEAD_BRANCH,
        base_branch=BASE_BRANCH
    ))

    print("\nCreating pull request:")
    print(pr_tool.run(ctx, 
        owner=GITHUB_USERNAME,
        repo=REPO_NAME,
        head_branch=HEAD_BRANCH,
        base_branch=BASE_BRANCH,
        title=PULL_REQUEST_TITLE,
        body=PULL_REQUEST_BODY
    ))


if __name__ == "__main__":
    run()
