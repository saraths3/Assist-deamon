
from decouple import config
from google import genai


GEMINI_API_KEY = config('GEMINI_API_KEY')


client = genai.Client(api_key = GEMINI_API_KEY)
interaction = client.interactions.create(
    model = 'gemini-3.5-flash',
    input = "describe a creeper? (malayalam) 40 words."
)
print(interaction.output_text)