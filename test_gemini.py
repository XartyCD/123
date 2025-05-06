import google.generativeai as genai

genai.configure(api_key="AIzaSyAu-NpbHQfJZT4h4W9Qdn9BjrFFkm4SPeU")


model = genai.GenerativeModel("models/gemini-1.5-flash")
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)

response = model.generate_content("Привет, кто ты?")
print(response.text)