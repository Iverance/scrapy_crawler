from scrapy.spider import Spider
from scrapy.selector import Selector

from tutorial.items import DmozItem

class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://doc.scrapy.org/en/latest/topics/selectors.html"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        """
        logs = open(filename, 'wb').write(response.body)
        """
        sel = Selector(response)

        text = sel.xpath('//div/*/text()').extract()
        text.remove("\n")
        text = [x for x in text if "u'\n'" not in x]
        with open(filename+'_text.txt', 'w') as t:
            t.write('{0}\n'.format(text))

        sites = sel.xpath('//ul/li')
        items = []
        for site in sites:
            item = DmozItem()
            item['title'] = site.xpath('a/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('text()').extract()
            items.append(item)
            with open(filename+'_url.txt', 'w') as f:
                f.write('name: {0}, link: {1}\n'.format(item['title'], item['link']))
        

