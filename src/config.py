import json
import os
from dotenv import load_dotenv

load_dotenv()

CONFIG_PATH = os.getenv('CONFIG_PATH')
with open(CONFIG_PATH, 'r') as f:
    CONFIG = json.load(f)

MAX_REQ_PER_PEER = os.getenv('MAX_REQ_PER_PEER', 30)
