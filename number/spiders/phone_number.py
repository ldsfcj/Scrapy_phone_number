import scrapy

#http://www.jihaoba.com/escrow/

class phoneSpider(scrapy.Spider):
    name = 'phone'

    start_urls = ['http://www.jihaoba.com/escrow/']

    def parse(self, response):
        for ul in response.xpath('//div[@class="numbershow"]/ul'):
            phone_frist = ul.xpath('li[contains(@class,"number")]/a/@href').re('\d{11}')[0]
            price = ul.xpath('li[@class="price"]/span/text()').extract_first()[1:]
            brand = ul.xpath('li[@class="brand"]/text()').extract_first()

            if price.endswith('万'):
                price = int(float(price[:-1])*10000)
            else:
                price = int(price)

            yield {
                "phone_number":phone_frist,
                "number_price":price,
                "brand":brand
            }

        next_page = "http://www.jihaoba.com" + response.xpath('//a[@class="m-pages-next"]/@href').extract_first()

        yield scrapy.Request(url=next_page,callback=self.parse)

