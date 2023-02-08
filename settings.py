import os

from dotenv import load_dotenv

load_dotenv()

SIZE = WIDTH, HEIGHT = 1280, 720

DATABASE = os.environ.get('DATABASE', 'db.sqlite3')

IPv4 = os.environ.get('IPv4', '255.255.255.255')
