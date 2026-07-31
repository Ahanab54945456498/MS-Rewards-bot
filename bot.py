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
            # স্প্যাম লগার বন্ধ করার জন্য
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
    
    email = os.environ.get("MS_EMAIL")
    password = os.environ.get("MS_PASSWORD")

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
            page.set_default_timeout(15000) # ১৫ সেকেন্ড অটোমেটিক টাইমাউট

            # --- স্টেপ ১: লগইন হ্যান্ডলিং ---
            if email and password:
                print(f"[+] Attempting Login for: {email}", flush=True)
                try:
                    await page.goto("https://login.live.com", wait_until="domcontentloaded", timeout=20000)
                    await asyncio.sleep(2)

                    # ইমেইল ইনপুট
                    await page.fill('input[type="email"]', email)
                    await page.click('input[type="submit"]')
                    await asyncio.sleep(3)

                    # পাসওয়ার্ড ইনপুট
                    await page.fill('input[type="password"]', password)
                    await page.click('input[type="submit"]')
                    await asyncio.sleep(4)

                    # "Stay signed in?" এর পপ-আপ হ্যান্ডলিং
                    try:
                        await page.click('input[id="idSIButton9"]', timeout=3000)
                    except:
                        pass

                    print("[+] Login sequence completed!", flush=True)
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
                    # ইউআরএল সরাসরি নেভিগেট করা (ইনপুট বক্সে না টাইপ করে)
                    search_url = f"https://www.bing.com/search?q={word.replace(' ', '+')}"
                    await page.goto(search_url, wait_until="domcontentloaded", timeout=15000)

                    # র‍্যান্ডম ডিলে দেওয়া যাতে বট ডিটেক্ট না করে
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
    # ২ সেকেন্ড বিরতি দিয়ে ব্যাকগ্রাউন্ড থ্রেডে বটের কাজ শুরু করা
    import time
    time.sleep(2)
    asyncio.run(run_bot())

if __name__ == "__main__":
    # ১. ব্যাকগ্রাউন্ড থ্রেডে বট চালু
    bot_thread = threading.Thread(target=start_bot_thread, daemon=True)
    bot_thread.start()

    # ২. মূল থ্রেডে সার্ভার সচল রাখা
    run_dummy_server()
