import time, re, sys, os
import html as html_parser
from ppadb.client import Client as AdbClient
import subprocess


def log(txt:str, verbose=False, end='\n', date=True):
    if verbose == True:
        print(txt)
    logfile = open('tmp/file.log', "a+")
    if date == False:
        logfile.write(txt+end)
    else:
        logfile.write('['+time.strftime("%d/%m/%Y-%H:%M")+']'+txt+end)
    logfile.close()

def get_html_android(url, max_retry=5):
    html_path, retry = './webdav/page.html', 0
    if os.path.exists(html_path): os.remove(html_path)
    
    client = AdbClient(host='127.0.0.1', port=5037)
    device = client.device('89BX07Q17')
    device.shell('am force-stop org.mozilla.fenix && sleep 3')
    device.shell(f'am start -a android.intent.action.VIEW -d {url}')
    ts_loading = time.time()
    while not os.path.exists(html_path):
        time.sleep(1)
        if time.time() - ts_loading > 60:
            log(f'{retry}/{max_retry} Time out {url}', verbose=True)
            retry, ts_loading = retry + 1, time.time()
            device.shell('am force-stop org.mozilla.fenix && sleep 3')
            device.shell(f'am start -a android.intent.action.VIEW -d {url}')
        if retry == max_retry:
            log(f'Cannot reach {url}', verbose=True)
            sys.exit()

    with open(html_path) as f: data = f.read()
    return html_parser.unescape(data)



###
# Fonctionne puis demande d'activer JS lorsqu'on est suspect
###

# def get_android_cookies():
#   client = AdbClient(host='127.0.0.1', port=5037)
#   device = client.device('89BX07Q17')
#   device.shell('am start -a android.intent.action.VIEW -d "fr.igraal.com/"')
#   input('source?')
#   #time.sleep(10)
#   FF_cookies_db = '/data/data/org.mozilla.firefox/files/mozilla/2l3a3dvx.default/cookies.sqlite'
#   sql_cmd = "SELECT name, value FROM moz_cookies WHERE host LIKE '%igraal.com%';"
#   adb_cookies = device.shell(f'sqlite3 {FF_cookies_db} "{sql_cmd}"').strip()
#   #print(cookies)
#   cookies = {}
#   for c in adb_cookies.split('\n'):
#     name_value = c.split('|')
#     cookies[name_value[0]] = name_value[1]

#   return cookies  

# #adb shell am start -a android.intent.action.VIEW -d https://www.igraal.com/
# #adb shell input text "yohan.web@outlook.com"

# from fake_useragent import UserAgent
# from requests_html import HTMLSession

# def get_html(url:str, max_attempt:int=3):
#     attempt = 1

#     ua = UserAgent()
#     header = {'User-Agent':str(ua.firefox)}

#     # headers = {
#     #   'Host': 'fr.igraal.com',
#     #   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
#     #   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
#     #   'Accept-Language': 'fr',
#     #   'Accept-Encoding': 'gzip, deflate, br',
#     #   'DNT': '1',
#     #   'Connection': 'keep-alive',
#     #   'Upgrade-Insecure-Requests': '1',
#     #   'Sec-Fetch-Dest': 'document',
#     #   'Sec-Fetch-Mode': 'navigate',
#     #   'Sec-Fetch-Site': 'none',
#     #   'Sec-Fetch-User': '?1'
#     # }

#     # cookies = {
#     #   'REMEMBERME': os.environ.get("IGRAAL_COOKIE"),
#     #   'datadome': os.environ.get("IGRAAL_CAPTCHA")
#     # }

#     cookies = get_android_cookies()

#     while (attempt <= max_attempt):
#         try:
#             session = HTMLSession()
#             r = session.get(url, headers=header, cookies=cookies)
#             r.html.render()
#             #html = requests.get(url, headers=header, cookies=cookies)
#             return html_parser.unescape(r.html.text)
#         except OSError as e:
#             code = e.code if hasattr(e, 'code') else 'no_code'
#             reason = e.reason if hasattr(e, 'reason') else 'no_reason'

#             log(f"Error {code} {attempt}/{max_attempt} {reason} : {url} - {e}")
#             if attempt == max_attempt:
#                 mail_yohan("[driiveme] Erreur get_html", f"{code}:{reason}\n{e}\n{url}\nattempt {attempt}/{max_attempt}")
#             if code == 503 or code == 500:
#                 time.sleep(1 * 60 * 60)
#             time.sleep(10 * 60)
#             attempt += 1
#     return -1

