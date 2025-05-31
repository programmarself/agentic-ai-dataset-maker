from github import Github

def push_to_github(repo_name, file_name, content, token):
    g = Github(token)
    try:
        repo = g.get_repo(repo_name)
        repo.create_file(file_name, "Add dataset", content, branch="main")
        return "✅ Dataset pushed to GitHub!"
    except Exception as e:
        return f"❌ Error: {str(e)}"