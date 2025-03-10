# the_movie_db_test


## Local environment setup

Install Python 3.10.14 & setup virtual environment. I recommend to use [pyenv](https://github.com/pyenv/pyenv) and
[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

```bash
pyenv install 3.10.14
pyenv virtualenv 3.10.14 moviedb_venv
pyenv activate moviedb_venv
```

**Create environment file**:
   ```bash
   cp .env.template .env
   ```
   Edit the `.env` file with your credentials.