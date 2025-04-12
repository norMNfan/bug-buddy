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
    # InitializeGitHubClient(),
    ListGitHubRepos(),
    ListGitHubRepoFiles(),
    ReadGitHubFile(),
    GetGitHubFileWithMetadata(),
    CreateGitHubIssue(),
    GitHubAddCommitFile(),
    CreateGitHubPullRequest(),
])

aws_tools = InMemoryToolRegistry.from_local_tools([
    # InitializeAWSClient(),
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


def initialise_github():
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')

    ctx = {}  
    initialize_tool = InitializeGitHubClient()
    print("Initializing GitHub Client...")
    print(initialize_tool.run(ctx, token=GITHUB_TOKEN, username=GITHUB_USERNAME))

def initialise_aws():
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET = os.getenv("AWS_SECRET")
    AWS_REGION = os.getenv("AWS_REGION")

    print(f"ACCESS KEY: {AWS_ACCESS_KEY}")
    print(f"SECRET: {AWS_SECRET}")
    print(f"REGION: {AWS_REGION}")

    ctx = {}  
    initialize_tool = InitializeAWSClient()

    print(initialize_tool.run(ctx, access_key=AWS_ACCESS_KEY, secret_key=AWS_SECRET, region=AWS_REGION))

def whole_flow():
    initialise_github()

    initialise_aws()

    portia = instantiate_portia()

    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')

    REPO_NAME = os.getenv('GITHUB_REPO')


    query = """
1. List the log groups
        2. then select the first log group
        3. then list all the log streams for that group
        4. then listen for error logs in that most recent stream
        5. list all the repos under this user: {GITHUB_USERNAME}
        6. list files under this repo: {REPO_NAME} for owner: {GITHUB_USERNAME}
        7. from those list of files, select the one that is best associated with the error using the owner and repo info form before
        8. view the contents of the selected file using the owner and repo information from before
        9. propose a fix for this error given the contents of the file from before, and output a diff of the solution and the existing content
        10. Create an issue in Github with the proposed changes using Github credentials from before
        11. In the final output, format the before and after diff using markdown
        """.format(GITHUB_USERNAME=GITHUB_USERNAME, REPO_NAME=REPO_NAME)

    list_log_groups_plan = portia.plan(query)

    print(list_log_groups_plan.pretty_print())

    list_log_groups_run = portia.run_plan(list_log_groups_plan)
    print(list_log_groups_run.model_dump_json(indent=2))
    
    return list_log_groups_run.model_dump_json(indent=2)


def run():
    return whole_flow()

def notnotnotmain():
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET = os.getenv("AWS_SECRET")
    AWS_REGION = os.getenv("AWS_REGION")

    print(f"ACCESS KEY: {AWS_ACCESS_KEY}")
    print(f"SECRET: {AWS_SECRET}")
    print(f"REGION: {AWS_REGION}")

    portia = instantiate_portia()
    ctx = {}  
    initialize_tool = InitializeAWSClient()

    print(initialize_tool.run(ctx, access_key=AWS_ACCESS_KEY, secret_key=AWS_SECRET, region=AWS_REGION))

    list_log_groups_tool = ListAWSLogGroups()
    print(f"\n Listing log groups for {AWS_REGION}")
    log_groups = list_log_groups_tool.run(ctx)
    print(log_groups)

    most_recent_log_stream_tool = GetMostRecentLogStream()
    print(f"\n Getting recent log stream for group {log_groups[0]}")
    log_stream = most_recent_log_stream_tool.run(ctx, log_group_name=log_groups[0])
    print(log_stream)

    listen_for_error_logs_tool = ListenForErrorLogs()
    print(f"\n Listening for error logs for group: {log_groups[0]} and stream: {log_stream}")
    error_logs = listen_for_error_logs_tool.run(ctx, log_group_name=log_groups[0], log_stream_name=log_stream)
    print(error_logs)




def notmain():
    # === SET THESE VALUES ===
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GITHUB_USERNAME = os.getenv('williamdarkocode')

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

    # print("\nAdding and committing file:")
    # print(commit_tool.run(ctx, 
    #     owner=GITHUB_USERNAME,
    #     repo=REPO_NAME,
    #     path=NEW_FILE_PATH,
    #     content=NEW_FILE_CONTENT,
    #     message=f"NEWWW {COMMIT_MESSAGE}",
    #     branch=HEAD_BRANCH,
    #     base_branch=BASE_BRANCH
    # ))

    # print("\nCreating pull request:")
    # print(pr_tool.run(ctx, 
    #     owner=GITHUB_USERNAME,
    #     repo=REPO_NAME,
    #     head_branch=HEAD_BRANCH,
    #     base_branch=BASE_BRANCH,
    #     title=PULL_REQUEST_TITLE,
    #     body=PULL_REQUEST_BODY
    # ))




if __name__ == "__main__":
    run()
