import scrapy
from scrapy import Request
from re import findall 
from scrapy.loader import ItemLoader 
from companies.items import CompaniesItem
from math import ceil 

class SkaddenSpider(scrapy.Spider):
    name = 'gibbonslaw'
    allowed_domains = ['gibbonslaw.com']
    start_urls = []

    def __init__(self):
        self.listing_template = 'https://www.gibbonslaw.com/api/professionals?letter=&page={}'
        self.not_names = ['J.P.','Jr.','V','III','M.','II','J.','W.','R.','AICP','G.','IV','W.F.','D.','S.','R.','W.','C.','Dr.','F.','A.','P.']


    def start_requests(self):
        yield Request(
            self.listing_template.format(1),
        )


    def parse(self,response):
        total_pages = self.get_total_pages(response)
        for page in range(1,total_pages + 1):
            yield Request(
                self.listing_template.format(page),
                dont_filter=True,
                callback = self.parse_individuals,
            )


    def parse_individuals(self, response):
        people_urls = [response.urljoin(item['link']['url']) for item in response.json()['results']]
        for url in people_urls :
            yield Request(
                url,
                callback =self.parse_individual
            )



    def parse_individual(self,response):
        loader = ItemLoader(CompaniesItem(),response)
        loader.add_value('url',response.url)
        fullname_list = response.xpath('string(//h1)').get().split()
        if any(name == fullname_list[0] for name in self.not_names):
            loader.add_value('first_name', fullname_list[1])
        else :
            loader.add_value('first_name', fullname_list[0])
        if any(name == fullname_list[-1] for name in self.not_names):
            loader.add_value('last_name', fullname_list[-2])
        else :
            loader.add_value('last_name', fullname_list[-1])
        loader.add_value('firm',self.name)
        loader.add_css('title','h2.hero__subtitle::text')
        loader.add_css('email','a.contact-info__email::text')
        educations_list = [edu.xpath('string(.)').get() for edu in response.xpath('//button[@aria-label="Toggle Education"]/ancestor::div[1]/following-sibling::div//p')]
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
        loader.add_css('image','img.hero__square-image::attr(src)')
        loader.add_xpath('bio','string(//div[@class="tabs__section"]//div[@type="richText"])')
        loader.add_value('firm_bio','https://www.gibbonslaw.com/about')
        loader.add_css('office','a.contact-info__office-link::text')
        yield loader.load_item()


    def get_total_pages(self,response):
        return ceil(response.json()['total']/8)


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


                