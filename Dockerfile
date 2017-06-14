FROM buildpack-deps:xenial

RUN apt-get -y update && apt-get install -y --no-install-recommends python-pip

RUN pip install --upgrade pip
RUN pip install -U setuptools

WORKDIR /wikiapp

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]
