from pydantic import BaseModel, Field
from portia import Tool
from github_client import GitHubClient
from github_client_manager import GitHubClientManager
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
    name = "initialize_github_client"
    description = "Initialize the GitHub client with token and username"
    parameters_class = InitGitHubClientSchema

    def run(self, token: str, username: str):
        GitHubClientManager.initialize(token, username)
        return f"GitHub client initialized for user {username}"


client = GitHubClientManager.get_client()

# 1. List Repositories
class ListGitHubRepos(Tool):
    name = "list_github_repos"
    description = "List all GitHub repositories for a given user."
    parameters_class = ListReposSchema

    def run(self, user: str) -> Any:
        return client.list_repos(user)


# 2. List Files
class ListGitHubRepoFiles(Tool):
    name = "list_github_repo_files"
    description = "List files in a GitHub repository at a given path."
    parameters_class = ListFilesSchema

    def run(self, owner: str, repo: str, path: str = "") -> Any:
        return client.list_files(owner, repo, path)


# 3. Read File Content
class ReadGitHubFile(Tool):
    name = "read_github_file"
    description = "Read the content of a file in a GitHub repository."
    parameters_class = ReadFileSchema

    def run(self, owner: str, repo: str, path: str) -> Any:
        return client.read_file(owner, repo, path)


# 4. File with Metadata
class GetGitHubFileWithMetadata(Tool):
    name = "get_github_file_with_metadata"
    description = "Get metadata and decoded content for a specific file."
    parameters_class = FileWithMetadataSchema

    def run(self, owner: str, repo: str, path: str) -> Any:
        return client.get_file_with_metadata(owner, repo, path)


# 5. Create Issue (auth)
class CreateGitHubIssue(Tool):
    name = "create_github_issue"
    description = "Create an issue on a GitHub repository."
    parameters_class = CreateIssueSchema

    def run(self, owner: str, repo: str, title: str, body: str) -> Any:
        token = self.get_secret("GITHUB_TOKEN")
        return client.create_issue(token, owner, repo, title, body)


# 6. Add & Commit File (auth)
class GitHubAddCommitFile(Tool):
    name = "github_add_commit_file"
    description = "Add or update a file in a GitHub repo and commit it."
    parameters_class = AddCommitFileSchema

    def run(self, owner: str, repo: str, path: str, content: str, message: str, branch: str = "main") -> Any:
        token = self.get_secret("GITHUB_TOKEN")
        return client.add_and_commit_file(token, owner, repo, path, content, message, branch)


# 7. Create Pull Request (auth)
class CreateGitHubPullRequest(Tool):
    name = "create_github_pull_request"
    description = "Create a pull request from a feature branch."
    parameters_class = PullRequestSchema

    def run(self, owner: str, repo: str, head_branch: str, base_branch: str, title: str, body: str = "") -> Any:
        token = self.get_secret("GITHUB_TOKEN")
        return client.create_pull_request(token, owner, repo, head_branch, base_branch, title, body)