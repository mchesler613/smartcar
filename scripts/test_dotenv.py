import os
from dotenv import load_dotenv


def run():
    load_dotenv()
    print(os.getenv('SECRET_KEY'))
    print(os.getenv('SMARTCAR_CLIENT_ID'))
