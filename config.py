from dotenv import dotenv_values
env = dotenv_values(".env")
class Config:
    MYSQL_USERNAME = env["MYSQL_USERNAME"]
    MYSQL_PASSWORD = env["MYSQL_PASSWORD"]
    MYSQL_HOST = env["MYSQL_HOST"]
    MYSQL_PORT = env["MYSQL_PORT"]
    MYSQL_DB = env["MYSQL_DB"]
    JWT_SECRET_KEY = env["JWT_SECRET_KEY"]
    AUTHENTICATION_KEY = env["AUTHENTICATION_KEY"]
    JWT_TOKEN_LOCATION = [env["JWT_TOKEN_LOCATION"]]
    APP_HOST = env["APP_HOST"]