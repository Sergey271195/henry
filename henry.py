import sys
import requests
import json

def say_hello():
    print("Hello, I am Henry. I can try to help you!")

def get_github_credentials():
    credentials = {}
    with open("settings.txt") as credentials_file:
        credentials["username"] = credentials_file.readline().strip()
        credentials["password"] = credentials_file.readline().strip()
        credentials["token"] = credentials_file.readline().strip()
    return credentials

def get_headers():
    token = get_github_credentials()["token"]
    return {
        "Authorization": "token " + token,
        "Accept": "application/vnd.github.v3+json"
    }

def create_repo(repo_name):
    request = requests.post("https://api.github.com/user/repos", headers = get_headers(), json = {"name": repo_name})
    response_json = request.json()
    if request.status_code == 201:
        print(f"Successfully created repository '{repo_name}'")
    elif request.status_code == 422:
        print(f"Repository with '{repo_name}' name already exists")
    else:
        print(response_json["errors"][0]["message"])

def delete_repo(repo_name):
    credentials = get_github_credentials()
    owner = credentials["username"]
    request = requests.delete(f"https://api.github.com/repos/{owner}/{repo_name}", headers = get_headers())
    if request.status_code == 204:
        print(f"Successfully deleted '{repo_name}' repository")
    elif request.status_code == 404:
        print(f"Repository '{repo_name}' doesn't exist")

def get_repos():
    request = requests.get("https://api.github.com/user/repos", headers = get_headers())
    response_json = request.json()
    for item in list(map(lambda x: x["name"], response_json)):
        print(item)
    #print(response_json)

def parse_command_line_arguments():
    actual_arguments = sys.argv[1:]
    args_length = len(actual_arguments)
    if (args_length == 0):
        say_hello()
    elif args_length == 2:
        if actual_arguments[0] == "get" and actual_arguments[1] == "repos":
            get_repos()
    elif args_length == 3:
        if actual_arguments[0] == "create" and actual_arguments[1] == "repo":
            create_repo(actual_arguments[2])
        elif actual_arguments[0] == "delete" and actual_arguments[1] == "repo":
            delete_repo(actual_arguments[2])

if __name__ == "__main__":
    parse_command_line_arguments()