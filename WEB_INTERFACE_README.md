# DBT Tables Web Interface

This web interface allows you to view your dbt tables in a user-friendly web browser instead of using the terminal.

## Features

- **Dashboard**: View all available tables in your analytics schema
- **Table Viewer**: Browse table data with pagination and column information
- **Export**: Download table data as CSV
- **Real-time**: Refresh data without restarting containers
- **Responsive**: Works on desktop and mobile devices

## How to Use

### 1. Start the Services

```bash
# Build and start all services (PostgreSQL, dbt, and web interface)
docker-compose up --build

# Or start in detached mode
docker-compose up --build -d
```

### 2. Run Your DBT Models

```bash
# Run dbt models to create tables
docker-compose exec dbt dbt run

# Or run specific models
docker-compose exec dbt dbt run --models models_reviews top_rated_apps
```

### 3. Access the Web Interface

Open your web browser and go to:
```
http://localhost:5000
```

### 4. View Your Tables

- **Dashboard**: See all available tables at `http://localhost:5000`
- **Specific Table**: View individual table data at `http://localhost:5000/table/{table_name}`

## Available Tables

Based on your current dbt models, you should see:

1. **models_reviews**: Cleaned app reviews with non-null review texts
2. **top_rated_apps**: Top 3 apps by average rating with review statistics

## API Endpoints

The web interface also provides REST API endpoints:

- `GET /api/tables` - List all tables
- `GET /api/table/{table_name}` - Get table data as JSON

## Troubleshooting

### No Tables Showing
If you don't see any tables:
1. Make sure dbt models have been run: `docker-compose exec dbt dbt run`
2. Check if tables exist in the analytics schema
3. Verify PostgreSQL connection

### Web Interface Not Loading
1. Check if the web container is running: `docker-compose ps`
2. Check logs: `docker-compose logs web`
3. Ensure port 5000 is not in use by another application

### Database Connection Issues
1. Verify PostgreSQL is running: `docker-compose ps`
2. Check PostgreSQL logs: `docker-compose logs postgres`
3. Ensure the database is properly initialized

## Stopping the Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: This will delete your data)
docker-compose down -v
```

## Development

To modify the web interface:
1. Edit files in the current directory
2. The web container will automatically reload changes
3. Refresh your browser to see updates
