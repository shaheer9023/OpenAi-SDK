import chainlit as cl
import os
from agents import Agent,Runner,RunConfig,AsyncOpenAI,OpenAIChatCompletionsModel
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
gemini_api_key=os.getenv("key")

# step 1 
provider=AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
# step 2
model=OpenAIChatCompletionsModel(
    model = "gemini-2.5-pro-exp-03-25",
    openai_client=provider,
)
# configure: Run Level
config=RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)
# step 3
agent1=Agent(
    instructions="""1) you only have to answer in roman urdu 
    2) if someone ask you to answer in english or other language 
    then you have to told them that you cant 
    3) user can ask questions in other languages like english urdu or else but you have to reply their questions in roman urdu""",
    name="my roman urdu chatbot",
    
)
# setp 4 RUN
# result=Runner.run_sync(
#     input="tell me about yourself",
#     run_config=config,
#     starting_agent=agent1

# )
# print(result)
@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history",[])
    await cl.Message(content="Hello I Am Roman Urdu Chatbot Instructed by Shaheer Ahmad").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history=cl.user_session.get("history")
    history.append({"role":"user","content":message.content})
    result=await Runner.run(
        agent1,
        input=history,
        run_config=config,
    )
    history.append({"role":"assistant","content":result.final_output})
    cl.user_session.set("history",history)

    await cl.Message(content=result.final_output).send()