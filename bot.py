import base64
import json
import os
import random
import time
from urllib.parse import parse_qs, unquote
import requests
from datetime import datetime, timedelta

# Color constants for traffic light-like outputs
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RESET = '\033[0m'  # Reset color

def print_(word, color=RESET, end='\n'):
    """Print with color formatting without timestamp."""
    print(f"{color}{word}{RESET}", end=end)

def clear_terminal():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Display the Shadow Scripters banner."""
    banner = """
   ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗
   ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║
   ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║
   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║
   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝
   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ 
   ███████╗ ██████╗██████╗ ██╗██████╗ ████████╗███████╗
   ██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝██╔════╝
   ███████╗██║     ██████╔╝██║██████╔╝   ██║   ███████╗
   ╚════██║██║     ██╔══██╗██║██╔═══╝    ██║   ╚════██║
   ███████║╚██████╗██║  ██║██║██║        ██║   ███████║
   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   ╚══════╝
    """
    print_(banner, color=GREEN)
    print_(f"Shadow Scripters Bot", color=YELLOW)
    print_(f"Telegram: https://t.me/shadowscripters\n", color=YELLOW)

# Load queries from data.txt
def load_query():
    try:
        with open('data.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print_("File data.txt not found.", color=RED)
        return []
    except Exception as e:
        print_(f"Failed to get queries: {str(e)}", color=RED)
        return []

# Load tasks from task.json
def load_task():
    try:
        with open("task.json", 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print_(f"Error loading tasks: {str(e)}", color=RED)
        return []

# Parse the user query string
def parse_query(query: str):
    try:
        parsed_query = parse_qs(query)
        parsed_query = {k: v[0] for k, v in parsed_query.items()}
        user_data = json.loads(unquote(parsed_query['user']))
        parsed_query['user'] = user_data
        return parsed_query
    except Exception as e:
        print_(f"Error parsing query: {str(e)}", color=RED)
        return {}

# Make HTTP requests with automatic retry for failures
def make_request(method, url, headers, json=None, params=None, data=None):
    retry_count = 0
    while True:
        time.sleep(2)  # Delay between retries
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params or json)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=json, data=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=json, data=data)
        else:
            raise ValueError("Invalid method.")
        
        if response.status_code >= 500:
            if retry_count >= 4:
                print_(f"Status Code: {response.status_code} | Server Down", color=RED)
                return None
            retry_count += 1
        elif response.status_code >= 400:
            print_(f"Status Code: {response.status_code} | Request Failed", color=RED)
            return None
        elif response.status_code >= 200:
            return response.json()

# Handle login and API token retrieval
def login(query):
    url = 'https://coub.com/api/v2/sessions/login_mini_app'
    headers = {
        "Accept": "application/json, */*",
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = make_request('POST', url, headers, data=query)
    if response:
        print_("Token successfully retrieved.", color=GREEN)
        api_token = response.get('api_token', "")
        return get_token(api_token)
    return None

# Get API access token
def get_token(api_token):
    url = 'https://coub.com/api/v2/torus/token'
    headers = {
        "Accept": "application/json, */*",
        "User-Agent": "Mozilla/5.0",
        "x-auth-token": api_token
    }
    response = make_request('POST', url, headers)
    if response:
        print_(f"Token created successfully, valid for {response.get('expires_in', 0) // 3600} hours.", color=GREEN)
        return response.get('access_token', "")
    return None

# Retrieve rewards for a user
def get_rewards(token):
    url = "https://rewards.coub.com/api/v2/get_user_rewards"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, */*",
        "User-Agent": "Mozilla/5.0",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print_(f"Failed to retrieve rewards. Status code: {response.status_code}", color=RED)
        return None

# Claim a specific task
def claim_task(token, task_id, task_title):
    url = "https://rewards.coub.com/api/v2/complete_task"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, */*",
        "User-Agent": "Mozilla/5.0",
    }
    params = {"task_reward_id": task_id}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        print_(f"Task {task_title} completed.", color=GREEN)
        return response.json()
    else:
        print_(f"Task {task_title} failed. Status code: {response.status_code}", color=RED)
        return None

# Countdown function for 1 day (24 hours) with real-time update (stays in one line)
def countdown_timer(duration_in_seconds):
    while duration_in_seconds:
        hours, remainder = divmod(duration_in_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"Time remaining: {int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        print_(time_str, color=YELLOW, end='\r')  # Overwrites the same line
        time.sleep(1)
        duration_in_seconds -= 1
    print()  # Move to the next line when countdown finishes

# Main process loop
def main():
    print_banner()  # Display the Shadow Scripters banner
    while True:
        try:
            queries = load_query()
            tasks = load_task()
            total_queries = len(queries)
            delay_between_accounts = 5  # 5 seconds delay between accounts
            
            start_time = time.time()
            print_(f"Total accounts found: {total_queries}", color=YELLOW)
            
            for index, query in enumerate(queries, start=1):
                list_id = []
                user = parse_query(query).get('user', {})
                username = user.get('username', '')
                
                print_(f"====== Processing account {index}/{total_queries} | {username} ======", color=YELLOW)
                
                token = login(query)
                if not token:
                    print_(f"Failed to get token for {username}. Moving to next account...", color=RED)
                    continue
                
                data_reward = get_rewards(token=token)
                if not data_reward:
                    print_(f"No rewards found for {username}.", color=YELLOW)
                    continue
                
                for data in data_reward:
                    reward_id = data.get('id', 0)
                    if reward_id not in [2, 12, 13, 15, 16, 19]:
                        list_id.append(reward_id)
                
                for task in tasks:
                    task_id = task.get('id')
                    task_title = task.get('title')
                    
                    if task_id in list_id:
                        print_(f"{task_title} already completed...", color=GREEN)
                    else:
                        try:
                            time.sleep(2)
                            print_(f"Starting task: {task_title}...", color=YELLOW)
                            claim_task(token, task_id, task_title)
                        except Exception as e:
                            print_(f"Failed to process task {task_title}: {str(e)}", color=RED)
                
                # 5 second delay between accounts
                print_(f"Waiting 5 seconds before processing next account...", color=YELLOW)
                time.sleep(delay_between_accounts)
            
            # After all accounts are processed, start 24-hour countdown
            print_(f"All accounts have been processed. Starting 24-hour countdown...", color=YELLOW)
            countdown_timer(86400)  # 86400 seconds = 24 hours

            # Repeat process after 24 hours
            clear_terminal()  # Clear screen before restarting
            print_(f"Restarting process after 24 hours...", color=GREEN)

        except Exception as e:
            print_(f"Major error occurred: {str(e)}. Continuing with other tasks...", color=RED)

if __name__ == "__main__":
    main()
