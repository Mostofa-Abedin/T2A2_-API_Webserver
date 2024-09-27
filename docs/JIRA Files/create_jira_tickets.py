import requests
import json
import base64

# Function to get the API token from the file
def get_api_token(file_path):
    with open(file_path, 'r') as file:
        # Assuming the token is the only content in the file
        api_token = file.readline().strip()
    return api_token

# JIRA credentials
JIRA_URL = 'https://startup-mostofa.atlassian.net'
API_ENDPOINT = f'{JIRA_URL}/rest/api/2/issue'
USERNAME = 'abedin.online.trading@gmail.com'

# Path to the API token file
API_TOKEN_FILE = 'My_Personal_API_key.md'

# Fetch the API token from the file
API_TOKEN = get_api_token(API_TOKEN_FILE)

# Manually encode the credentials
auth_str = f"{USERNAME}:{API_TOKEN}"
auth_bytes = auth_str.encode('utf-8')
auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

# Authentication headers
headers = {
    "Authorization": f"Basic {auth_base64}",
    "Content-Type": "application/json"
}

# List of JSON files to process
json_files = [
    'sprint1_tickets.json'
    'sprint2_tickets.json'
]

# Loop through each JSON file and create tickets
for json_file in json_files:
    with open(json_file) as file:
        tickets_data = json.load(file)
    
    # Create tickets for each file
    for ticket in tickets_data['tickets']:
        # Adjust labels if necessary (e.g., ensure no spaces)
        if 'labels' in ticket['fields']:
            # Remove spaces from labels
            ticket['fields']['labels'] = [label.replace(' ', '_') for label in ticket['fields']['labels']]
        
        try:
            response = requests.post(API_ENDPOINT, headers=headers, json=ticket)
            if response.status_code == 201:
                print(f"Ticket created successfully: {response.json()['key']}")
            else:
                # Detailed error logging
                print(f"Failed to create ticket: {ticket['fields'].get('summary', 'Unknown Summary')} - {response.status_code} - {response.text}")
        except Exception as e:
            # Catch any other exceptions
            print(f"An error occurred while creating ticket: {ticket['fields'].get('summary', 'Unknown Summary')} - {str(e)}")
