## DBT LEARNING

If there is any existing container that you want not to run:
```
docker-compose down -v
```
The flag -v is for "volume"

Before running:
```
docker-compose up -d
```
The flag -d is for

Running debug (or any other dbt command):
```
docker-compose run --rm dbt debug
```

docker-compose run --rm dbt show --select top_rated_apps

docker-compose exec postgres psql -U dbt -d app_reviews -c "SELECT * FROM analytics.top_rated_apps;"