from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from travelportals.spiders.TripAdvisor import TripadvisorSpider

def handler(event=None, context=None):
    try:
        process = CrawlerProcess(get_project_settings())
        process.crawl(TripadvisorSpider)
        process.start()

        return { 
            'statusCode': '200',   # a valid HTTP status code
            'body': 'Lambda function execution success',        
        }
    except Exception as e:
         return { 
            'statusCode': '500',   # a valid HTTP status code
            'error_message': f'ERROR: {e}',
            'body': 'Lambda function execution failed',        
        }
    
if __name__ == '__main__':
    handler()


