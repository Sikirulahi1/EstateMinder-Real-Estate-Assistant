import us
import scrapy
import time
import time
from urllib.parse import urlencode, urljoin
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class ZillowSpider(scrapy.Spider):
    name = "zillowspider"
    allowed_domains = ["www.zillow.com", "proxy.scrapeops.io"]

    API_KEY = 'da5fdb70-f539-409f-99d0-5668313f82ff'


    def get_proxy_url(self, url):
        payload = {'api_key': self.API_KEY, 'url': url}
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
        return proxy_url


    def get_zillow_url(self, city, state, page=1):
        state_abbr = us.states.lookup(state).abbr if us.states.lookup(state) else state
        city = city.replace(' ', '-')
        return f"https://www.zillow.com/homes/{city},-{state_abbr}_rb/{city.lower()}-{state_abbr.lower()}/{page}_p/"


    def start_requests(self):
        loc_dict = {
            'city': ['San Francisco', 'New York', 'Dallas',],
            'state': ['California', 'New York', 'Texas', ]
        }


        for city, state in zip(loc_dict['city'], loc_dict['state']):
            
            for page in range(1, 21): 
                house_url = self.get_zillow_url(city, state, page)
                
                yield scrapy.Request(
                    url=house_url, 
                    callback=self.parse_search_results,
                    meta={'city': city, 'state': state}
                )



    def parse_search_results(self, response):

        city = response.meta['city']
        state = response.meta['state']
        self.log(f"Scraping {city}, {state} - URL: {response.url}")
        time.sleep(2)
        
        for property_card in response.css('div.PropertyCardWrapper__StyledPropertyCardBody-srp-8-105-0__sc-16e8gqd-4'):
            # Extract property URL
            property_url = property_card.css('a.property-card-link::attr(href)').get()
            
            if property_url:
                absolute_property_url = response.urljoin(property_url)  # Form full URL if the link is relative
                # Make a request to the property page to extract price and other details
                
                yield scrapy.Request(
                    url=self.get_proxy_url(absolute_property_url),
                    callback=self.parse,
                    meta={'city': city, 'state': state})
            
            
    def parse(self, response):
        
        # Extract price from the property page
        price = response.css('span[data-testid="price"] span::text').get()
        property_status = response.css('.Text-c11n-8-100-2__sc-aiai24-0.bSfDch::text').get()
        homeType = response.xpath('(//span[contains(@class, "Text-c11n-8-100-2__sc-aiai24-0")]/text())[8]').get()
        address = ''.join(response.css('h1.Text-c11n-8-100-2__sc-aiai24-0::text').getall()).replace('\xa0', ' ').strip()
        property_description = " ".join(response.css('div[data-testid="description"] div.Text-c11n-8-100-2__sc-aiai24-0::text').getall()).strip()
        property_img_link = response.css('picture img::attr(src)').getall()
        
        tags = response.css('div.Spacer-c11n-8-100-2__sc-17suqs2-0.bJkbaI div[role="list"] span::text').getall()
        specialFeatures = ', '.join(tags)
        
        agentName = response.css('p[data-testid="attribution-LISTING_AGENT"] span:nth-child(1)::text').get()
        agentLicenceNo = response.css('p[data-testid="attribution-LISTING_AGENT"] span:nth-child(2)::text').get()
        RealEstateCompany = response.css('p[data-testid="attribution-BROKER"] span:nth-child(1)::text').get()
        contactNumber = response.css('p[data-testid="attribution-BROKER"] span:nth-child(2)::text').get()
        ## Extracting the further features of the house
        houseFeatures = f"\n"
        
        for category in response.css('div.styles__StyledFactCategory-fshdp-8-100-2__sc-1i5yjpk-0'):

            sub_heading = category.css('h6::text').get()
            facts = category.css('ul.styles__StyledFactCategoryFactsList-fshdp-8-100-2__sc-1i5yjpk-1 li span::text').getall()
            grouped_facts = [''.join(facts[i:i+3]) for i in range(0, len(facts), 3)]
            houseFeatures += f"{sub_heading}:\n{', '.join(grouped_facts)}\n\n"
        
        
        yield {
            'price' : price,
            'homeType' : homeType,
            'propertyStatus': property_status,
            'address' : address,
            'propertyDescription' : property_description,
            'ImageLink': property_img_link,
            'specialFeatures' : specialFeatures,
            'houseFeatures' : houseFeatures,
            'agentName': agentName,
            'agentLicenceNo' : agentLicenceNo,
            'RealEstateCompany' : RealEstateCompany,
            'contactNumber' : contactNumber,
        }
        