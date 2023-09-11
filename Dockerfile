FROM public.ecr.aws/lambda/python:3.11

# Set the working directory to {LAMBDA_TASK_ROOT} = '/var/task'
WORKDIR ${LAMBDA_TASK_ROOT}

#Copy the file from the local host to the filesystem of the container at the working directory.
COPY requirements.txt .
#Install Scrapy specified in requirements.txt.
RUN pip3 install --no-cache-dir -r requirements.txt

#scrape all files in root directory
COPY . .

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD ["lambda_function.handler"]

