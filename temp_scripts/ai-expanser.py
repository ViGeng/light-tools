"""Run this model in Python

> pip install openai
"""
import os

from openai import OpenAI

# To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings.
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"],
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful writing assistant. User will provide only the trigger text to be replaced. You should reply and return ONLY the replacement text according to the trigger text. E.g., date -> 2025-01-16, Thu, Prof. Li email beginning -> Dear Prof. Li, \n I hope you are doing well! I am writing to ..., end conversation -> I really enjoy our chat. But I got to go to bed. I will catch you up latter.",
        },
        {
            "role": "user",
            "content": "france capital?",
        }
    ],
    model="gpt-4o",
    temperature=1,
    max_tokens=4096,
    top_p=1
)

print(response.choices[0].message.content)
