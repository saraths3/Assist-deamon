
# from decouple import config
# from google import genai


# GEMINI_API_KEY = config('GEMINI_API_KEY')


# client = genai.Client(api_key = GEMINI_API_KEY)
# interaction = client.interactions.create(
#     model = 'gemini-3.5-flash',
#     input = "describe a creeper? (malayalam) 40 words."
# )
# print(interaction.output_text)

# **************************************

# from google import genai
# from decouple import config

# client = genai.Client(api_key=config('GEMINI_API_KEY'))
# chat = client.chats.create(model="gemini-3.5-flash")

# print("Chat started! Type 'exit' to quit.\n")

# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ["exit", "quit"]:
#         print("Ending chat session.")
#         break
        
#     if not user_input.strip():
#         continue

#     # send_message appends user_input and returns the updated chat response
#     response = chat.send_message(user_input)
#     print(f"Gemini: {response.text}\n")

# ****************************************

from google import genai
from decouple import config
from google.genai.errors import APIError  # For catching potential API errors

client = genai.Client(api_key=config('GEMINI_API_KEY'))
# Note: Ensure you use an active model name such as "gemini-2.5-flash" or similar current production endpoints
chat = client.chats.create(model="gemini-3.5-flash")

print("Chat started! Type 'exit' to quit.\n")

try:
    while True:
        user_input = input("You: ")
        
        # Check exit conditions
        if user_input.lower() in ["exit", "quit"]:
            print("Ending chat session.")
            break
            
        # Ignore empty lines
        if not user_input.strip():
            continue

        try:
            # send_message appends user_input and returns the updated chat response
            response = chat.send_message(user_input)
            print(f"Gemini: {response.text}\n")
            
        except APIError as e:
            print(f"\n[API Error]: {e}. Please try your message again.\n")
        except Exception as e:
            print(f"\n[Unexpected Error]: {e}\n")

except KeyboardInterrupt:
    print("\nEnding chat session via keyboard interrupt. Goodbye!")
