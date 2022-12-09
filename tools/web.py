from typing import Optional
from tools import INPUT_FILE_NAME, INPUTS_DIR
from tools.config import get_configuration
import os 
from pathlib import Path 
import requests
import sys 

# curl 'https://adventofcode.com/2022/day/7/answer' -X POST -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: https://adventofcode.com' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Referer: https://adventofcode.com/2022/day/7' -H 'Cookie: session=XXX' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: same-origin' -H 'Sec-Fetch-User: ?1' -H 'Sec-GPC: 1' --data-raw 'level=2&answer=3866390'


def download_input(file_path:Optional[str]=None): 
    if file_path is None:
        file_path = sys.argv[0]

    filename = Path(file_path).stem

    if os.path.exists(os.path.join(INPUTS_DIR, filename, INPUT_FILE_NAME)):
        return 

    input_num = int(filename.split("_")[1])

    config = get_configuration()
    cookies = {}
    for key, value in config.items("requests.cookies"):
        cookies[key] = value
        

    response = requests.get(f"https://adventofcode.com/2022/day/{input_num}/input", cookies=cookies)

    os.makedirs(os.path.join(INPUTS_DIR, filename), exist_ok=True)

    with open(os.path.join(INPUTS_DIR, filename, INPUT_FILE_NAME), 'wb') as f:
        f.write(response.content)
