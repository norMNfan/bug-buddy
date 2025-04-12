from .github_client import GitHubClient

class GitHubClientManager:
    _client: GitHubClient = None

    @classmethod
    def initialize(cls, token: str, username: str):
        cls._client = GitHubClient(token=token, username=username)

    @classmethod
    def get_client(cls) -> GitHubClient:
        if cls._client is None:
            raise RuntimeError("GitHub client has not been initialized. Please run InitializeGitHubClient first.")
        return cls._client
