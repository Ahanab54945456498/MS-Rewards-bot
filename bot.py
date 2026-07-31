import asyncio
import random
import os
import http.server
import socketserver
import threading
from playwright.async_api import async_playwright

# ১. আপনার প্রদান করা কুকি লিস্ট
COOKIES = [
    {
        "name": "SRCHUSR",
        "value": "DOB=20260731&DS=1&POEX=W",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "_Rwho",
        "value": "u=m&ts=2026-07-31",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": True,
        "sameSite": "None"
    },
    {
        "name": "rn_S",
        "value": "eyJhbGciOiJSU0EtT0FFUC0yNTYiLCJlbmMiOiJBMjU2R0NNIn0.sVEvRSjqaaOOEhavfP3f5b7gdjxS-pWe182yZDKYUYAjAaoa89QVfv5vDMdWbMeBlHI5PnhwAawd_OcK-jNHAZrQtdH5ZAMvM442D71JOXPbFpZ9n-QBvfJgxAh14rSwKZcsZKTZOD3FD7sXRh317-YKRF2zyzWiSxMRuncevofpJEhZ-jH5JfXGpP7ddSsryz0uHYjnKADwoIgdibbaRW8cO6eZZpUtVPt83R8n4ueoa2FbYrcX1K8YCycr6AVScrSnQ3KXZs5IJMlkNa5AB36seeisK8aQlNZkvlt7n12ZW9Z7Jw4y5rdtP3nyRlpXICxM7KE9I8lJcwNsTospOw.NYnGB1XAewHukIYI.AB97oLiO-Ky14ox6OvtOEc5tKJ7gptDmo5x0DAzZtfjHcSzMhMnNTufvamG6dWWI8HWpGX_wRy8quSTvOSsinOJe9WF6mM3IKLwmkTH5dI4n1RPB-XS-NiWahOmYIezKaZhZt5ddcE4sRDDx90yzpxxgvbp9eHnwLe9MgTi6pnjweLa3L_8athjKAXAYCs-0z5i66EmpbUk7t69Si4OmMRFOfCjcE4tuREKwXPcz71ZfGhiV1Zo6WgrNui2iUcTfOh2aYFM9c_2hfmjaluKMhdEPLvPLojYXHmINMbi1f1yJ6I1A4EiEWgLia011EFD3NLmp3ssmT-mzZoCxKSaj2eLZjUMQ1aeBKS0Pu-tyVaezSIE.Khksz1KX42NAhYSctoH90w",
        "domain": "rewards.bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": True,
        "sameSite": "None"
    },
    {
        "name": "MSFPC",
        "value": "GUID=737131a8c41e4d3d88a6e6edf29c4b50&HASH=7371&LV=202607&V=4&LU=1785468654071",
        "domain": "rewards.bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "SRCHHPGUSR",
        "value": "SRCHLANG=en&IG=508FD4D8F3EB4878AF4707A4EF9CCBD2&PREFCOL=0&CW=456&CH=777&SCW=456&SCH=777&BRW=MW&BRH=MT&DPR=1.6&UTC=360&HV=1785468644&HVE=CfDJ8A8rLfEh4ZdMhJ19YNJ4FtTwlECfCZ59_ER84feDlBC5p8p0FvDTMijgzaB4ayChoSOGu1OsxdfGWEEc4KonRSPEMc32diT5yofJrpi6oX4gk1NeDS5vg-1Q18HVQf2OkRSf5KhdOUzJQPsOP4tR7BGC9CGUsn6fj9H948bbrsHR-rwWnsS4L75d5_BjUI8oFg&HBOPEN=2",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "ANON",
        "value": "A=2A6491C3C23E819FC98BE046FFFFFFFF",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "_SS",
        "value": "SID=207177D25DC16724028660755CF966B0&R=365&RB=365&GB=0&RG=0&RP=0",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "_U",
        "value": "1yg9-6EJYJdmJ6nik49nuZDbJWzD7c0G0eZ7Qs4HkVXMF5ZzGOkXsrnYOWTeJg7CESjHTQgXuTzadoVIqtdP6lbP4DgUkA_nmvWNLCsAx1RCyHZjPNcry6CNstowpupauMV_ScpqMUsV6NBQuRmZlrBsneLaP41VXHY30aBg1wn0R0wyX7C62Ko_Fr6yvcXeVsR7xkPkUHY1YxoqV3IEo_w",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "ai_session",
        "value": "3pKtGPX3i/R1Qnt51O2eTQ|1785468651676|1785468658307",
        "domain": "rewards.bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "SRCHD",
        "value": "AF=NOFORM",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "GRNID",
        "value": "a6493296-db30-4034-93fb-c3a51ec00114",
        "domain": "rewards.bing.com",
        "path": "/",
        "secure": False,
        "httpOnly": False
    },
    {
        "name": "_EDGE_V",
        "value": "1",
        "domain": ".bing.com",
        "path": "/",
        "secure": False,
        "httpOnly": True
    },
    {
        "name": "BFBUSR",
        "value": "BFBHP=0",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "_RwBf",
        "value": "mta=0&ispd=0&rc=365&rb=365&rg=0&pc=0&mtu=0&rbb=0.0&clo=0&v=1&l=2026-07-30T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=1785389790&rwflt=-62135539200&rwaul2=0&g=newLevel1&o=0&p=None&c=MY00I3&t=8900&s=2026-07-23T01:57:56.2950124+00:00&ts=2026-07-31T03:30:44.9887565+00:00&rwred=0&wls=2&wlb=0&wle=0&ccp=2&cpt=0&lka=0&lkt=0&aad=0&TH=&cid=0&gb=2026w30_u&e=At2479UcSU2QJ_5bMUNkt1Bb_CrBWKkpOa3ODrAYKA2SO5AOTQk8Qiio1WA11dg0jhU_v3V6U_DtgVZLvfoZMA&A=2A6491C3C23E819FC98BE046FFFFFFFF",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "_EDGE_S",
        "value": "F=1&SID=207177D25DC16724028660755CF966B0",
        "domain": ".bing.com",
        "path": "/",
        "secure": False,
        "httpOnly": True
    },
    {
        "name": "_C_ETH",
        "value": "1",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": True
    },
    {
        "name": ".MSA.Auth",
        "value": "CfDJ8A8rLfEh4ZdMhJ19YNJ4FtQQx1EbCxY_VjHjNqVJ8iAr9GRLLzxNs_CIhK7dANH2ZcaZ25s4MyPptZp2j1-MtefTknl-jkSKFcf0NaoVFvZFOu4-Ozo-P4fYz815kdTkG67GUEr047BQniE1hGekte8nhHsUCFWZLPeYTTxlRRrwcL3hNXd_11Ca0eiCZQtrNtbjMKF8NMsV7evTJgzQdDyaZNEufjh8fHHNiURqpy1ZteQPIipf8jeKZPWRjhVzYOJtnNdt6sPksWquTXyo4ae8j0UU7HmUw2jeTE-vZuiuALJRqp3scPL1qGxndfqW8hLhKXemMteLtBlormmgrkdgtLikq_L_lh0P3gbkMARMjyHLTAHIXuxtYKVT_gChVRD1uMcLEt9vTXKcYiSuj2WikV5WhS-IYANxGhMVKUi_UnKvMCMSCnsJUjFbHHO7ZWnqlrx_8WwVtBtKJUZ9zPLe2g1V7AlKYkR_ncO9A0e3ceTR0FRAaQD2_NA9zcetGXA96_TLa19yFzxVEm8cJ6yskKJrFlFi7f95Ijpr0w4gFTKUCfc5rSHDPByLqZirS8iyKgICp7iNwp_QBbrq74gAfSYRyE6IbPiPGk0tGbqv26mKA3wYlOheDiSAycuAAEIkVVXkO-yiVJnNOZDJbrIHZlL4ZlxUNNv4QZw3sAtq39wgyP9EOFn8cSvkcTzzZP4F-wqp0vGyfT5IsRCIyPz4oNVIGcSJkYK8lGzl6iQPofx8YsBFHRTMK_qpIhWmuOxR6NSK-HulpG3xPGweOTE9auFjJwxcGZCgwCT5gUppQuTKwDiYCGl0htf7UOLHmikdEDF5cpuNZxWd6kGQvxNkGAC65TM_lzvW7NiM1BJWBkRYEA3nG4kL5fg3cdvqxaZDQHg4WhlPeY5g3Vlitrg0WFiC-oXl2GlB3XRoqOkTarR7arlpLfiFLXyyOY-d3g",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": True,
        "sameSite": "Lax"
    },
    {
        "name": "_C_Auth",
        "value": "",
        "domain": "rewards.bing.com",
        "path": "/",
        "secure": False,
        "httpOnly": False
    },
    {
        "name": "_HPVN",
        "value": "CS=eyJQbiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyNi0wNy0zMVQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjoyLCJUb2JuIjowfQ==",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "_MsaRef",
        "value": "RT=1785472207833",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "Lax"
    },
    {
        "name": "ak_bmsc",
        "value": "5A372D9AF78009B332E79DBB2A992EC2~000000000000000000000000000000~YAAQrg4DFzMD56WfAQAAbGA5tgBmMk4MSLlPJFakBEIUPb4EKAig2wzrFHMAa+AZvdMNhNC4iaAqw2Yz8S2cmmMIs4R9/FN83heFkXABnkxZKCX9A6hKJF26DVV7wibBeduRXfY3e4BuIRIa8JGG2kdcjm/MjBFzaWz1BEcces+riL/VSD6dCvAacLb36WRxoHwCM7xKh5vEnVmdqGgTLOKqHqr184U8qMUYZMrnHStZ1m/h4wfiDtuJmIStCg+7oBaE6Tv9Pv6nolrg89bNKY+n4jbXfX7jcpPBYIGhnmW6iTnSuMUU/6Wg0kXt5F9hSArEoBCOarS0MeIg/y6HEpkV8CSMbLde3uBYKc9VGggMaZNKjMGsRn159+ZT7siw",
        "domain": ".bing.com",
        "path": "/",
        "secure": False,
        "httpOnly": True
    },
    {
        "name": "MicrosoftApplicationsTelemetryDeviceId",
        "value": "6c4316f9-2b4c-4b80-b446-d9cb57d7ff60",
        "domain": "rewards.bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "MSCC",
        "value": "NR",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "MUID",
        "value": "3326F4FBBB39640F27B8E35CBA016556",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "MUIDB",
        "value": "3326F4FBBB39640F27B8E35CBA016556",
        "domain": ".bing.com",
        "path": "/",
        "secure": False,
        "httpOnly": True
    },
    {
        "name": "rn_SID",
        "value": "207177D25DC16724028660755CF966B0",
        "domain": "rewards.bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": True,
        "sameSite": "None"
    },
    {
        "name": "SRCHUID",
        "value": "V=2&GUID=F5A45AD3621A47FF8E5DD6EEBEBD61DD&dmnchg=1",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    },
    {
        "name": "WLS",
        "value": "C=7f24f8aa3615f37e&N=Nasib",
        "domain": ".bing.com",
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None"
    }
]

# ২. কি-ওয়ার্ড লিস্ট
KEYWORDS = [
    "Latest technology news 2026", "Python Playwright tutorial", "ESP32 robotics ideas",
    "Cricket world cup updates", "Best budget laptops", "AI development trends",
    "SpaceX launch schedule", "Web automation tips", "Arduino home automation"
]

# ৩. ডামি সার্ভার (Render এর জন্য)
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

# ৪. মেইন অটোমেশন লজিক
async def run_bot():
    print("[+] Starting Rewards Automation Bot (Cookie Mode)...", flush=True)

    async with async_playwright() as p:
        try:
            print("[+] Launching Browser...", flush=True)
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
            
            # কুকি ইনজেক্ট করা
            print("[+] Injecting Authentication Cookies...", flush=True)
            await context.add_cookies(COOKIES)
            
            page = await context.new_page()

            # --- স্টেপ ১: সেটিং সেশন ---
            print("[+] Verifying Logged-in Session on Bing...", flush=True)
            await page.goto("https://www.bing.com", wait_until="commit", timeout=15000)
            await asyncio.sleep(2)
            print("[+] Cookie Session Injected Successfully!", flush=True)

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
