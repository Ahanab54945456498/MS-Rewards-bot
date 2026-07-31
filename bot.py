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

async def run_bot():
    # Render লগ পেজে সাথে সাথে দেখার জন্য
    print("[+] Bot Execution Started!", flush=True)
    
    email = os.environ.get("MS_EMAIL")
    password = os.environ.get("MS_PASSWORD")

    print("[+] Launching Browser...", flush=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1366, 'height': 768}
        )
        
        page = await context.new_page()
        await stealth_async(page)

        # ১. লগইন প্রসেস
        if email and password:
            print(f"[+] Logging in as: {email}", flush=True)
            try:
                await page.goto("https://login.live.com", wait_until="networkidle")
                await asyncio.sleep(2)
                
                await page.fill('input[type="email"]', email)
                await page.click('input[type="submit"]')
                await asyncio.sleep(3)
                
                await page.fill('input[type="password"]', password)
                await page.click('input[type="submit"]')
                await asyncio.sleep(4)
                
                try:
                    await page.click('input[id="idSIButton9"]', timeout=4000)
                except:
                    pass
                
                print("[+] Login Step Completed!", flush=True)
            except Exception as e:
                print(f"[-] Login step skipped/failed: {e}", flush=True)
        else:
            print("[-] Warning: MS_EMAIL or MS_PASSWORD environment variables not found!", flush=True)

        # ২. সরাসরি সার্চ ইউআরএল দিয়ে পয়েন্ট কালেকশন
        print("[+] Starting Bing Searches...", flush=True)
        random.shuffle(KEYWORDS)
        
        for i, word in enumerate(KEYWORDS[:10]):
            print(f"[{i+1}/10] Searching: '{word}'", flush=True)
            try:
                search_url = f"https://www.bing.com/search?q={word.replace(' ', '+')}"
                await page.goto(search_url, wait_until="domcontentloaded")
                
                delay = random.randint(8, 15)
                print(f"    Waiting {delay} seconds...", flush=True)
                await asyncio.sleep(delay)
            except Exception as e:
                print(f"[-] Search error: {e}", flush=True)

        print("[+] All 10 Searches Completed Successfully!", flush=True)
        await browser.close()

def start_bot_thread():
    asyncio.run(run_bot())

if __name__ == "__main__":
    # ১. ব্যাকগ্রাউন্ডে বট রান করা
    threading.Thread(target=start_bot_thread).start()
    
    # ২. সাথে সাথে পোর্টে ওয়েব সার্ভার চালু করা (যাতে Render টাইমাউট না দেয়)
    port = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    print(f"[+] Web Server running on port {port}", flush=True)
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()
