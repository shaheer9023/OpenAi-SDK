import os
import chainlit as cl
from dotenv import load_dotenv,find_dotenv
from agents import Agent, RunConfig,AsyncOpenAI,OpenAIChatCompletionsModel,Runner
from openai.types.responses import ResponseTextDeltaEvent
load_dotenv(find_dotenv())
gemini_api_key=os.getenv("gemini_api_key")
# step 1
provider=AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
# step 2 
model=OpenAIChatCompletionsModel(
    model="gemini-2.5-pro-exp-03-25",
    openai_client=provider,
)
# step 3
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)
agent1=Agent(
    instructions="you are helpful Ai Assistant",
    name="my chatBOT",
)

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history",[])
    await cl.Message(content="me hoon doremon mere ps hr sawal ka jawab h 😂").send()
@cl.on_message
async def handle_message(message:cl.Message):
    history=cl.user_session.get("history")
    msg=cl.Message(content="")
    await msg.send()
    history.append({"role":"user","content":message.content})
    result=Runner.run_streamed(
        agent1,
        input=history,
        run_config=config,
    )
    async for event in result.stream_events():
        if event.type=="raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)

    history.append({"role":"assistant","content":result.final_output})
    cl.user_session.set("history",history)        
