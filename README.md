# CoinScrapper

## How to start for development:

1. Make python environment
```bash
python3 -m venv env
source env/bin/activate
```

2. Initiate DB.
```bash
# Install Postgresql
psql -d postgres -U postgres -W
create database coin_scrapper;
create user coin_scrapper;
alter role coin_scrapper with passwsord='';
grant ALL privileges on database coin_scrapper to coin_scrapper;
alter role coin_scrapper login;
```

3. Install Redis
[here are the instructions](https://redis.io/)

4. Get membership or free trial from proxymesh.
This step is optional, but proxymesh allows us to fake our ip to anywhere in the world for each run.
This way we avoid getting our ip banned from scraping.

5. Initiate .env
```bash
CHROMEDRIVER_PATH=""
CHROME_BINARY_PATH=""
secret_key=""

postgres_db_name=""
postgres_db_username=""
postgres_db_password=""

# for proxys if not using comment this part out in scrapper.py as well.
HOSTNAME=""
PORT=""

LOGS_PATH="/var/logs/CoinScrapper"

```

6. Run python server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver localhost:8000
```
