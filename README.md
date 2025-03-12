# MOVIE API

## Local Environment Setup

### Prerequisites

- Python 3.10.14
- [pyenv](https://github.com/pyenv/pyenv)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
- Docker (for Redis containerization)

### Installation

1. **Install Python 3.10.14 and set up the virtual environment:**

    ```bash
    pyenv install 3.10.14
    pyenv virtualenv 3.10.14 moviedb_venv
    pyenv activate moviedb_venv
    ```

2. **Install Python requirements:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Create and configure the environment file:**

    ```bash
    cp .env.template .env
    ```

    Edit the `.env` file with your credentials.

### Redis Setup

To run Redis, use the following Docker command:

```bash
docker run --restart unless-stopped --name  movie_redis -p 6379:6379 -d redis:7.0-alpine
```

### Running Tests
```bash
pytest --cache-clear --capture=no --showlocals --verbose  --cov-report=html
```

#### How to run locally

 ```bash
python run.py
```

## API Reference
All endpoints require JWT authentication via Bearer token in the Authorization header.

Endpoints


1. Retrieve Favorite Movies
```bash
curl --location 'http://127.0.0.1:5000/movies/favorites' \
--header 'Authorization: Bearer 1234567890'
```

2. Add movie to favorites
```bash
curl --location 'http://127.0.0.1:5000/movies/favorites' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer 1234567890' \
--data '{
  "release_date": "2025-03-12",
  "id": 1234,
  "title": "Gladiator"

}'
```

3. Remove movie from favorites
```bash
curl --location --request DELETE 'http://127.0.0.1:5000/movies/favorites/3423' \
--header 'Authorization: Bearer 1234567890'
```

4. Update movie rating
```bash
curl --location --request PATCH 'http://127.0.0.1:5000/movies/favorites/343245323' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer 1234567890' \
--data '{
"rating":9

}'
```

5. Admin delete all movies by user_id
```bash
curl --location --request DELETE 'http://127.0.0.1:5000/admin/users/2/favorites' \
--header 'Authorization: Bearer abcdef1234567890'
```

6. Retrieve movies popular
```bash
curl --location 'http://127.0.0.1:5000/movies/popular'
```