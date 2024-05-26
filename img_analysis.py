from dotenv import load_dotenv
import google.generativeai as genai
import os
import PIL.Image


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro-vision")

img = PIL.Image.open('imgs\\26.earth.jpg')

while True:
    query = input("Enter your query: ")
    if query == "exit":
        break
    response = model.generate_content([query, img], stream=True)
    response.resolve()
    print("Response: ",response.text,'\n')


