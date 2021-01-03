From python:3.9.0-buster

WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg

COPY . .
CMD ["find_word_audio.py"]
ENTRYPOINT ["python3"]
