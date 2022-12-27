import os


# def get_postgres_uri():
#     host = os.environ.get("DB_HOST", "localhost")
#     port = 54321 if host == "localhost" else 5432
#     password = os.environ.get("DB_PASSWORD", "abc123")
#     user, db_name = "allocation", "allocation"
#     return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

def get_mariadb_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 3306 if host == "localhost" else 3306
    password = os.environ.get("DB_PASSWORD", "1234")
    user, db_name = "root", "test"
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"


def get_mongodb_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 27017 if host == "localhost" else 27017
    return f'mongodb://{host}:{port}'


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 80 if host == "localhost" else 80
    return f"http://{host}:{port}"
