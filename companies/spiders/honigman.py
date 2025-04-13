import scrapy
from scrapy import Request
from re import findall 
from scrapy.loader import ItemLoader 
from companies.items import CompaniesItem



class HonigmanSpider(scrapy.Spider):
    name = 'honigman'
    allowed_domains = ['honigman.com']
    start_urls = ['https://www.honigman.com/attorneys-directory.html?results']


    def parse(self, response):
        people_urls = [response.urljoin(url) for url in response.css('div.title a::attr(href)').getall()]
        for url in people_urls :
            yield Request(
                url ,
                callback = self.parse_individual
            )


    def parse_individual(self,response):
        loader = ItemLoader(CompaniesItem(),response)
        loader.add_value('url',response.url)
        fullname_list = response.xpath('//h1/text()').get().split()
        loader.add_value('first_name', fullname_list[0])
        loader.add_value('last_name',fullname_list[-1])
        loader.add_value('firm',self.name)
        loader.add_css('title','div#bioTitle::text')
        loader.add_css('email','div#bioEmail a::text')
        educations_list = [edu.xpath('string(.)').get() for edu in response.css('div.startInline')]
        try :
            law_school , year = self.get_law_school(educations_list)
            loader.add_value('law_school',law_school)
            loader.add_value('law_school_graduation_year',year)
        except TypeError : 
            pass 
        try : 
            undergraduate_school, year = self.get_undergraduate_school(educations_list)
            loader.add_value('undergraduate_school',undergraduate_school)
            loader.add_value('undergraduate_school_graduation_year',year)
        except TypeError :
            pass
        loader.add_value('image',response.urljoin(response.css('img.bioPhoto::attr(src)').get()))
        loader.add_xpath('bio','string(//div[@id="bio_content"])')
        loader.add_value('firm_bio','https://www.honigman.com/firm.html')
        loader.add_xpath('office','string(//ul[@id="bioOfficeInfo"]/li[1])')
        yield loader.load_item()


    def get_law_school(self,educations_list):
        year = education = ''
        for edu in educations_list : 
            if 'law' in edu.lower() : 
                education = edu
                try :
                    year = findall('\d\d\d\d',education)[0]
                except IndexError : 
                    pass
                return education,year


    def get_undergraduate_school(self,educations_list):
        year = education = ''
        for edu in educations_list : 
            if not 'law' in edu.lower() : 
                education = edu
                try : 
                    year = findall('\d\d\d\d',education)[0]
                except IndexError : 
                    pass
                return education,year