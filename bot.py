import asyncio
import random
import os
import http.server
import socketserver
import threading
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

KEYWORDS = [
    "Latest technology news 2026", "Python Playwright tutorial", "ESP32 robotics ideas",
    "Cricket world cup updates", "Best budget laptops", "AI development trends",
    "SpaceX launch schedule", "Web automation tips", "Arduino home automation"
]

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

async def run_bot():
    print("[+] Starting Rewards Automation Bot...", flush=True)
    
    email = "Nasibahanab@gmail.com"
    password = "9414Nasib"

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

            # --- স্টেপ ১: ফাস্ট লগইন প্রসেস ---
            print(f"[+] Navigating to Bing Login: {email}", flush=True)
            try:
                # সরাসরি Bing-এর লগইন ইউআরএলে হিট করা
                login_url = "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1&rver=6.7.6643.0&wp=MBI_SSL&wreply=https%3a%2f%2fwww.bing.com%2f"
                await page.goto(login_url, wait_until="commit", timeout=20000)
                await asyncio.sleep(2)

                # ইমেইল ইনপুট
                if await page.query_selector('input[type="email"]'):
                    await page.fill('input[type="email"]', email)
                    await page.click('input[type="submit"]')
                    await asyncio.sleep(3)

                # পাসওয়ার্ড ইনপুট
                if await page.query_selector('input[type="password"]'):
                    await page.fill('input[type="password"]', password)
                    await page.click('input[type="submit"]')
                    await asyncio.sleep(3)

                # Stay signed in?
                try:
                    await page.click('input[id="idSIButton9"]', timeout=3000)
                except:
                    pass

                print("[+] Login Step Finished!", flush=True)
            except Exception as e:
                print(f"[-] Login skipped or failed: {e}", flush=True)

            # --- স্টেপ ২: সার্চ অ্যান্ড পয়েন্ট কালেকশন ---
            print("[+] Starting Bing Searches...", flush=True)
            search_keywords = KEYWORDS.copy()
            random.shuffle(search_keywords)

            success_count = 0
            for i, word in enumerate(search_keywords[:10]):
                print(f"[{i+1}/10] Searching: '{word}'", flush=True)
                try:
                    search_url = f"https://www.bing.com/search?q={word.replace(' ', '+')}"
                    await page.goto(search_url, wait_until="commit", timeout=12000)

                    delay = random.randint(6, 10)
                    print(f"    Waiting {delay} seconds...", flush=True)
                    await asyncio.sleep(delay)
                    success_count += 1
                except Exception as e:
                    print(f"    [-] Search error on '{word}': {e}", flush=True)

            print(f"[+] Task Finished! Successfully completed {success_count}/10 searches.", flush=True)

        except Exception as global_error:
            print(f"[-] Critical Error: {global_error}", flush=True)
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
