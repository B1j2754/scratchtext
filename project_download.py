"""
Script for downloading an existing Scratch project's JSON
"""

import requests
import json

def get_token(project_id):
    # GET request to Scratch API, to get access token
    api_url = f"https://api.scratch.mit.edu/projects/{project_id}"
    response = requests.get(api_url)

    if response.status_code == 200:
        project_data = response.json()
        project_token = project_data.get("project_token")

        return project_token
    
    else:
        print(f"https://scratch.mit.edu/projects/{project_id} either doesn't exist, or is unshared")

def get_url(project_id, project_token):
    # Create access link
    project_url = f"https://projects.scratch.mit.edu/{project_id}?token={project_token}"
    return project_url

def get_json(project_url):
    print(project_url)
    # Make GET request to access link and download JSON code
    response = requests.get(project_url)

    if response.status_code == 200:
        project_json = response.json()
        return project_json

def download_project(project_id):
    project_token = get_token(project_id)

    if project_token:
        project_url = get_url(project_id, project_token)
        project_json = get_json(project_url)

        # print(project_json)

        if project_json:
            print(f"Downloaded json of project: {project_id}")
            with open('downloaded.json', 'w') as json_file:
                json.dump(project_json, json_file)

download_project("1032156423")