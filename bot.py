import requests
import json
import time
import threading
from datetime import datetime, timedelta

# Configuration
API_BASE_URL = "https://owdragon.oasisworld.io/api"
FEED_INTERVAL_HOURS = 12

class OasisWorldBot:
    def __init__(self, auth_method, auth_data):
        self.auth_method = auth_method  # 'query' or 'token'
        self.auth_data = auth_data
        self.jwt = None
        self.address = None
        self.power = None
        self.balance = None
        self.last_feed_time = None
        self.running = False
        self.processed_missions = set()
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
            "Origin": "https://owdragon.oasisworld.io",
            "Referer": "https://owdragon.oasisworld.io/?startapp=1467975528"
        }
        
    def authenticate(self):
        if self.auth_method == 'query':
            return self.auth_with_query()
        elif self.auth_method == 'token':
            return self.auth_with_token()
        else:
            print("Invalid authentication method")
            return False
    
    def auth_with_query(self):
        try:
            payload = {
                "init_data": self.auth_data,
                "referral_code": ""
            }
            
            response = requests.post(
                f"{API_BASE_URL}/auth/telegram",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    self.jwt = data["data"]["jwt"]
                    self.headers["Authorization"] = f"Bearer {self.jwt}"
                    print("Authentication successful")
                    return True
                else:
                    print(f"Authentication failed: {data.get('message')}")
                    return False
            else:
                print(f"Authentication failed with status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error during authentication: {str(e)}")
            return False
    
    def auth_with_token(self):
        self.jwt = self.auth_data
        self.headers["Authorization"] = f"Bearer {self.jwt}"
        print("Using provided JWT token")
        return True
    
    def get_address(self):
        try:
            response = requests.post(
                f"{API_BASE_URL}/get-address",
                headers=self.headers,
                json={"jwt": self.jwt},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    self.address = data["data"]["address"]
                    print(f"Address: {self.address}")
                    return True
                else:
                    print(f"Failed to get address: {data.get('message')}")
            else:
                print(f"Failed to get address with status code: {response.status_code}")
            return False
                
        except Exception as e:
            print(f"Error getting address: {str(e)}")
            return False
    
    def get_power(self):
        try:
            response = requests.post(
                f"{API_BASE_URL}/get-power",
                headers=self.headers,
                json={"jwt": self.jwt},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    self.power = data["data"]["power"]
                    print(f"Power: {self.power}")
                    return True
                else:
                    print(f"Failed to get power: {data.get('message')}")
            else:
                print(f"Failed to get power with status code: {response.status_code}")
            return False
                
        except Exception as e:
            print(f"Error getting power: {str(e)}")
            return False
    
    def get_balance(self):
        try:
            response = requests.post(
                f"{API_BASE_URL}/get-balance",
                headers=self.headers,
                json={"jwt": self.jwt},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    self.balance = data["data"]["balance"]
                    print(f"Balance: {self.balance}")
                    return True
                else:
                    print(f"Failed to get balance: {data.get('message')}")
            else:
                print(f"Failed to get balance with status code: {response.status_code}")
            return False
                
        except Exception as e:
            print(f"Error getting balance: {str(e)}")
            return False
    
    def feed(self):
        try:
            response = requests.post(
                f"{API_BASE_URL}/feed",
                headers=self.headers,
                json={"jwt": self.jwt},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    reward = data["data"]["reward"]
                    self.last_feed_time = datetime.now()
                    print(f"Feed successful! Reward: {reward}")
                    return True
                else:
                    print(f"Failed to feed: {data.get('message')}")
            else:
                print(f"Failed to feed with status code: {response.status_code}")
            return False
                
        except Exception as e:
            print(f"Error during feeding: {str(e)}")
            return False
    
    def clear_missions(self):
        try:
            # Use mission-specific headers
            mission_headers = self.headers.copy()
            mission_headers["Referer"] = "https://owdragon.oasisworld.io/missions"
            
            # Process social missions
            social_missions = self.get_missions("social", mission_headers)
            for mission in social_missions:
                if mission["user_mission_id"] not in self.processed_missions and mission["status"] == 0:
                    print(f"Processing social mission: {mission['title']}")
                    
                    # For social missions, we need to submit before finishing
                    if self.submit_mission(mission["user_mission_id"], "social", mission_headers):
                        print("Mission submitted successfully")
                        time.sleep(1)  # Short delay
                        if self.finish_mission(mission["user_mission_id"], "social", mission_headers):
                            self.processed_missions.add(mission["user_mission_id"])
                            print("Mission finished successfully")
            
            # Process daily missions
            daily_missions = self.get_missions("daily", mission_headers)
            for mission in daily_missions:
                if mission["user_mission_id"] not in self.processed_missions and mission["status"] == 0:
                    print(f"Processing daily mission: {mission['title']}")
                    
                    # For daily login mission, submit with random value
                    if "Login and play the game" in mission["title"]:
                        if self.submit_mission(mission["user_mission_id"], "daily", mission_headers, "auto_"+str(int(time.time()))):
                            print("Daily login mission submitted")
                    
                    time.sleep(1)  # Short delay
                    if self.finish_mission(mission["user_mission_id"], "daily", mission_headers):
                        self.processed_missions.add(mission["user_mission_id"])
                        print("Mission finished successfully")
            
            return True
                
        except Exception as e:
            print(f"Error clearing missions: {str(e)}")
            return False
    
    def get_missions(self, mission_type, headers):
        try:
            response = requests.post(
                f"{API_BASE_URL}/query-mission",
                headers=headers,
                json={
                    "jwt": self.jwt,
                    "query": mission_type
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    return data.get("data", [])
                else:
                    print(f"Failed to get {mission_type} missions: {data.get('message')}")
            else:
                print(f"Failed to get {mission_type} missions with status code: {response.status_code}")
            return []
                
        except Exception as e:
            print(f"Error getting {mission_type} missions: {str(e)}")
            return []
    
    def submit_mission(self, mission_id, tab, headers, value="bb123456"):
        try:
            payload = {
                "jwt": self.jwt,
                "mission_id": mission_id,
                "tab": tab,
                "value": value
            }
            
            response = requests.post(
                f"{API_BASE_URL}/submit-mission",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    return True
                else:
                    print(f"Failed to submit mission: {data.get('message')}")
            else:
                print(f"Failed to submit mission with status code: {response.status_code}")
            return False
                
        except Exception as e:
            print(f"Error submitting mission: {str(e)}")
            return False
    
    def finish_mission(self, mission_id, tab, headers):
        try:
            response = requests.post(
                f"{API_BASE_URL}/finish-mission",
                headers=headers,
                json={
                    "jwt": self.jwt,
                    "mission_id": mission_id,
                    "tab": tab
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    return True
                else:
                    print(f"Failed to finish mission: {data.get('message')}")
            else:
                print(f"Failed to finish mission with status code: {response.status_code}")
            return False
                
        except Exception as e:
            print(f"Error finishing mission: {str(e)}")
            return False
    
    def run(self):
        self.running = True
        
        # Initial authentication and setup
        if not self.authenticate():
            print("Initial authentication failed")
            self.running = False
            return
            
        self.get_address()
        self.get_power()
        self.get_balance()
        
        # Initial feed and mission clear
        self.feed()
        self.clear_missions()
        
        # Schedule periodic operations
        while self.running:
            now = datetime.now()
            next_feed_time = self.last_feed_time + timedelta(hours=FEED_INTERVAL_HOURS) if self.last_feed_time else now
            
            if now >= next_feed_time:
                self.feed()
                self.clear_missions()
                
                # Update account info periodically
                self.get_power()
                self.get_balance()
            
            # Sleep for 1 minute before checking again
            time.sleep(60)
    
    def stop(self):
        self.running = False

def load_accounts():
    query_accounts = []
    token_accounts = []
    
    try:
        with open("data.txt", "r") as f:
            query_accounts = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("data.txt not found - no query accounts loaded")
    
    try:
        with open("token.txt", "r") as f:
            token_accounts = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("token.txt not found - no token accounts loaded")
    
    return query_accounts, token_accounts

def main():
    query_accounts, token_accounts = load_accounts()
    bots = []
    
    # Create bots for query accounts
    for query in query_accounts:
        bot = OasisWorldBot("query", query)
        bots.append(bot)
    
    # Create bots for token accounts
    for token in token_accounts:
        bot = OasisWorldBot("token", token)
        bots.append(bot)
    
    if not bots:
        print("No accounts found in data.txt or token.txt")
        return
    
    # Start all bots in separate threads
    threads = []
    for bot in bots:
        thread = threading.Thread(target=bot.run)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all bots...")
        for bot in bots:
            bot.stop()
        
        for thread in threads:
            thread.join()
        
        print("All bots stopped")

if __name__ == "__main__":
    main()