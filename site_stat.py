import psutil, time
from selenium import webdriver


class SiteStater:
    def go_to_baseline(self):
        self.driver.get(self.baseline_website)

    def stat_current(self):
        return self.process.cpu_percent(interval=None)

    def stat_website(self, site_url):
        self.init_driver()
        self.go_to_baseline()
        self.stat_current()
        try:
            self.driver.get(site_url)
            time.sleep(self.pause)
            after = self.stat_current()
        except:
            after = None
        finally:
            self.close()
            return after

    def init_driver(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_page_load_timeout(self.timeout)
        for child in psutil.Process().children():
            if 'phantom' in child.name():  # 'geckodriver' for firefox
                self.process = child
                break
        if not self.process:
            raise Exception('Failed to launch PhantomJS')

    def __init__(self, pause=10, timeout=60):
        self.driver = None
        self.process = None
        self.pause = pause
        self.timeout = timeout
        self.baseline_website = 'http://whatismyip.akamai.com'

    def close(self):
        self.driver.quit()