# Dockerfile for Flask App
FROM python:3.9

WORKDIR /app

COPY . /app

# copz supervisor configurations
COPY serverConfig/supervisord.conf /etc/supervisord.conf


RUN apt-get update && apt-get install -y supervisor
# Install gunicorn
RUN pip install gunicorn

RUN pip install --no-cache-dir -r ./requirements.txt

RUN pip install pymysql mysqlclient

RUN pip install snakemake

RUN pip install Flask-Migrate


# this is for us to be able to execute supervisor for our server powered by Gunicorn.
COPY serverConfig/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# CMD ["gunicorn", "--log-level=debug", "-w 4", "-b 0.0.0.0:5000", "main:app"]
