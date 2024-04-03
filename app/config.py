from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("DB_URL")
api = os.getenv("DB_API_KEY")
