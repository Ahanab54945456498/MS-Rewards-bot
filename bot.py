import asyncio
import random
import os
import http.server
import socketserver
import threading
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"[+] Dummy Web Server listening on port {port}")
        httpd.serve_forever()

KEYWORDS = [
    "Latest technology news 2026", "Python Playwright tutorial", "ESP32 robotics ideas",
    "Cricket world cup updates", "Best budget laptops", "AI development trends",
    "SpaceX launch schedule", "Web automation tips", "Arduino home automation"
]

async def run_bot():
    email = os.environ.get("MS_EMAIL")
    password = os.environ.get("MS_PASSWORD")

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
            print("[+] Logging into Microsoft Account...")
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
                
                print("[+] Login Step Completed!")
            except Exception as e:
                print(f"[-] Login step skipped/failed: {e}")

        # ২. সরাসরি সার্চ ইউআরএল দিয়ে পয়েন্ট কালেকশন (যাতে টাইমাউট না হয়)
        print("[+] Starting Bing Searches...")
        random.shuffle(KEYWORDS)
        
        for i, word in enumerate(KEYWORDS[:10]):
            print(f"[{i+1}/10] Searching: '{word}'")
            try:
                # সরাসরি Bing Search URL এ যাওয়া (কোনো বক্সে ক্লিক করার ঝামেলা নেই)
                search_url = f"https://www.bing.com/search?q={word.replace(' ', '+')}"
                await page.goto(search_url, wait_until="domcontentloaded")
                
                delay = random.randint(8, 15)
                print(f"    Waiting {delay}s...")
                await asyncio.sleep(delay)
            except Exception as e:
                print(f"[-] Search error: {e}")

        print("[+] Automation Completed Successfully!")
        await browser.close()

if __name__ == "__main__":
    threading.Thread(target=lambda: asyncio.run(run_bot()), daemon=True).start()
    run_dummy_server()
