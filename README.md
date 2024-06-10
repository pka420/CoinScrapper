# CoinScrapper

## Demo

  https://github.com/pka420/CoinScrapper/assets/30459586/b6f798c5-0871-4dcd-85bb-739707f8c705


1. Create a job.
![image](https://github.com/pka420/CoinScrapper/assets/30459586/543dba60-e55a-474c-bc5f-5ffdff287e54)

2. Check Status

Not Completed:
![image](https://github.com/pka420/CoinScrapper/assets/30459586/269787cc-ea48-46da-882e-20f135fc73b7)

Completed: 
![image](https://github.com/pka420/CoinScrapper/assets/30459586/9beb407c-8d96-4d1c-bbc9-5a4ed5bc1356)

Failed:
![image](https://github.com/pka420/CoinScrapper/assets/30459586/1fb39eb5-c1af-4673-830f-0c72c604e6f6)



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

