import requests
import json
import time
import random
import string
import uuid
import hashlib
from urllib.parse import quote, urlencode

banner = r"""                                                                                 
                         TikTok Username Changer v2.0 | @hymenic on Telegram | Patched Version
"""

class TikTokAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "com.ss.android.ugc.trill/300904 (Linux; U; Android 10; en_US; SM-G960F; Build/QP1A.190711.020; Cronet/TTNetVersion:5c404a0b 2022-08-24)",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "sdk-version": "2",
        })
        
        # Generate device IDs
        self.device_id = self.generate_device_id()
        self.iid = self.generate_iid()
        self.install_id = str(uuid.uuid4()).replace("-", "")
        self.openudid = self.generate_openudid()
        
    def generate_device_id(self):
        """Generate device ID."""
        return f"7{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
    
    def generate_iid(self):
        """Generate installation ID."""
        return str(random.randint(1000000000000000000, 9999999999999999999))
    
    def generate_openudid(self):
        """Generate OpenUDID."""
        return ''.join(random.choices('0123456789abcdef', k=16))
    
    def generate_common_params(self, include_user_info=False):
        """Generate common TikTok API parameters."""
        params = {
            "ac": "wifi",
            "aid": "1233",
            "app_language": "en",
            "app_name": "musical_ly",
            "app_version": "30.9.4",
            "build_number": "30.9.4",
            "carrier_region": "SA",
            "channel": "googleplay",
            "device_brand": "samsung",
            "device_id": self.device_id,
            "device_model": "SM-G960F",
            "device_platform": "android",
            "device_type": "SM-G960F",
            "iid": self.iid,
            "install_id": self.install_id,
            "language": "en",
            "locale": "en",
            "mcc_mnc": "42001",
            "openudid": self.openudid,
            "os_api": "29",
            "os_version": "10",
            "region": "SA",
            "ssmix": "a",
            "sys_region": "SA",
            "timezone_name": "Asia/Riyadh",
            "timezone_offset": "10800",
            "ts": str(int(time.time())),
            "version_code": "300904",
        }
        
        if include_user_info:
            params.update({
                "account_region": "SA",
                "current_region": "SA",
            })
            
        return params
    
    def generate_x_gorgon_simple(self):
        """Generate a simple X-Gorgon header (placeholder)."""
        timestamp = str(int(time.time()))
        random_str = ''.join(random.choices('0123456789abcdef', k=32))
        return f"0404c0c0{random_str}"
    
    def get_user_info(self, session_token):
        """Get user information using session token."""
        print(f"[+] Testing session token...")
        
        # Set the session token
        self.session.cookies.set('sessionid', session_token, domain='.tiktok.com')
        
        # First try a simpler endpoint
        url = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/commit/user/get/"
        
        params = self.generate_common_params(include_user_info=True)
        
        # Generate headers
        headers = {
            "X-Khronos": str(int(time.time())),
            "X-Gorgon": self.generate_x_gorgon_simple(),
            "x-tt-trace-id": f"00-{random.getrandbits(64):016x}-{random.getrandbits(32):08x}-01",
        }
        
        try:
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            print(f"[+] Response status: {response.status_code}")
            print(f"[+] Response length: {len(response.text)}")
            
            if response.status_code == 200 and response.text.strip():
                try:
                    data = response.json()
                    print(f"[+] JSON parsed successfully")
                    print(f"[+] Response keys: {list(data.keys())}")
                    
                    if data.get("status_code") == 0:
                        user_info = data.get("user", {})
                        username = user_info.get("unique_id", "Unknown")
                        user_id = user_info.get("uid", "")
                        sec_uid = user_info.get("sec_uid", "")
                        
                        print(f"[+] Login successful!")
                        print(f"[+] Username: @{username}")
                        print(f"[+] User ID: {user_id}")
                        
                        return {
                            "success": True,
                            "username": username,
                            "user_id": user_id,
                            "sec_uid": sec_uid,
                        }
                    else:
                        print(f"[-] API error: {data.get('status_msg', 'Unknown')}")
                except json.JSONDecodeError as e:
                    print(f"[-] JSON decode error: {e}")
                    print(f"[-] Response: {response.text[:200]}")
                    
                    # Try alternative parsing
                    if "unique_id" in response.text:
                        import re
                        username_match = re.search(r'"unique_id":"([^"]+)"', response.text)
                        if username_match:
                            username = username_match.group(1)
                            print(f"[+] Found username in text: {username}")
                            return {
                                "success": True,
                                "username": username,
                                "user_id": "",
                                "sec_uid": "",
                            }
            else:
                print(f"[-] Invalid response")
                
        except Exception as e:
            print(f"[-] Error: {e}")
        
        # If first method fails, try web API
        return self.get_user_info_web(session_token)
    
    def get_user_info_web(self, session_token):
        """Get user info using web API."""
        print("[+] Trying web API...")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": f"sessionid={session_token}",
            "Accept": "application/json",
        }
        
        try:
            response = requests.get(
                "https://www.tiktok.com/api/user/detail/",
                headers=headers,
                params={"uniqueId": "", "accountType": 1},
                timeout=10
            )
            
            print(f"[+] Web API status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("statusCode") == 0:
                        user_info = data.get("userInfo", {}).get("user", {})
                        username = user_info.get("uniqueId", "Unknown")
                        user_id = user_info.get("id", "")
                        
                        print(f"[+] Web API success!")
                        print(f"[+] Username: @{username}")
                        print(f"[+] User ID: {user_id}")
                        
                        return {
                            "success": True,
                            "username": username,
                            "user_id": user_id,
                            "sec_uid": user_info.get("secUid", ""),
                        }
                except:
                    pass
                    
        except Exception as e:
            print(f"[-] Web API error: {e}")
        
        return {"success": False}
    
    def change_username(self, new_username, user_id, sec_uid, session_token):
        """Change TikTok username."""
        print(f"[+] Attempting to change username to: {new_username}")
        
        # Method 1: Try web API first
        success, message = self.change_username_web(new_username, session_token)
        if success:
            return success, message
        
        # Method 2: Try mobile API
        return self.change_username_mobile(new_username, user_id, sec_uid)
    
    def change_username_web(self, new_username, session_token):
        """Change username using web API."""
        print("[+] Trying web API method...")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": f"sessionid={session_token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Referer": "https://www.tiktok.com/setting",
            "Origin": "https://www.tiktok.com",
        }
        
        data = {
            "unique_id": new_username,
            "account_type": "1",
        }
        
        try:
            response = requests.post(
                "https://www.tiktok.com/api/user/update/",
                headers=headers,
                data=data,
                timeout=15
            )
            
            print(f"[+] Web API change status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("statusCode") == 0:
                        return True, "Username changed successfully via web API!"
                    else:
                        return False, f"Web API error: {result.get('statusMsg', 'Unknown')}"
                except:
                    return False, "Could not parse web API response"
            else:
                return False, f"Web API HTTP error: {response.status_code}"
                
        except Exception as e:
            return False, f"Web API error: {str(e)}"
    
    def change_username_mobile(self, new_username, user_id, sec_uid):
        """Change username using mobile API."""
        print("[+] Trying mobile API method...")
        
        params = self.generate_common_params()
        if user_id:
            params["user_id"] = user_id
        if sec_uid:
            params["sec_user_id"] = sec_uid
        
        data = {
            "unique_id": new_username,
        }
        
        if user_id:
            data["user_id"] = user_id
        if sec_uid:
            data["sec_user_id"] = sec_uid
        
        url = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/commit/user/"
        
        headers = {
            "X-Khronos": str(int(time.time())),
            "X-Gorgon": self.generate_x_gorgon_simple(),
            "x-tt-trace-id": f"00-{random.getrandbits(64):016x}-{random.getrandbits(32):08x}-01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        
        try:
            response = self.session.post(url, params=params, data=data, headers=headers, timeout=15)
            print(f"[+] Mobile API response: {response.status_code}")
            print(f"[+] Response preview: {response.text[:200]}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("status_code") == 0:
                        return True, "Username changed successfully via mobile API!"
                    else:
                        return False, f"Mobile API error: {data.get('status_msg', 'Unknown')}"
                except:
                    # Check for success indicators in plain text
                    if "success" in response.text.lower() or "unique_id" in response.text:
                        return True, "Username change appears successful!"
                    return False, "Could not parse mobile API response"
            else:
                return False, f"Mobile API HTTP error: {response.status_code}"
                
        except Exception as e:
            return False, f"Mobile API error: {str(e)}"

def get_session_input():
    """Get session input from user."""
    print("\n" + "="*70)
    print("SESSION TOKEN INPUT")
    print("="*70)
    
    print("\nOptions:")
    print("1. Mobile app session token (from HTTP Canary/Packet Capture)")
    print("2. Web sessionid (from browser cookies)")
    print("3. I'll get it manually")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    if choice == "1" or choice == "2":
        token = input("\nPaste your session token: ").strip()
        if token:
            return token
    
    elif choice == "3":
        print("\nHow to get session token:")
        print("-"*40)
        print("For MOBILE (Android):")
        print("1. Install 'HTTP Canary' from Play Store")
        print("2. Start capture, open TikTok, stop capture")
        print("3. Find request to api.tiktokv.com")
        print("4. Look for 'sessionid' in request headers")
        print("\nFor WEB:")
        print("1. Login to TikTok.com in Chrome/Firefox")
        print("2. Press F12 → Application → Cookies")
        print("3. Find 'sessionid' (should be 100+ chars)")
        print("-"*40)
        
        token = input("\nNow paste your session token: ").strip()
        return token
    
    return None

def main():
    """Main function."""
    print(banner)
    time.sleep(2)
    
    # Get session token
    session_token = get_session_input()
    if not session_token:
        print("\n[-] No session token provided!")
        return
    
    print(f"\n[+] Token length: {len(session_token)} characters")
    print(f"[+] First 20 chars: {session_token[:20]}...")
    
    # Initialize API
    api = TikTokAPI()
    
    # Get user info
    print("\n[1] Verifying session and getting user info...")
    user_info = api.get_user_info(session_token)
    
    if not user_info["success"]:
        print("\n[-] Failed to verify session!")
        print("\nPossible reasons:")
        print("1. Session token is expired")
        print("2. Token is from wrong source (need mobile or web)")
        print("3. Account is restricted")
        print("4. Need to use VPN")
        return
    
    current_username = user_info["username"]
    user_id = user_info["user_id"]
    sec_uid = user_info["sec_uid"]
    
    print(f"\n[+] Current username: @{current_username}")
    print(f"[+] User ID: {user_id}")
    
    # Get new username
    print("\n" + "="*70)
    new_username = input("\nEnter NEW username (without @): ").strip()
    
    if not new_username:
        print("[-] No username provided!")
        return
    
    if new_username == current_username:
        print("[-] New username is the same as current!")
        return
    
    if len(new_username) < 4:
        print("[-] Username must be at least 4 characters!")
        return
    
    if len(new_username) > 24:
        print("[-] Username must be 24 characters or less!")
        return
    
    # Check if username contains only allowed characters
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.")
    if not all(c in allowed_chars for c in new_username):
        print("[-] Username can only contain letters, numbers, underscore, and period!")
        return
    
    # Confirm
    print(f"\n[+] You are about to change:")
    print(f"[+] From: @{current_username}")
    print(f"[+] To: @{new_username}")
    
    confirm = input("\nType 'CONFIRM' to proceed: ").strip().upper()
    if confirm != "CONFIRM":
        print("\n[-] Change cancelled!")
        return
    
    # Change username
    print(f"\n[2] Attempting to change username...")
    success, message = api.change_username(new_username, user_id, sec_uid, session_token)
    
    print(f"\n{'[+]' if success else '[-]'} {message}")
    
    if success:
        # Verify
        print(f"\n[3] Verifying change...")
        time.sleep(5)
        
        # Get updated user info
        updated_info = api.get_user_info(session_token)
        if updated_info["success"]:
            final_username = updated_info["username"]
            if final_username == new_username:
                print(f"[+] Verified! New username: @{final_username}")
            else:
                print(f"[-] Verification failed. Current username: @{final_username}")
        else:
            print("[-] Could not verify change")
    
    print("\n" + "="*70)
    print("\n[+] Script completed!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[-] Operation cancelled by user!")
    except Exception as e:
        print(f"\n[-] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPress Enter to exit...")
