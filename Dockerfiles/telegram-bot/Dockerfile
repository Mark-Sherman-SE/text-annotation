FROM python:3.10

COPY requirements.txt .
COPY bot_animation.py .
COPY config.yaml .
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r requirements.txt
CMD [ "python", "./bot_animation.py" ]