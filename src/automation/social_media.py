from playwright.sync_api import sync_playwright

class SocialMediaAutomator:
    def __init__(self, use_cdp=False, cdp_endpoint=None):
        self.use_cdp = use_cdp
        self.cdp_endpoint = cdp_endpoint
        self.playwright = sync_playwright().start()
        self.browser = self.connect_browser()

    def connect_browser(self):
        if self.use_cdp and self.cdp_endpoint:
            browser = self.playwright.chromium.connect_over_cdp(self.cdp_endpoint)
        else:
            browser = self.playwright.chromium.launch(headless=False)
        return browser

    def login(self, url, username, password):
        context = self.browser.new_context()
        page = context.new_page()
        page.goto(url)
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')
        # ...existing code...
        page.close()
        context.close()

    def post_update(self, content):
        context = self.browser.new_context()
        page = context.new_page()
        # ...existing code...
        page.goto('https://socialmedia.com/post')
        page.fill('textarea[name="post"]', content)
        page.click('button[type="submit"]')
        # ...existing code...
        page.close()
        context.close()

    def close(self):
        self.browser.close()
        self.playwright.stop()
    # ...existing code...
