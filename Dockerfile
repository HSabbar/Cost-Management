FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt 
CMD ["python", "aws-s3.py", "&&", "python", "azure-api.py", "&&", "ls", "/app/data/"]
