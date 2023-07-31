FROM python:3.9-slim

WORKDIR /weather

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
#RUN python populate_mongo_data.py

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5001

CMD ["flask", "run", "--port", "5001"]
