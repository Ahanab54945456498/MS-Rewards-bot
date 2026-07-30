import asyncio
import random
import os
import http.server
import socketserver
import threading
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

# Render Web Service Port Binding
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

        # ১. মাইক্রোসফট লগইন পেজে যাওয়া
        if email and password:
            print("[+] Logging into Microsoft Account...")
            try:
                await page.goto("https://login.live.com")
                await asyncio.sleep(3)
                
                # Email Input
                await page.fill('input[type="email"]', email)
                await page.click('input[type="submit"]')
                await asyncio.sleep(3)
                
                # Password Input
                await page.fill('input[type="password"]', password)
                await page.click('input[type="submit"]')
                await asyncio.sleep(4)
                
                # "Stay signed in?" prompt handle
                try:
                    await page.click('input[id="idSIButton9"]', timeout=5000)
                except:
                    pass
                
                print("[+] Login Attempt Completed!")
            except Exception as e:
                print(f"[-] Login failed: {e}")

        # ২. সার্চ শুরু করা
        print("[+] Navigating to Bing...")
        await page.goto("https://www.bing.com")
        await asyncio.sleep(5)

        random.shuffle(KEYWORDS)
        for i, word in enumerate(KEYWORDS[:10]):
            print(f"[{i+1}/10] Searching: '{word}'")
            try:
                search_box = await page.wait_for_selector('textarea[name="q"]', timeout=10000)
                await search_box.fill("")
                await search_box.type(word, delay=random.randint(120, 220))
                await search_box.press("Enter")
                
                delay = random.randint(8, 15)
                print(f"    Waiting {delay}s...")
                await asyncio.sleep(delay)
            except Exception as e:
                print(f"[-] Search failed: {e}")

        print("[+] Automation Completed Successfully!")
        await browser.close()

if __name__ == "__main__":
    # ডামি সার্ভার মূল থ্রেডে অন রাখা যাতে প্রসেস বন্ধ না হয়ে সার্ভার লাইভ থাকে
    threading.Thread(target=lambda: asyncio.run(run_bot()), daemon=True).start()
    run_dummy_server()
