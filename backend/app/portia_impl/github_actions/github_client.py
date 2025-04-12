import requests
import base64

class GitHubClient:
    def __init__(self, token, username):
        """
        Initialize the GitHub client.

        :param token: GitHub personal access token
        :param username: Your GitHub username
        """
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.username = username
        self.token = token

    def list_repositories(self, user=None):
        """
        List repositories for a user or the authenticated account.
        """
        user = user or self.username
        url = f"{self.base_url}/users/{user}/repos"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return [repo['name'] for repo in response.json()]

    def list_files(self, owner, repo, path=""):
        """
        List files in a repository at a given path.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return [item['name'] for item in response.json()]

    def read_file(self, owner, repo, path):
        """
        Read a file's content from a repository.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        content = response.json()
        return base64.b64decode(content['content']).decode()

    def get_file_metadata_and_content(self, owner, repo, path):
        """
        Get file metadata and content.
        """
        owner = owner or self.username
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        content = base64.b64decode(data['content']).decode()
        return {
            "name": data['name'],
            "path": data['path'],
            "sha": data['sha'],
            "content": content
        }

    def create_issue(self, owner, repo, title, body=None):
        """
        Create an issue on a repository.
        """
        owner = owner or self.username
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        payload = {"title": title, "body": body}
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def add_and_commit_file(self, owner, repo, path, content, message, branch="main", base_branch="main"):
        """
        Add or update a file and commit it to a repository.
        """
        owner = owner or self.username
        branch_url = f"{self.base_url}/repos/{owner}/{repo}/git/ref/heads/{branch}"
        branch_response = requests.get(branch_url, headers=self.headers)

        if branch_response.status_code == 404:
            # Step 2: Get the SHA of the base branch
            base_ref_url = f"{self.base_url}/repos/{owner}/{repo}/git/ref/heads/{base_branch}"
            base_response = requests.get(base_ref_url, headers=self.headers)
            base_response.raise_for_status()
            base_sha = base_response.json()["object"]["sha"]

            # Step 3: Create the new branch from the base branch
            create_branch_payload = {
                "ref": f"refs/heads/{branch}",
                "sha": base_sha
            }

            create_response = requests.post(
                f"{self.base_url}/repos/{owner}/{repo}/git/refs",
                headers=self.headers,
                json=create_branch_payload
            )
            create_response.raise_for_status()

        # Check if file exists
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        get_response = requests.get(url, headers=self.headers, params={"ref": branch})
        file_exists = get_response.status_code == 200
        sha = get_response.json().get('sha') if file_exists else None

        encoded_content = base64.b64encode(content.encode()).decode()

        payload = {
            "message": message,
            "content": encoded_content,
            "branch": branch
        }

        if sha:
            payload["sha"] = sha

        response = requests.put(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def create_pull_request(self, owner, repo, head_branch, base_branch, title, body=None):
        """
        Create a pull request from head_branch to base_branch.
        """
        owner = owner or self.username
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        payload = {
            "title": title,
            "head": head_branch,
            "base": base_branch,
            "body": body or ""
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
