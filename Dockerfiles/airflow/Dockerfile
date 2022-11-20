FROM apache/airflow:2.4.2-python3.10
COPY requirements.txt .
COPY download_nltk_data.py .
USER airflow
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r requirements.txt
CMD [ "python", "./download_nltk_data.py" ]
