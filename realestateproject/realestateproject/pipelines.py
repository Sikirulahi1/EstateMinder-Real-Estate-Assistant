# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
from psycopg2 import sql
import json


class RealestateprojectPipeline:
    def process_item(self, item, spider):
        return item


class SavingToPostgresPipeline(object):
    
    def __init__(self):
        self.create_connection()
        
    def create_connection(self):
        self.connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='mygoodlord',
            database='zillowrealestate',
            port='5432'
        )
        self.curr = self.connection.cursor()
        
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS house_data (
                id serial PRIMARY KEY, 
                price VARCHAR(255) NOT NULL,
                homeType VARCHAR(255) NOT NULL,
                propertyStatus VARCHAR(255),
                address TEXT NOT NULL,
                propertyDescription TEXT,
                ImageLink TEXT[],
                specialFeatures TEXT,
                houseFeatures TEXT,
                agentName VARCHAR(255) NOT NULL,
                agentLicenceNo VARCHAR(255),
                RealEstateCompany VARCHAR(255),
                contactNumber VARCHAR(255)
            )
        """)
        
    def process_item(self, item, spider):
        try:
            # Check to see if address is already in database 
            self.curr.execute("SELECT * FROM house_data WHERE address = %s", (item['address'],))
            result = self.curr.fetchone()

            # If it is in DB, create log message
            if result:
                spider.logger.warn("Item already in database: %s" % item['address'])
            else:
                # Prepare ImageLink as an array if necessary
                image_links = item['ImageLink'] if isinstance(item['ImageLink'], list) else [item['ImageLink']]
                
                # If text isn't in the DB, insert data
                self.curr.execute(""" 
                    INSERT INTO house_data (
                        price, 
                        homeType, 
                        propertyStatus, 
                        address, 
                        propertyDescription, 
                        ImageLink, 
                        specialFeatures, 
                        houseFeatures, 
                        agentName, 
                        agentLicenceNo, 
                        RealEstateCompany, 
                        contactNumber
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    item['price'],
                    item['homeType'],
                    item['propertyStatus'],
                    item['address'],
                    item['propertyDescription'],
                    image_links,
                    item['specialFeatures'],
                    item['houseFeatures'],
                    item['agentName'],
                    item['agentLicenceNo'],
                    item['RealEstateCompany'],
                    item['contactNumber'],
                ))

                # Execute insert of data into database
                self.connection.commit()
                print("New record inserted.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error storing item in the database: {e}")
            spider.logger.error(f"Error storing item in the database: {e}")
        return item
    
    def close_spider(self, spider):
        # Close cursor & connection to database 
        self.curr.close()
        self.connection.close()


class SavingToJSONPipeline:

    def open_spider(self, spider):
        self.file = open('house_data.json', 'a')
        self.seen_items = set()
        try:
            with open('house_data.json', 'r') as existing_file:
                for line in existing_file:
                    item = json.loads(line)
                    unique_id = (item['price'], item['address'], item['homeType'])
                    self.seen_items.add(unique_id)
        except FileNotFoundError:
            pass

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        unique_id = (item['price'], item['address'], item['homeType'])

        if unique_id not in self.seen_items:
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
            self.seen_items.add(unique_id)
        else:
            print(f"Duplicate item found: {unique_id}; not writing to JSON.")

        return item