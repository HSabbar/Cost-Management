FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt 
EXPOSE 8050
ENV PORT 8050
#CMD exec gunicorn --bind :$PORT dashbord:app --workers 1 --threads 1 --timeout 60
CMD ["python", "dashbord.py" ]  #aws-s3.py ; python azure-api.py ; ls /app/data/; python dashbord.py