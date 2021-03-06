import os
import logging
from hashlib import sha256
from urllib.parse import urlparse

class UrlInfo(object):
    def __init__(self, url, completed = False, wordCount = 0):
        self.url = url
        self.completed = completed
        self.wordCount = wordCount
        
def get_logger(name, filename=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    fh = logging.FileHandler(f"Logs/{filename if filename else name}.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
       "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def get_urlhash(url):
    parsed = urlparse(url)
    # everything other than scheme.
    return sha256(
        f"{parsed.netloc}/{parsed.path}/{parsed.params}/"
        f"{parsed.query}/{parsed.fragment}".encode("utf-8")).hexdigest()

def normalize(url):
    # trim out url fragment
    parts = url.rsplit('/', 1)
    if len(parts) == 2:
        left, right = parts
        posi = right.find('#')

        # # trim query ??
        # posi1 = right.find('?', 0, posi)
        # if posi1 != -1 and posi1 < posi:
        #     posi = posi1

        if posi != -1:
            url = left + '/' + right[:posi]
    
    if url.endswith("/"):
        return url.rstrip("/")
    return url