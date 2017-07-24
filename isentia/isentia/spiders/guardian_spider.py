import scrapy

class GuardianSpider(scrapy.Spider):
    name = "guardian"
    allowed_domains = ["theguardian.com"]
    start_urls = [
                "https://www.theguardian.com/au",
        ]

    def parse_article(self,response):

        try:
            headline = response.css('.content__headline').xpath('text()'). \
                extract_first().strip()
            author = response.css('.byline').xpath('span/a/span/text()'). \
                extract_first().strip()
            published = response.css('.content__dateline').xpath('time/@datetime'). \
                extract_first().strip()
            tags = map(lambda s: s.strip(),
                   response.css('.submeta__keywords').css('.submeta__link'). \
                   xpath('text()').extract())
            url = 'https://www.theguardian.com' + \
              response.xpath('//html[@id="js-context"]/@data-page-path'). \
                  extract_first().strip()

            # yield Article information
            yield {
                'url': url,
                'headline': headline,
                'author': author,
                'published': published,
                'tags': tags
            }
        except Exception as e:
            #Some of the url's were empty might be due to an issue or they
            #were kept empty intentionally
            pass
        # Crawl all the articles found on the article page itself
        for href in response.css('.u-underline::attr(href)').extract():
            if href:
                yield response.follow(href, callback=self.parse_article)

    def parse(self, response):
        # Crawl all articles on the main page
        for href in response.xpath(
                '//a[contains(@data-link-name,"article")]/@href'
        ).extract():
            if href:
                yield response.follow(href, callback=self.parse_article)
