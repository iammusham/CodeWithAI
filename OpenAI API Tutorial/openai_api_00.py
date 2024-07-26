from openai import OpenAI

openai_api_key = "your_openai_api_key"

model = "gpt-3.5-turbo"
client = OpenAI(api_key=openai_api_key)

while True:
  user_input = input("Ask me anything: ")
  messages = [{"role":"system","content":"Act as a Jarvis like assistant"},{"role":"user","content":user_input}]
  response = client.chat.completions.create(model=model,messages=messages,max_tokens=50)
  output = response.choices[0].message.content
  tokens = response.usage.total_tokens
  print(f"ChatGPT: {output}")
  print()
  print(f"Tokens used {tokens}")
  print()