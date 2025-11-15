import mongoengine
from configparser import ConfigParser
from pathlib import Path

config = ConfigParser()
config.read(Path(__file__).parent / "config.ini")

user = config.get("DB", "user")
password = config.get("DB", "pass")
db_name = config.get("DB", "db_name")
domain = config.get("DB", "domain")
app_name = config.get("DB", "app_name")

mongoengine.connect(
    host=f"mongodb+srv://{user}:{password}@{domain}/{db_name}?appName={app_name}",
    ssl=True
)