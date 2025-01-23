import ollama
import os
import re
client  = ollama.Client(host='http://localhost:11434')
model = "llama3.2-vision:latest"

res = client.chat(
	model=model,
	messages=[
		{
			'role': 'user',
			'content': 'Solve the math problem in this image:',
			'images': [os.getcwd() +  '/images/math.png']
		}
	]
)

print(res.message.content)