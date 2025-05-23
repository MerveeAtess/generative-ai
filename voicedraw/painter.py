"""
1.txt-img : DALL-E 3
2.txt+img - img :Gemini Vision Pro
3.çatı metod : DALL-E AND GEMINI VISION PRO
"""
import google.generativeai as genai
import PIL.Image #geminiai image import
import requests #dall-e resim üretme
import os
from dotenv import load_dotenv
from openai import OpenAI
from io import BytesIO
from datetime import datetime

load_dotenv()

my_key_openai = os.getenv("openai_apikey")

client = OpenAI(
    api_key=my_key_openai
)

#ilk resim üretme
def generate_image_with_dalle(prompt):

    AI_Response = client.images.generate(
        model = "dall-e-3",
        size = "1024x1024",
        quality = "hd",
        n = 1,
        response_format = "url", 
        prompt = prompt
    )
    
    image_url = AI_Response.data[0].url

    response = requests.get(image_url)
    image_bytes = BytesIO(response.content)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"./img/generated_image_{timestamp}.png"

    if not os.path.exists("./img"):
        os.makedirs("./img")
    
    #resmi yerelde kaydetme 
    with open(filename, "wb") as file:
        file.write(image_bytes.getbuffer())

    return filename

#çoklu form: txt+img - img
my_key_google = os.getenv("google_apikey")

genai.configure(
    api_key=my_key_google
)

def gemini_vision_with_local_file(image_path, prompt):

    multimodality_prompt = f"""Bu gönderdiğim resmi, bazı ek yönergelerle birlikte yeniden oluşturmanı istiyorum.
    Bunun için ilk olarak resmi son derece ayrıntılı biçimde betimle. Daha sonra sonucunda bana vereceğin metni, bir yapay zeka
    modelini kullanarak görsel oluşturmakta kullanacağım. O yüzden yanıtına son halini verirken bunun resim üretmekte kullanılacak bir
    girdi yani prompt olduğunu dikkate al. İşte ek yönerge şöyle: {prompt}
    """

    client = genai.GenerativeModel(model_name="gemini-pro-vision")
   
    #kaynak resim-adres dışarıdan verilecek
    source_image = PIL.Image.open(image_path)

    #liste göndererek txt ve img promptlar
    AI_Response = client.generate_content(
        [
            multimodality_prompt,
            source_image
        ]
    )

    AI_Response.resolve()

    return AI_Response.text

#3. aşama - txtten img oluşturma tekrar göndererek yapılır
#çatı metod

def generate_image(image_path, prompt):

    image_based_prompt = gemini_vision_with_local_file(image_path=image_path, prompt=prompt)
    
    filename = generate_image_with_dalle(prompt=image_based_prompt)

    return filename