import requests
import time, re, sys, os
import html as html_parser
from dotenv import load_dotenv; load_dotenv()

debug = False


def log(txt:str):
    #print(txt)
    logfile = open('file.log', "a+")
    logfile.write(f'[{time.strftime("%d/%m/%Y-%H:%M")}]{txt}\n')
    logfile.close()

def get_html(url:str, max_attempt:int=3):
    attempt = 1

    headers = {
      'Host': 'fr.igraal.com',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
      'Accept-Language': 'fr',
      'Accept-Encoding': 'gzip, deflate, br',
      'DNT': '1',
      'Connection': 'keep-alive',
      'Upgrade-Insecure-Requests': '1',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'none',
      'Sec-Fetch-User': '?1'
    }

    cookies = {
      'REMEMBERME': os.environ.get("IGRAAL_COOKIE"),
      'datadome': os.environ.get("IGRAAL_CAPTCHA")
    }



    while (attempt <= max_attempt):
        try:
            html = requests.get(url, headers=headers, cookies=cookies)
            return html_parser.unescape(html.text)
        except OSError as e:
            code = e.code if hasattr(e, 'code') else 'no_code'
            reason = e.reason if hasattr(e, 'reason') else 'no_reason'

            log(f"Error {code} {attempt}/{max_attempt} {reason} : {url} - {e}")
            if attempt == max_attempt:
                mail_yohan("[driiveme] Erreur get_html", f"{code}:{reason}\n{e}\n{url}\nattempt {attempt}/{max_attempt}")
            if code == 503 or code == 500:
                time.sleep(1 * 60 * 60)
            time.sleep(10 * 60)
            attempt += 1
    return -1
