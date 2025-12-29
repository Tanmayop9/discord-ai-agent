from crewai_tools import tool
import requests
import dotenv
import os


dotenv.load_dotenv()
COMPOSIO_API_KEY = os.environ["COMPOSIO_API_KEY"]


@tool("Create GitHub Issue")
def create_github_issue(connectedAccountId: str, owner: str, repo: str, title: str, body: str | None = None, labels: list | None = None) -> str:
    """
        Create a new issue in a GitHub repository.

        :param required connectedAccountId: The ID of the connected account.
        :param required owner: Repository owner (username or organization).
        :param required repo: Repository name.
        :param required title: Issue title.
        :param optional body: Issue description/body.
        :param optional labels: List of label names to add to the issue.
    """

    print("\n\nCreating GitHub issue\n\n")

    url = "https://backend.composio.dev/api/v1/actions/github_create_issue/execute"

    input_data = {
        "owner": owner,
        "repo": repo,
        "title": title
    }

    if body is not None:
        input_data["body"] = body
    if labels is not None:
        input_data["labels"] = labels

    payload = {
        "connectedAccountId": connectedAccountId,
        "appName": "github",
        "input": input_data
    }

    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get("executed"):
        issue_data = response_json.get("response", {})
        issue_number = issue_data.get("number", "")
        issue_url = issue_data.get("html_url", "")
        return f"✅ Issue #{issue_number} created successfully!\n🔗 {issue_url}"
    else:
        if response_json.get("response", {}).get("error", {}).get("code") == 401:
            return "Your GitHub authentication credentials expired. Please re-authenticate using `!authenticate_github` command."
        return "❌ Something went wrong while creating the issue."


@tool("List GitHub Issues")
def list_github_issues(connectedAccountId: str, owner: str, repo: str, state: str = "open", max_results: int = 10) -> str:
    """
        List issues from a GitHub repository.

        :param required connectedAccountId: The ID of the connected account.
        :param required owner: Repository owner (username or organization).
        :param required repo: Repository name.
        :param optional state: Issue state - "open", "closed", or "all" (default: "open").
        :param optional max_results: Maximum number of issues to return (default: 10).
    """

    print("\n\nListing GitHub issues\n\n")

    url = "https://backend.composio.dev/api/v1/actions/github_list_issues/execute"

    input_data = {
        "owner": owner,
        "repo": repo,
        "state": state,
        "per_page": max_results
    }

    payload = {
        "connectedAccountId": connectedAccountId,
        "appName": "github",
        "input": input_data
    }

    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get("executed"):
        issues = response_json.get("response", [])
        if issues:
            issue_list = []
            for issue in issues[:max_results]:
                number = issue.get("number", "")
                title = issue.get("title", "No Title")
                state_emoji = "🟢" if issue.get("state") == "open" else "🔴"
                issue_list.append(f"{state_emoji} **#{number}:** {title}")
            return f"📋 **Issues in {owner}/{repo}:**\n" + "\n".join(issue_list)
        else:
            return f"No {state} issues found in {owner}/{repo}."
    else:
        if response_json.get("response", {}).get("error", {}).get("code") == 401:
            return "Your GitHub authentication credentials expired. Please re-authenticate using `!authenticate_github` command."
        return "❌ Something went wrong while listing issues."


@tool("Search GitHub Repositories")
def search_github_repos(connectedAccountId: str, query: str, max_results: int = 10) -> str:
    """
        Search for GitHub repositories.

        :param required connectedAccountId: The ID of the connected account.
        :param required query: Search query (e.g., "machine learning", "language:python stars:>1000").
        :param optional max_results: Maximum number of repositories to return (default: 10).
    """

    print("\n\nSearching GitHub repositories\n\n")

    url = "https://backend.composio.dev/api/v1/actions/github_search_repositories/execute"

    input_data = {
        "q": query,
        "per_page": max_results
    }

    payload = {
        "connectedAccountId": connectedAccountId,
        "appName": "github",
        "input": input_data
    }

    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get("executed"):
        repos = response_json.get("response", {}).get("items", [])
        if repos:
            repo_list = []
            for repo in repos[:max_results]:
                name = repo.get("full_name", "Unknown")
                description = repo.get("description", "No description")[:60]
                stars = repo.get("stargazers_count", 0)
                repo_list.append(f"⭐ **{name}** ({stars} stars)\n  {description}...")
            return "🔍 **Search Results:**\n\n" + "\n\n".join(repo_list)
        else:
            return "No repositories found matching your search."
    else:
        if response_json.get("response", {}).get("error", {}).get("code") == 401:
            return "Your GitHub authentication credentials expired. Please re-authenticate using `!authenticate_github` command."
        return "❌ Something went wrong while searching repositories."


@tool("Create Pull Request")
def create_pull_request(connectedAccountId: str, owner: str, repo: str, title: str, head: str, base: str, body: str | None = None) -> str:
    """
        Create a pull request in a GitHub repository.

        :param required connectedAccountId: The ID of the connected account.
        :param required owner: Repository owner (username or organization).
        :param required repo: Repository name.
        :param required title: Pull request title.
        :param required head: The name of the branch where your changes are implemented.
        :param required base: The name of the branch you want the changes pulled into.
        :param optional body: Pull request description.
    """

    print("\n\nCreating pull request\n\n")

    url = "https://backend.composio.dev/api/v1/actions/github_create_pull_request/execute"

    input_data = {
        "owner": owner,
        "repo": repo,
        "title": title,
        "head": head,
        "base": base
    }

    if body is not None:
        input_data["body"] = body

    payload = {
        "connectedAccountId": connectedAccountId,
        "appName": "github",
        "input": input_data
    }

    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get("executed"):
        pr_data = response_json.get("response", {})
        pr_number = pr_data.get("number", "")
        pr_url = pr_data.get("html_url", "")
        return f"✅ Pull request #{pr_number} created successfully!\n🔗 {pr_url}"
    else:
        if response_json.get("response", {}).get("error", {}).get("code") == 401:
            return "Your GitHub authentication credentials expired. Please re-authenticate using `!authenticate_github` command."
        return "❌ Something went wrong while creating the pull request."


@tool("Star GitHub Repository")
def star_repository(connectedAccountId: str, owner: str, repo: str) -> str:
    """
        Star a GitHub repository.

        :param required connectedAccountId: The ID of the connected account.
        :param required owner: Repository owner (username or organization).
        :param required repo: Repository name.
    """

    print("\n\nStarring repository\n\n")

    url = "https://backend.composio.dev/api/v1/actions/github_star_repository/execute"

    input_data = {
        "owner": owner,
        "repo": repo
    }

    payload = {
        "connectedAccountId": connectedAccountId,
        "appName": "github",
        "input": input_data
    }

    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get("executed"):
        return f"⭐ Successfully starred {owner}/{repo}!"
    else:
        if response_json.get("response", {}).get("error", {}).get("code") == 401:
            return "Your GitHub authentication credentials expired. Please re-authenticate using `!authenticate_github` command."
        return "❌ Something went wrong while starring the repository."
