# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import logging
import pandas as pd
from datetime import datetime
import pyarrow as pa
import pyarrow.parquet as pq
import boto3
import os

class TripAdvisorHotelPipeline:
    
    def __init__(self, settings):
        self.S3_BUCKET = os.environ.get('S3_BUCKET')
        self.S3_PREFIX_PATH = os.environ.get('S3_PREFIX_PATH')
        self.item_list = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        ## Use to connect database 
        logging.warning('OPEN_SPIDER() METHOD INVOKED FROM PIPELINE')


    def write_df_to_s3_in_parquet_format(self, df):
        # Convert the Pandas dataframe to an Arrow table
        table = pa.Table.from_pandas(df)

        #Write the Arrow table to a Parquet file in memory
        parquet_bytes = pa.BufferOutputStream()
        pq.write_table(table, parquet_bytes)

         # Upload the Parquet file to S3
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket=self.S3_BUCKET,
            Key=f"{self.S3_PREFIX_PATH}hotels-{datetime.now().strftime('%Y-%m-%d-%H-%M')}.parquet",
            Body=parquet_bytes.getvalue().to_pybytes()
        )

    def close_spider(self, spider):
        ## use to close database
        logging.warning('CLOSE_SPIDER() METHOD INVOKED FROM PIPELINE')
        df = pd.DataFrame(data=self.item_list)
        df = df. astype(str)
        print(f'total item count: {df.count()}')
        self.write_df_to_s3_in_parquet_format(df)

    def process_item(self, item, spider):
        logging.info(f'Scraped hotel elements:: {item}')
        self.item_list.append(dict(item))
        return item