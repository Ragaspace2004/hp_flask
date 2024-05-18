import flask
import requests
HONO_ENDPOINT_URL = "https://my-app.ragapriya-k2022cse.workers.dev"

def analyze_botnet_activity(ip_address):
    HIGH_REQUEST_THRESHOLD = 5 # Requests per minute
    LARGE_PAYLOAD_SIZE = 10# Size in bytes
    known_bot_user_agents = ["bot", "crawl", "spider", "scrape"]

    try:
        # Fetch request frequency per minute
        response = requests.get(f"{HONO_ENDPOINT_URL}/analyze/request-frequency-per-minute/{ip_address}")
        response.raise_for_status()
        request_data = response.json()
        print("frequency per minute",request_data['results'])

        # Fetch max payload size
        response = requests.get(f"{HONO_ENDPOINT_URL}/analyze/size-payload/{ip_address}")
        response.raise_for_status()
        payload_data = response.json()
        print("payload gen",payload_data['results'])

        # Fetch user-agent data
        # Fetch user-agent data
        username = "your_username"  # replace with the actual username
        response = requests.get(f"{HONO_ENDPOINT_URL}/analyze/user-agent/{username}")
        response.raise_for_status()
        user_agent_data = response.json()
        print(user_agent_data['results'])
        # Analyze request frequency
        high_request_count = any(entry['request_count'] > HIGH_REQUEST_THRESHOLD for entry in request_data['results'])

        # Analyze payload size
        max_payload_size = payload_data['results'][0]['max_payload'] if payload_data['results'] else 0

        # Analyze user agents
        bot_user_agents = [ua['user_agent'] for ua in user_agent_data['results'] if any(bot in ua['user_agent'].lower() for bot in known_bot_user_agents)]

        if high_request_count:
            return True, "High request frequency detected"
        if max_payload_size > LARGE_PAYLOAD_SIZE:
            return True, "Unusually large payload size detected"
        if bot_user_agents:
            return True, f"Known botnet user-agent pattern detected: {bot_user_agents[0]}"

        return False, "No botnet activity detected"

    except requests.exceptions.RequestException as e:
        print(f"Error analyzing botnet activity: {e}")
        return False, "Error analyzing botnet activity"
    
analyze_botnet_activity("127.0.0.1")