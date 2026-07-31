import asyncio
import random
import os
import http.server
import socketserver
import threading
import sys
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

# ১. কি-ওয়ার্ড লিস্ট
KEYWORDS = [
    "Latest technology news 2026", "Python Playwright tutorial", "ESP32 robotics ideas",
    "Cricket world cup updates", "Best budget laptops", "AI development trends",
    "SpaceX launch schedule", "Web automation tips", "Arduino home automation"
]

# ২. ডামি সার্ভার ফাংশন (Render Port Binding এর জন্য)
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            return

    try:
        print(f"[+] Starting Web Server on port {port} for Render...", flush=True)
        with socketserver.TCPServer(("", port), QuietHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"[-] Server Error: {e}", flush=True)

# ৩. মেইন অটোমেশন লজিক
async def run_bot():
    print("[+] Starting Rewards Automation Bot...", flush=True)
    
    email = os.environ.get("nasibahanab@gmail.com")
    password = os.environ.get("9414Nasib")

    if not email or not password:
        print("[-] WARNING: Environment variables MS_EMAIL or MS_PASSWORD are missing!", flush=True)

    async with async_playwright() as p:
        try:
            print("[+] Launching Chromium Browser...", flush=True)
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled'
                ]
            )
            
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                viewport={'width': 1366, 'height': 768}
            )
            
            page = await context.new_page()
            await stealth_async(page)
            page.set_default_timeout(20000)

            # --- স্টেপ ১: লগইন হ্যান্ডলিং (টাইমাউট বাড়িয়ে ৬০ সেকেন্ড করা হয়েছে) ---
            if email and password:
                print(f"[+] Attempting Login for: {email}", flush=True)
                try:
                    # ৬০ সেকেন্ড টাইমাউট যাতে স্লো নেটওয়ার্কেও লোড হতে পারে
                    await page.goto("https://login.live.com", wait_until="domcontentloaded", timeout=60000)
                    await asyncio.sleep(3)

                    # ইমেইল ইনপুট
                    await page.wait_for_selector('input[type="email"]', timeout=30000)
                    await page.fill('input[type="email"]', email)
                    await page.click('input[type="submit"]')
                    await asyncio.sleep(4)

                    # পাসওয়ার্ড ইনপুট
                    await page.wait_for_selector('input[type="password"]', timeout=30000)
                    await page.fill('input[type="password"]', password)
                    await page.click('input[type="submit"]')
                    await asyncio.sleep(5)

                    # "Stay signed in?" এর পপ-আপ হ্যান্ডলিং
                    try:
                        await page.click('input[id="idSIButton9"]', timeout=5000)
                    except:
                        pass

                    print("[+] Login sequence completed successfully!", flush=True)
                except Exception as e:
                    print(f"[-] Login encountered an issue (Continuing anyway): {e}", flush=True)

            # --- স্টেপ ২: সার্চ অ্যান্ড পয়েন্ট কালেকশন ---
            print("[+] Starting Bing Searches...", flush=True)
            search_keywords = KEYWORDS.copy()
            random.shuffle(search_keywords)

            success_count = 0
            for i, word in enumerate(search_keywords[:10]):
                print(f"[{i+1}/10] Searching: '{word}'", flush=True)
                try:
                    search_url = f"https://www.bing.com/search?q={word.replace(' ', '+')}"
                    await page.goto(search_url, wait_until="domcontentloaded", timeout=20000)

                    delay = random.randint(8, 14)
                    print(f"    Waiting {delay} seconds...", flush=True)
                    await asyncio.sleep(delay)
                    success_count += 1
                except Exception as e:
                    print(f"    [-] Search error on '{word}': {e}", flush=True)

            print(f"[+] Task Finished! Successfully completed {success_count}/10 searches.", flush=True)

        except Exception as global_error:
            print(f"[-] Critical Error during automation: {global_error}", flush=True)
        finally:
            try:
                await browser.close()
                print("[+] Browser closed cleanly.", flush=True)
            except:
                pass

def start_bot_thread():
    import time
    time.sleep(2)
    asyncio.run(run_bot())

if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_bot_thread, daemon=True)
    bot_thread.start()

    run_dummy_server()
