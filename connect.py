from mongoengine import connect
import configparser
import pathlib


file_config = pathlib.Path(__file__).parent.joinpath("config.ini")

config = configparser.ConfigParser()
config.read(file_config)

mongo_user = config.get("mongodb", "user")
mongodb_pass = config.get("mongodb", "password")
domain = config.get("mongodb", "domain")
db_name = config.get("mongodb", "db_name")

connect(host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority")
