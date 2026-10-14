
import ollama

reponse = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Réponds en français : que peux-tu faire ?"
        }
    ]
)

print(reponse["message"]["content"])
