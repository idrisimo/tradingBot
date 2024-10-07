import openai
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()
api_key = os.environ['GPT_API_KEY']

openai.api_key = api_key


class GPTController:
    def __init__(self):
        pass
    
    def
