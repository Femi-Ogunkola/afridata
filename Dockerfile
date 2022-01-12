FROM ubuntu:20.04
RUN mkdir function
RUN cd function
COPY code/lambda_function.py function/lambda_function.py
COPY code/ function/
WORKDIR /function
RUN apt-get update
RUN apt-get install python3-pip -y
RUN apt-get install zip -y
RUN pip install -t . pymongo
RUN pip install -t . dnspython
RUN pip install -t . pandas
RUN zip -r linux-lambda.zip *