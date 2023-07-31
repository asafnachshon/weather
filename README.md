# Weather App


## Prerequisites

- Docker
- Docker Compose

## Instructions

### 1. Run Docker Compose and Populate MongoDB Data

Build and start the Docker containers for the Flask Weather App and MongoDB.

```bash
docker-compose up --build
```

`populate_mongo_data.py`: automatically populates MongoDB with initial weather data.


### 2. Usage and API Endpoints

#### API Endpoints

##### `GET http://localhost:5001/avg_tmp_per_city_per_day`

Retrieves the average temperature per city per day.

##### `GET http://localhost:5001/lowest_humid`

Returns the lowest humidity recorded across all locations and dates in the database.

##### `GET http://localhost:5001/feels_like_rank`

Provides a ranking of cities based on the farthest "feels-like" temperature.

- Use the `order_dir` parameter (optional) to specify the order of the ranking.
- Use `order_dir=desc` for descending order.
- Use `order_dir=asc` for ascending order.
