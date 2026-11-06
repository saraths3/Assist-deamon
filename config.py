from decouple import config
from google import genai

GEMINI_API_KEY = config('GEMINI_API_KEY')
DEFAULT_MODEL = config('DEFAULT_MODEL', default='gemini-2.5-flash')

client = genai.Client(api_key=GEMINI_API_KEY)