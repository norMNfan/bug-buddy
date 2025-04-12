import os
from dotenv import load_dotenv
from portia import (
    Config,
    InMemoryToolRegistry,
    LLMModel,
    LLMProvider,
    Plan,
    Portia,
    StorageClass
    PortiaToolRegistry,
    StorageClass,
    PlanRunState,
    example_tool_registry
)
from portia.storage import PortiaCloudStorage
from github_actions import *
from aws_actions import *

github_tools = InMemoryToolRegistry.from_local_tools([
    # InitializeGitHubClient(),
    ListGitHubRepos(),
    ListGitHubRepoFiles(),
    ReadGitHubFile(),
    GetGitHubFileWithMetadata(),
    CreateGitHubIssue(),
    GitHubAddCommitFile(),
    CreateGitHubPullRequest(),
    OnErrorLogFoundHumanDecisionTool()
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
    anthropic_api_key=ANTHROPIC_API_KEY,
    storage_class=StorageClass.CLOUD
)

def instantiate_portia():
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


def create_plan():
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
        5. if there are any error logs, as in the list is not empty, ask the user on how to handle this via either creating a PR or an ISSUE using the on_error_log_human_decision tool
        6. list all the repos under this user: {GITHUB_USERNAME}
        7. list files under this repo: {REPO_NAME} for owner: {GITHUB_USERNAME}
        8. from those list of files, select the one that is best associated with the error using the owner and repo info form before
        9. view the contents of the selected file using the owner and repo information from before
        10. propose a fix for this error given the contents of the file from before, and output a diff of the solution and the existing content
        11. Create an issue in Github with the proposed changes using Github credentials from before
        12. In the final output, format the before and after diff using markdown
        """.format(GITHUB_USERNAME=GITHUB_USERNAME, REPO_NAME=REPO_NAME)

    plan = portia.plan(query)

    return plan

def run_plan(plan_id: str):
    portia = instantiate_portia()

    my_store = PortiaCloudStorage(config=anthropic_config)

    plan = my_store.get_plan(plan_id)

    run = portia.run_plan(plan)
    # print(run.model_dump_json(indent=2))
    
    # return run.model_dump_json(indent=2)
    return run.outputs.clarifications[0]


def resume_run(plan_run_id:str, user_input:str):
    portia = instantiate_portia()

    my_store = PortiaCloudStorage(config=anthropic_config)

    plan_run = my_store.get_plan_run(plan_run_id)
    plan = my_store.get_plan(plan_run.plan_id)

    resumed_plan_run = portia.resume(plan_run, plan_run_id)

    while resumed_plan_run.state == PlanRunState.NEED_CLARIFICATION:
        for clarification in plan_run.get_outstanding_clarifications():
            print(clarification)

    return resumed_plan_run


if __name__ == "__main__":
    plan = create_plan()
    plan_id = plan.id

    plan_start = run_plan(plan_id)

    print(plan_start)