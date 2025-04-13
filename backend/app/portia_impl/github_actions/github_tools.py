from pydantic import BaseModel, Field
from portia import Tool, ToolRunContext, MultipleChoiceClarification
from .github_client_manager import GitHubClientManager
from typing import Any, List, Literal

class ListReposSchema(BaseModel):
    user: str = Field(..., description="GitHub username whose repositories should be listed")


class ListFilesSchema(BaseModel):
    repo: str = Field(..., description="Repository name")
    path: str = Field("", description="Path within the repository to list files from")


class ReadFileSchema(BaseModel):
    repo: str = Field(..., description="Repository name")
    path: str = Field(..., description="Path of the file to read")


class FileWithMetadataSchema(BaseModel):
    repo: str = Field(..., description="Repository name")
    path: str = Field(..., description="Path of the file to retrieve with metadata")


class CreateIssueSchema(BaseModel):
    repo: str = Field(..., description="Repository name")
    title: str = Field(..., description="Title of the issue")
    body: str = Field("", description="Body or description of the issue")


class AddCommitFileSchema(BaseModel):
    repo: str = Field(..., description="Repository name")
    path: str = Field(..., description="Path of the file in the repo")
    content: str = Field(..., description="The file content to add or update")
    message: str = Field(..., description="Commit message")
    branch: str = Field("main", description="Branch to commit to")
    base_branch: str = Field("main", description="Branch to commit to")


class PullRequestSchema(BaseModel):
    repo: str = Field(..., description="Repository name")
    head_branch: str = Field(..., description="Source branch (the one with changes)")
    base_branch: str = Field(..., description="Destination branch (usually 'main')")
    title: str = Field(..., description="Pull request title")
    body: str = Field("", description="Pull request description or body text")



"""
    Initialise github client
"""
class InitGitHubClientSchema(BaseModel):
    token: str = Field(..., description="GitHub personal access token")
    username: str = Field(..., description="GitHub username for authentication")

class InitializeGitHubClient(Tool):
    id: str = "initialize_github_client"
    name: str = "initialize_github_client"
    description: str = "Initialize the GitHub client with token and username"
    args_schema: type[BaseModel] = InitGitHubClientSchema
    output_schema: tuple[str, str] = ("str", "Success or failure of the tool")

    def run(self, _:ToolRunContext, token: str, username: str):
        GitHubClientManager.initialize(token, username)
        return f"GitHub client initialized for user {username}"


"""
    Human input clarification
"""
class OnErrorLogFoundHumanDecisionSchema(BaseModel):
    """Input for the OnErrorLogFoundHumanDecisionTool."""

    error_logs: List[str] = Field(
        description="The list of error logs"
    )

    human_decision: Literal["PR", "ISSUE"] | None = Field(
        None,
        description=(
            "Whether we create a PR or create an ISSUE.\n"
            "This MUST be set to None until the clarification check has been done.\n"
            "If the human says PR, this value will be 'PR'.\n"
            "If the human says ISSUE, this value will be 'ISSUE'."
        ),
    )

class OnErrorLogFoundHumanDecisionTool(Tool):
    id: str = "on_error_log_human_decision"
    name: str = "on_error_log_human_decision"  
    description: str = "Query the user on how to address the error via making a PR or an ISSUE."  
    args_schema: type[BaseModel] = OnErrorLogFoundHumanDecisionSchema
    output_schema: tuple[str, str] = (
            "str",
            "PR or ISSUE depending on the human decision",
        )
    def run(self, context:ToolRunContext, error_logs: List[str], human_decision: Literal["PR", "ISSUE"] | None = None) -> Any:
        if human_decision is None:
            return MultipleChoiceClarification(
                plan_run_id=context.plan_run_id,
                user_guidance=(
                    "I've found the following error(s) in your logs:\n"
                    f"{error_logs}"
                    "You can choose to either make a PR where I suggest a fix or create an ISSUE"
                ),
                argument_name="human_decision",
                options=["PR", "ISSUE"],
            )
        else:
            return human_decision



