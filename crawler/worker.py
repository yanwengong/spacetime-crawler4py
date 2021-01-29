from threading import Thread

from utils.download import download
from utils import get_logger
from scraper import scraper
import time


class Worker(Thread):
    def __init__(self, worker_id, config, frontier, reporter):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.reporter = reporter
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls, urlInfo, token_list = scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.reporter.add_words(tbd_url, token_list)
            self.frontier.mark_url_complete(tbd_url, urlInfo)
            time.sleep(self.config.time_delay)
