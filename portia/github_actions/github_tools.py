from pydantic import BaseModel, Field
from portia import Tool, ToolRunContext
from .github_client import GitHubClient
from .github_client_manager import GitHubClientManager
from typing import Any

class ListReposSchema(BaseModel):
    user: str = Field(..., description="GitHub username whose repositories should be listed")


class ListFilesSchema(BaseModel):
    owner: str = Field(..., description="GitHub organization or username")
    repo: str = Field(..., description="Repository name")
    path: str = Field("", description="Path within the repository to list files from")


class ReadFileSchema(BaseModel):
    owner: str = Field(..., description="GitHub organization or username")
    repo: str = Field(..., description="Repository name")
    path: str = Field(..., description="Path of the file to read")


class FileWithMetadataSchema(BaseModel):
    owner: str = Field(..., description="GitHub organization or username")
    repo: str = Field(..., description="Repository name")
    path: str = Field(..., description="Path of the file to retrieve with metadata")


class CreateIssueSchema(BaseModel):
    owner: str = Field(..., description="GitHub organization or username")
    repo: str = Field(..., description="Repository name")
    title: str = Field(..., description="Title of the issue")
    body: str = Field("", description="Body or description of the issue")


class AddCommitFileSchema(BaseModel):
    owner: str = Field(..., description="GitHub organization or username")
    repo: str = Field(..., description="Repository name")
    path: str = Field(..., description="Path of the file in the repo")
    content: str = Field(..., description="The file content to add or update")
    message: str = Field(..., description="Commit message")
    branch: str = Field("main", description="Branch to commit to")


class PullRequestSchema(BaseModel):
    owner: str = Field(..., description="GitHub organization or username")
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
    name: str = "initialize_github_client"
    description: str = "Initialize the GitHub client with token and username"
    args_schema: type[BaseModel] = InitGitHubClientSchema

    def run(self, _:ToolRunContext, token: str, username: str):
        GitHubClientManager.initialize(token, username)
        return f"GitHub client initialized for user {username}"



# 1. List Repositories
class ListGitHubRepos(Tool):
    name: str = "list_github_repos"  
    description: str = "List all GitHub repositories for a given user."  
    args_schema: type[BaseModel] = ListReposSchema

    def run(self, _:ToolRunContext, user: str) -> Any:
        client = GitHubClientManager.get_client()

        return client.list_repositories(user)


# 2. List Files
class ListGitHubRepoFiles(Tool):
    name: str = "list_github_repo_files"  
    description: str = "List files in a GitHub repository at a given path."  
    args_schema: type[BaseModel] = ListFilesSchema

    def run(self, _:ToolRunContext, owner: str, repo: str, path: str = "") -> Any:
        client = GitHubClientManager.get_client()

        return client.list_files(owner, repo, path)


# 3. Read File Content
class ReadGitHubFile(Tool):
    name: str = "read_github_file"  
    description: str = "Read the content of a file in a GitHub repository."  
    args_schema: type[BaseModel] = ReadFileSchema

    def run(self, _:ToolRunContext, owner: str, repo: str, path: str) -> Any:
        client = GitHubClientManager.get_client()

        return client.read_file(owner, repo, path)


# 4. File with Metadata
class GetGitHubFileWithMetadata(Tool):
    name: str = "get_github_file_with_metadata"  
    description: str = "Get metadata and decoded content for a specific file."  
    args_schema: type[BaseModel] = FileWithMetadataSchema

    def run(self, _:ToolRunContext, owner: str, repo: str, path: str) -> Any:
        client = GitHubClientManager.get_client()

        return client.get_file_metadata_and_content(owner, repo, path)


# 5. Create Issue (auth)
class CreateGitHubIssue(Tool):
    name: str = "create_github_issue"  
    description: str = "Create an issue on a GitHub repository."  
    args_schema: type[BaseModel] = CreateIssueSchema

    def run(self, _:ToolRunContext, owner: str, repo: str, title: str, body: str) -> Any:
        client = GitHubClientManager.get_client()

        token = self.get_secret("GITHUB_TOKEN")
        return client.create_issue(token, owner, repo, title, body)


# 6. Add & Commit File (auth)
class GitHubAddCommitFile(Tool):
    name: str = "github_add_commit_file"  
    description: str = "Add or update a file in a GitHub repo and commit it."  
    args_schema: type[BaseModel] = AddCommitFileSchema

    def run(self, _:ToolRunContext, owner: str, repo: str, path: str, content: str, message: str, branch: str = "main") -> Any:
        client = GitHubClientManager.get_client()

        token = self.get_secret("GITHUB_TOKEN")
        return client.add_and_commit_file(token, owner, repo, path, content, message, branch)


# 7. Create Pull Request (auth)
class CreateGitHubPullRequest(Tool):
    name: str = "create_github_pull_request"  
    description: str = "Create a pull request from a feature branch."  
    args_schema: type[BaseModel] = PullRequestSchema

    def run(self, _:ToolRunContext, owner: str, repo: str, head_branch: str, base_branch: str, title: str, body: str = "") -> Any:
        client = GitHubClientManager.get_client()

        token = self.get_secret("GITHUB_TOKEN")
        return client.create_pull_request(token, owner, repo, head_branch, base_branch, title, body)