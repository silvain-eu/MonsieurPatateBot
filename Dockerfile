FROM  python:3.7-buster


WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY Commands ./Commands/
COPY Database ./Database/
COPY Utils ./Utils/

ENV token ""
ENV clientId ""
ENV voiceCategoryName "Salons vocaux"
ENV TZ="Europe/Paris"

CMD [ "python", "-u", "./main.py" ]