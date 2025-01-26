from playwright.sync_api import sync_playwright

class WebScraper:
    def __init__(self, config):
        self.use_cdp = config.playwright.use_cdp
        self.cdp_endpoint = config.social_media.whatsapp.cdp_endpoint
        self.playwright = sync_playwright().start()
        self.browser = self.connect_browser()

    def connect_browser(self):
        if self.use_cdp and self.cdp_endpoint:
            browser = self.playwright.chromium.connect_over_cdp(self.cdp_endpoint)
        else:
            browser = self.playwright.chromium.launch(headless=True)
        return browser

    def scrape(self, url):
        context = self.browser.new_context()
        page = context.new_page()
        page.goto(url)
        # ...existing code...
        content = page.content()
        # ...existing code...
        page.close()
        context.close()
        return content

    def close(self):
        self.browser.close()
        self.playwright.stop()
    # ...existing code...
