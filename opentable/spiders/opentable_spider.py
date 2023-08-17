import scrapy
import json
from opentable.items import OpentableItem
from scrapy.http import Request
  

class OpentableSpider(scrapy.Spider):
    name = 'opentable_spider'
    
    def start_requests(self):
        json_file_path = r'F:\Leapfrog_data\jsonscrape\opentable\opentable\spiders\format.json'
        print("JSON File Path:", json_file_path)  # Debug print
        try:
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                multi_search_data = data.get('multiSearch', {})  # Get the 'multiSearch' dictionary
                restaurants_details = multi_search_data.get('restaurants', [])  # Get the 'restaurants' list
                for restaurant in restaurants_details:
                    yield self.create_request(restaurant)
        except KeyError:
            self.logger.error("'restaurants' key not found in JSON data.")

    def create_request(self, restaurant):
        profile_link = restaurant.get('urls', {}).get('profileLink', {}).get('link', '')
        return Request(url=profile_link, callback=self.parse_restaurant, meta={'restaurant_data': restaurant})



    def parse_restaurant(self, response):
        restaurant_data = response.meta.get('restaurant_data', {})  

        print("Parsing restaurant:", restaurant_data['name'])

        item = OpentableItem()
        item['name'] = restaurant_data['name']
        item['area'] = restaurant_data['neighborhood']['name']
        item['price'] = restaurant_data['priceBand']['name']
        item['location'] = f"{restaurant_data['address'].get('line1', '')}, {restaurant_data['address'].get('city', '')}, {restaurant_data['address'].get('state', '')} {restaurant_data['address'].get('postCode', '')}"
        item['cuisine'] = restaurant_data['primaryCuisine']['name']
        item['profile_link'] = restaurant_data.get('urls', {}).get('profileLink', {}).get('link', '') 
        rating_data = restaurant_data.get('statistics', {}).get('reviews', {}).get('ratings', {}).get('overall', {})
        item['rating'] = rating_data.get('rating', '') 
        

        yield item

