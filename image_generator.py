# import required libraries
import openai


openai.api_key = "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"

response = openai.Image.create(
  prompt="royale toilet",
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']
print(image_url)
