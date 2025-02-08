#Setting up the API key 
import os 
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

#Encoding the image
import base64
def encode_image(image_path):
    image_file=open(image_path,'+rb')
    encoded_image=base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image



#Setup the multi-modal LLM
from groq import Groq
model="llama-3.2-90b-vision-preview"

def analyze_image_with_query(query, model, encoded_image):
    client=Groq()  
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }]
    chat_completion=client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content
