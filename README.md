# MOVIE API

## Overview
The **Movie API** provides a robust and efficient way to manage user-favorite movies, update ratings, and retrieve popular movie data. The API enforces authentication via JWT tokens for secure access.

## Local Environment Setup

### Prerequisites
Ensure you have the following dependencies installed before proceeding:

- **Python 3.10.14**
- [pyenv](https://github.com/pyenv/pyenv) (Python version management)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) (Virtual environment management)
- **Docker** (for Redis containerization)

### Installation
Follow these steps to set up the project locally:

1. **Install Python 3.10.14 and set up a virtual environment:**

    ```bash
    pyenv install 3.10.14
    pyenv virtualenv 3.10.14 moviedb_venv
    pyenv activate moviedb_venv
    ```

2. **Install project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the environment configuration:**

    ```bash
    cp .env.template .env
    ```
    
    Update the `.env` file with the required credentials and configurations.

### Redis Setup
To run Redis locally using Docker, execute the following command:

```bash
docker run --restart unless-stopped --name movie_redis -p 6379:6379 -d redis:7.0-alpine
```

## Running Tests
Run the test suite using the following command:

```bash
python -m pytest --cache-clear --capture=no --showlocals --verbose --cov-report=html
```

## Running the API Locally
To start the API server, execute:

```bash
python run.py
```

## API Reference
All API endpoints require JWT authentication using a Bearer token in the `Authorization` header.

### Endpoints

#### 1. Retrieve Favorite Movies
```bash
curl --location 'http://127.0.0.1:5000/favorites' \
--header 'Authorization: Bearer <your_token>'
```

#### 2. Add a Movie to Favorites
```bash
curl -X 'POST' \
  'http://localhost:5000/users/2/favorites' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <your_token>' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 123,
  "title": "The Dark Knight",
  "release_date": "2018-05-20"
}'
```

#### 3. Remove a Movie from Favorites
```bash
  curl -X 'DELETE' \
  'http://localhost:5000/users/2/favorites/123' \
  -H 'Authorization: Bearer <your_token>'
```

#### 4. Update Movie Rating
```bash
curl -X 'PATCH' \
  'http://localhost:5000/users/2/favorites/123' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <your_token>' \
  -H 'Content-Type: application/json' \
  -d '{
  "rating": 4
}''
```

#### 5. Admin: Delete All Movies by User ID
```bash
curl -X 'DELETE' 'http://127.0.0.1:5000/admin/users/2/favorites' \
  -H 'Authorization: Bearer <your_token>' \
```

#### 6. Retrieve Popular Movies
```bash
curl --location 'http://127.0.0.1:5000/movies'
```

---
