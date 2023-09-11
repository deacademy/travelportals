# travelportals
Educational project to scrape data from trustable sites and execute over AWS lambda for querying scraped data through the AWS Atena service

You you want to download the source code in your local system through git command then make sure you have git versioning tool installed in your local system.
you can use below command to download source code from master branch in your local system using git command.
>> git clone --branch master https://github.com/deacademy/travelportals.git

# Install user-agent package to use fake user agents to bypass restrictions ->
pip install scrapy-user-agents

# Install  scrapy_proxy_pool to use fake profixes to bypass restrictions ->
pip install scrapy_proxy_pool

# Install botocore to connect to aws s3 ->
pip install botocore

## Service use to get api key use to get 1000 free profixes ->(Need to create own account with any credit card)
https://scrapeops.io/app/dashboard


# Adding following lines in setttings.py file ->
DOWNLOADER_MIDDLEWARES = {

    ## Rotating User Agents -> pip install spider-user-agents
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,

    ## Rotating Free Proxies
    'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
    'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
}

## Copy/paste following line of code in your spider to use fake proxies ->
API_KEY = 'd99eff6b-ab58-4fdc-8664-68a4252c8edf'

def get_proxy_url(url):
    # logging.info(f'Scrape url:: {url}')
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?'+urlencode(payload)
    return proxy_url


# DOC LINK:: https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions
# DOC LINK:: https://shinesolutions.com/2018/09/13/running-a-web-crawler-in-a-docker-container/
# DOC LINK:: https://scrapeops.io/python-scrapy-playbook/scrapy-save-aws-s3/


## RUN DOCKER SERVER IN LOCAL SYSTEM ##
 >> docker run -p 9000:8080 travelportals_scrape_repo
 RUN BELOW TO STOP THE SERVER:
 >> docker kill 9000

## INVOKE DOCKER SERVER IN LOCAL SYSTEM ##
 >> curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
 RUN BELOW IN CASE OF FAILURE:
 >> Remove-item alias:curl

## DEPLOY DOCKER FROM LOCAL TO AWS ECR ##
 1. aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 294845879996.dkr.ecr.us-east-1.amazonaws.com
 2. docker build -t travelportals_scrape_repo .
 3. docker tag travelportals_scrape_repo:latest 294845879996.dkr.ecr.us-east-1.amazonaws.com/travelportals_scrape_repo:latest
 4. docker push 294845879996.dkr.ecr.us-east-1.amazonaws.com/travelportals_scrape_repo:latest

## Dokcer commands - ##
 ## Create docker image
   >> docker build -t travelportals_scrape_repo .
 ## Create docker container 
   >> docker run -d travelportals_scrape_repo
 ## Enter into docker container 
   >> docker exec -it 12980446b215  /bin/bash
 ## Command to remove all runinng and not running images in docker server ->
   >> docker rmi -f $(docker images -aq)
 ## Command to remove all runinng and not running image containers in docker server ->
   >> docker rm -f $(docker ps -aq)


## Exaample site to download mock data site ->
https://mockaroo.com/
https://s3.amazonaws.com/amazon-reviews-pds/readme.html

## Athena table name: tripadvisor_db.trip_advisor_hotels
## Athena table schema:->
HOTEL_NAME string, RATING string,  REVIEW_LEVEL string, REVIEW_COUNT string, AMENTINIES string, #FEATURES string,  HOTEL_LOCATION string, CONTACT_NUMBER string, NEARLY_LANDMARK_POINTS string, #HOTEL_PAGE_URL string, HOTEL_LISTING_PAGE_URL string


<!-- ssh-keygen -t rsa -b 4096 -C "sovan@dataengineeracademy.com" -->
<!-- git config --local user.name "sovan"
<!-- git config --local  user.email "sovan@dataengineeracademy.com" --> -->
<!-- git remote add origin git@github.com:deacademy/travelportals.git -->
