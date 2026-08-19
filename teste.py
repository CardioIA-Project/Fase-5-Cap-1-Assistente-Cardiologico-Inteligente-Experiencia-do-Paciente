import os
from dotenv import load_dotenv

load_dotenv
valor = os.getenv('WATSON_ASSISTANT_ID')
print(valor)