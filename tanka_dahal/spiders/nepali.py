import scrapy
from scrapy_playwright.page import PageMethod

class NepaliSpider(scrapy.Spider):
    name = "nepali"
    allowed_domains = ["www.youtube.com"]
    start_urls = ["https://www.youtube.com/@TheNepaliComment/shorts"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0], 
            callback=self.parse,
            meta=dict(
                playwright=True,  # Enable Playwright
                playwright_page_methods=[
                    PageMethod("wait_for_selector", "a.ShortsLockupViewModelHostEndpoint.ShortsLockupViewModelHostOutsideMetadataEndpoint"),  # Wait for video elements to load
                ],
            ),
            )

    def parse(self, response):
        base_url = "https://www.youtube.com"
        # Extract video links and titles using XPath
        video_xpath = response.xpath('//a[@class="ShortsLockupViewModelHostEndpoint ShortsLockupViewModelHostOutsideMetadataEndpoint"]')
        # title_xpath = response.xpath('//a[@class="ShortsLockupViewModelHostEndpoint ShortsLockupViewModelHostOutsideMetadataEndpoint"]/span')

        # Print video links and titles
        for link in video_xpath:
            video_url = link.xpath('./@href').get()
            video_title = link.xpath('.//span/text()').get()

            if video_url:
                video_url = f"{base_url}{video_url}"

            print(video_url)
            print(video_title)
            
            
            yield {
                    "title": video_title,
                    "url": video_url,
                    "source_name": 'The Nepali Comment'
                }