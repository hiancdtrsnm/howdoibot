FROM python:3.6


RUN mkdir -p /home/howdoibot
WORKDIR /home/howdoibot

COPY requirements.txt requirements.txt
#RUN python -m venv venv
RUN pip install -r requirements.txt

RUN pip install path.py
COPY howdoibot.py howdoibot.py

# run-time configuration
# EXPOSE 5000
# ENTRYPOINT ["python howdoibot.py"]
