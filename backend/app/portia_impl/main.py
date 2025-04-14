import os
from dotenv import load_dotenv
from portia import (
    Config,
    InMemoryToolRegistry,
    LLMModel,
    LLMProvider,
    Portia,
    StorageClass,
    StorageClass,
    PlanRunState
)
from portia.storage import PortiaCloudStorage
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
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

anthropic_config = Config.from_default(
    llm_provider=LLMProvider.OPENAI,
    llm_model_name=LLMModel.GPT_4_O,
    anthropic_api_key=OPENAI_API_KEY,
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

    HEAD_BRANCH = os.getenv("HEAD_BRANCH")
    BASE_BRANCH = os.getenv("BASE_BRANCH")


    query = """
        1. List the log groups
        2. then select the first log group
        3. then list all the log streams for that group
        4. then listen for error logs in that most recent stream
        5. if there are any error logs, as in the list is not empty, ask the user on how to handle this via either creating a PR or an ISSUE using the on_error_log_human_decision tool
            DO NOT CONTINUE UNTIL AFTER THE HUMAN HAS PROVIDED A CLARIFICATION RESPONSE
        6. list all the repos under this owner: {GITHUB_USERNAME}
        7. list files under this repo: {REPO_NAME} for owner: {GITHUB_USERNAME} at the root of the repo
        8. from those list of files, select the file that is best associated with the file for which the error is in error using the owner: {GITHUB_USERNAME} and repo: {REPO_NAME}. Select the file by name as you dedeuce from the error, not by some arbitrary path which doesn't exist.
        9. read the selected file's contents. Use the Use the repo: {REPO_NAME} and owner: {GITHUB_USERNAME}
        10. based on the human clarification resolution, you should do either create a PR if the human said PR or create an ISSUE if the human said ISSUE
            if the human said PR do the following (ONLY DO THESE IF PR):
                 - generate a fix taking into account the errors and the selected file content.
                 - Then commit this fix to the selected file in the repo: {REPO_NAME} using github_add_commit_file tool; this commit should be on branch: {HEAD_BRANCH} as the feature branch with base_branch as {BASE_BRANCH}.
                 - Then createa a github pull request from the feature branch {HEAD_BRANCH} using the create_github_pull_request tool; you appropriately decide on the body and title of the PR. Use the repo: {REPO_NAME} head_branch={HEAD_BRANCH}, and base_branch={BASE_BRANCH}.
            
            else if the human said ISSUE, create an ISSUE like a bug report, stating the errors found in the logs. Use the repo: {REPO_NAME} and owner: {GITHUB_USERNAME}. you decide the title and body appropriately of the issue
        """.format(GITHUB_USERNAME=GITHUB_USERNAME, REPO_NAME=REPO_NAME, BASE_BRANCH=BASE_BRANCH, HEAD_BRANCH=HEAD_BRANCH)

    plan = portia.plan(query)

    return plan

def run_plan(plan_id: str):
    portia = instantiate_portia()

    my_store = PortiaCloudStorage(config=anthropic_config)

    plan = my_store.get_plan(plan_id)

    run = portia.run_plan(plan)
    
    return run.outputs.clarifications[0]


def resume_run(plan_run_id:str, user_input:str):
    portia = instantiate_portia()

    my_store = PortiaCloudStorage(config=anthropic_config)

    plan_run = my_store.get_plan_run(plan_run_id)
    plan = my_store.get_plan(plan_run.plan_id)


    while plan_run.state == PlanRunState.NEED_CLARIFICATION:
        for clarification in plan_run.get_outstanding_clarifications():
            plan_run = portia.resolve_clarification(clarification, user_input, plan_run)

        plan_run = portia.resume(plan_run, plan_run.id)
    
    return plan_run


if __name__ == "__main__":
    plan = create_plan()
    plan_id = plan.id

    plan_start = run_plan(plan_id)

    plan_run_id = plan_start.plan_run_id

    resumed_run = resume_run(plan_run_id, "PR")
    print("\n RESUMED RUN")
    print(resumed_run)
