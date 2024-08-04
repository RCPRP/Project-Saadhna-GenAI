# Install libraries
! pip3 install --upgrade --quiet google-cloud-aiplatform \
                                 langchain-google-vertexai \
                                 langchain
from google.cloud import aiplatform
import IPython

app = IPython.Application.instance()
app.kernel.do_shutdown(True)
import sys

# Additional authentication is required for Google Colab
if "google.colab" in sys.modules:
    # Authenticate user to Google Cloud
    from google.colab import auth

    auth.authenticate_user()

# Define project information
PROJECT_ID = "project-id"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}

# Initialize Vertex AI
import vertexai

vertexai.init(project=PROJECT_ID, location=LOCATION)
# Import libraries
from IPython.display import Markdown
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_vertexai import ChatVertexAI, HarmBlockThreshold, HarmCategory
from vertexai.generative_models import Content, GenerativeModel, Part
'''
Sending chat prompts using Vertex AI SDK for Python
Load the Gemini 1.0 Pro model
Gemini 1.0 Pro supports text and code generation from a text prompt.
'''
model = GenerativeModel("gemini-1.0-pro")
#Use a conversation chain
model = ChatVertexAI(
    model_name="gemini-1.0-pro",
    convert_system_message_to_human=True,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    },
)

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a helpful soft skills trainer for kids aged 12-14 years creating a safe space to experiment their soft skills. Now the specific skills you have to develop is System: You are a helpful soft skills trainer for kids aged 12-14 years creating a safe space to experiment their soft skills. you are responsible for creating scenarios for these kids to make them understand about important soft skill as crtitical thinking. You have to give an open ended question based on the previous chat and guide the kid if they have said right response encourage them or kindly say how best to respons and ask them to respond back. you can have a maximum o 10 turns to make the kid understand and use this knowledge later. yu have to be very kind , encouraging and if the kid is using abusive language , tell not to do so. keep your response very short and crisp and create your questions arounf it you are responsible for creating scenarios for these kids to make them understand about important soft skill as crtitical thinking. You have to give an open ended question based on the previous chat and guide the kid if they have said right response encourage them or kindly say how best to respons and ask them to respond back. you can have a maximum o 5 turns to make the kid understand and use this knowledge later. yu have to be very kind , encouraging and if the kid is using abusive language , tell not to do so. keep your response very short and crisp less than 50 words . You have to use fascinating , exciting tone throughout with a magical touch as you are talking to kids. you have a right solution in mind initially but dont reveal it and encourage the kid to think and derive to it in a fun and kind way . start the conversation like hi. you have to strictly create scenarios and question on very relatable daily events including people they say in their daily life and the probems that any kids would face that is very very relatable "
        ),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)

memory = ConversationBufferMemory(memory_key="history", return_messages=True)
conversation = ConversationChain(llm=model, prompt=prompt, verbose=True, memory=memory)

conversation.invoke(
    input="Hi! "
)
#Use the first ai response to create a visualisation using Imagen model 
from vertexai.preview.vision_models import ImageGenerationModel

imagen_model = ImageGenerationModel.from_pretrained("imagegeneration@005")
image_prompt = "Hi there! It's lovely to have you here today. Now, close your eyes and imagine you're at a magical picnic with your friends. The sun is shining, birds are singing, and the air smells like freshly baked cookies. Suddenly, you realize there aren't enough cookies for everyone! What do you do?"

response = imagen_model.generate_images(
    prompt=image_prompt,
)

response.images[0].show()


#try the below conversation flow
conversation.invoke("oh my god , i will break the cookies and share")
conversation.invoke("I will inform my teacher")
conversation.invoke("share to my friends and say next time i will plan properly ")
conversation.invoke("I will count number of people attending and get extra cookies")
conversation.invoke("can you tell me how best to inform that there are less cookie at that moment")
conversation.invoke("wow , asweome thanks !")


