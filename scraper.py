from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

rsfPage = requests.get("https://recsports.berkeley.edu/rsf-weight-room-crowd-meter/")
assert(rsfPage.status_code == 200)

soup = BeautifulSoup(rsfPage.content, "html.parser")
iframes = soup.find_all("iframe")

iframes = [iframe["src"] for iframe in iframes if iframe.iframe != None and "density.io" in iframe["src"]]
assert(len(iframes) == 2)

for iframe in iframes:
    display = re.search(r'/dsp_(\d*)\?', iframe).group(1)
    token = re.search(r'token=(.*)$', iframe).group(1)
    frame = requests.get("https://api.density.io/v2/displays/dsp_" + display, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0', 'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br', 'Referer': 'https://safe.density.io/', 'Authorization': 'Bearer ' + token, 'Origin': 'https://safe.density.io', 'DNT': '1', 'Connection': 'keep-alive', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site', 'Sec-GPC': '1', 'TE': 'trailers'})
    assert(frame.status_code == 200)
    now = datetime.now() # current date and time
    f = open(frame.json()["name"] + "_" + str(int(now.timestamp())), "w")
    f.write(str(frame.json()))
    f.close()