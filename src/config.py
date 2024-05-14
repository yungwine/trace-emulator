import json
import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv('USING_DOCKER'):
    CONFIG_PATH = 'config.json'
else:
    CONFIG_PATH = os.getenv('CONFIG_PATH')
with open(CONFIG_PATH, 'r') as f:
    CONFIG = json.load(f)

MAX_REQ_PER_PEER = int(os.getenv('MAX_REQ_PER_PEER', 30))

LOGGING = os.getenv('LOGGING', 'INFO')
EMULATION_CACHE_SEC = os.getenv('EMULATION_CACHE_SEC', 3)
