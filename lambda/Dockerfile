FROM public.ecr.aws/lambda/python:3.9
ARG UNAME=root

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN yum update && \
    pip3 install -r requirements.txt --target /var/task/modules
COPY ./modules /var/task/modules

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]