# 1. List Repositories
class ListGitHubRepos(Tool):
    id: str = "list_github_repos"
    name: str = "list_github_repos"  
    description: str = "List all GitHub repositories for a given owner/user."  
    args_schema: type[BaseModel] = ListReposSchema
    output_schema: tuple[str, str] = ("List", "List repositories for a user or the authenticated account")

    def run(self, _:ToolRunContext, user: str) -> Any:
        client = GitHubClientManager.get_client()

        return client.list_repositories(user)


# 2. List Files
class ListGitHubRepoFiles(Tool):
    id: str = "list_github_repo_files"
    name: str = "list_github_repo_files"  
    description: str = "List all files in a GitHub repository at a given path."  
    args_schema: type[BaseModel] = ListFilesSchema
    output_schema: tuple[str, str] = ("List", "List of files in a repository at a given path")

    def run(self, _:ToolRunContext, repo: str, path: str = "") -> Any:
        client = GitHubClientManager.get_client()

        return client.list_files(client.username, repo, path)


# 3. Read File Content
class ReadGitHubFile(Tool):
    id: str = "read_github_file"
    name: str = "read_github_file"  
    description: str = "Read the content of a file in a GitHub repository."  
    args_schema: type[BaseModel] = ReadFileSchema
    output_schema: tuple[str, str] = ("str", "Read a file's content from a repository")

    def run(self, _:ToolRunContext, repo: str, path: str) -> Any:
        client = GitHubClientManager.get_client()

        return client.read_file(client.username, repo, path)


# 4. File with Metadata
class GetGitHubFileWithMetadata(Tool):
    id: str = "get_github_file_with_metadata"
    name: str = "get_github_file_with_metadata"  
    description: str = "Get metadata and decoded content for a specific file."  
    args_schema: type[BaseModel] = FileWithMetadataSchema
    output_schema: tuple[str, str] = ("dict", "Get file metadata and content as a dict")

    def run(self, _:ToolRunContext, repo: str, path: str) -> Any:
        client = GitHubClientManager.get_client()

        return client.get_file_metadata_and_content(client.username, repo, path)


# 5. Create Issue (auth)
class CreateGitHubIssue(Tool):
    id: str = "create_github_issue"
    name: str = "create_github_issue"  
    description: str = "Create an issue on a GitHub repository."  
    args_schema: type[BaseModel] = CreateIssueSchema
    output_schema: tuple[str, str] = ("any", "Create an issue on a repository")

    def run(self, _:ToolRunContext, repo: str, title: str, body: str) -> Any:
        client = GitHubClientManager.get_client()

        token = client.token
        # return client.create_issue(token, owner, repo, title, body)
        return client.create_issue(client.username, repo, title, body)


# 6. Add & Commit File (auth)
class GitHubAddCommitFile(Tool):
    id: str = "github_add_commit_file"
    name: str = "github_add_commit_file"  
    description: str = "Add or update a file in a GitHub repo and commit it."  
    args_schema: type[BaseModel] = AddCommitFileSchema
    output_schema: tuple[str, str] = ("any", "Add or update a file and commit it to a repository")

    def run(self, _:ToolRunContext, repo: str, path: str, content: str, message: str, branch: str = "main", base_branch: str = "main") -> Any:
        client = GitHubClientManager.get_client()

        token = client.token
        return client.add_and_commit_file(client.username, repo, path, content, message, branch, base_branch)


# 7. Create Pull Request (auth)
class CreateGitHubPullRequest(Tool):
    id: str = "create_github_pull_request"
    name: str = "create_github_pull_request"  
    description: str = "Create a pull request from a feature branch."  
    args_schema: type[BaseModel] = PullRequestSchema
    output_schema: tuple[str, str] = ("any", "Create a pull request from head_branch to base_branch")

    def run(self, _:ToolRunContext, repo: str, head_branch: str, base_branch: str, title: str, body: str = "") -> Any:
        client = GitHubClientManager.get_client()

        token = client.token
        return client.create_pull_request(client.username, repo, head_branch, base_branch, title, body)