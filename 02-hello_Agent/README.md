[Open Google Collab Code🚀](https://colab.research.google.com/drive/1cUcrVPLoWAqD-gAiFmLqPrVWMgqJ49xH?usp=sharing)

### **Step 1: Libraries Import Karna**

```python
import chainlit as cl
import os
from agents import Agent,Runner,RunConfig,AsyncOpenAI,OpenAIChatCompletionsModel
from dotenv import load_dotenv,find_dotenv
```

#### **Kya Ho Raha Hai?**

* `chainlit` import kiya gaya hai jo chatbot interface ke liye use hota hai.
* `os` library import ki gayi hai taake environment variables ko access kar sakein.
* `agents` module se **5 cheezein** import ki gayi hain jo AI model ko run karne me madad karti hain:
  * `Agent` → Ek AI agent define karta hai jo response dega.
  * `Runner` → AI model ko execute karne ke liye.
  * `RunConfig` → Model ka configuration set karne ke liye.
  * `AsyncOpenAI` → OpenAI API ya Gemini API ke liye async client.
  * `OpenAIChatCompletionsModel` → AI ka specific model define karne ke liye.
* `.env` file se API key load karne ke liye `dotenv` library use ki gayi hai.

---

### **Step 2: API Key Load Karna**

```python
load_dotenv(find_dotenv())
gemini_api_key=os.getenv("key")
```

#### **Kya Ho Raha Hai?**

* `load_dotenv(find_dotenv())` **.env file** ko load karta hai jisme API keys hoti hain.
* `os.getenv("key")` **environment variable** se `"key"` naam ki value uthata hai (jo Google Gemini API key hai).

---

### **Step 3: AI Model Provide Karna (Provider)**

```python
provider=AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
```

#### **Kya Ho Raha Hai?**

* `AsyncOpenAI` ek **asynchronous client** hai jo AI model ko Gemini API se connect karega.
* `api_key=gemini_api_key` → Isme **Google Gemini API key** di ja rahi hai.
* `base_url="https://generativelanguage.googleapis.com/v1beta/openai/"` → **Google Gemini API ka endpoint** diya gaya hai.

---

### **Step 4: Model Define Karna**

```python
model=OpenAIChatCompletionsModel(
    model = "gemini-2.5-pro-exp-03-25",
    openai_client=provider,
)
```

#### **Kya Ho Raha Hai?**

* `OpenAIChatCompletionsModel` use ho raha hai taake AI ka **Gemini-2.5 Pro Model** define kiya ja sake.
* `model = "gemini-2.5-pro-exp-03-25"` → Ye specific Gemini AI model hai jo hum use kar rahe hain.
* `openai_client=provider` → Isko humne **provider** diya jo pehle define kiya tha.

---

### **Step 5: AI Model ka Configuration Set Karna**

```python
config=RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)
```

#### **Kya Ho Raha Hai?**

* `RunConfig` AI model ka **configuration set** karne ke liye use ho raha hai.
* `model=model` → Jo model humne define kiya tha, wahi yahan diya ja raha hai.
* `model_provider=provider` → Isme **AI API provider** diya gaya hai.
* `tracing_disabled=True` → AI model ke tracking ko **disable** kar diya gaya hai.

---

### **Step 6: Agent Create Karna**

```python
agent1=Agent(
    instructions="""1) you only have to answer in roman urdu 
    2) if someone ask you to answer in english or other language 
    then you have to told them that you cant 
    3) user can ask questions in other languages like english urdu or else but you have to reply their questions in roman urdu""",
    name="my roman urdu chatbot",
)
```

#### **Kya Ho Raha Hai?**

* `Agent` ek AI agent hota hai jo **instructions** follow karta hai.
* `instructions` ke andar **3 rules** diye gaye hain:
  1. Sirf **Roman Urdu** me answer dena hai.
  2. Agar koi **English ya doosri language** me jawab maange, toh batao ke ye mumkin nahi.
  3. User kisi bhi language me sawaal puch sakta hai (English, Urdu, etc.), lekin AI sirf **Roman Urdu** me reply karega.
* `name="my roman urdu chatbot"` → AI agent ka naam diya gaya hai.

---

### **Step 7: Chatbot Start Hone Par Message Send Karna**

```python
@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history",[])
    await cl.Message(content="Hello I Am Roman Urdu Chatbot Instructed by Shaheer Ahmad").send()
```

#### **Kya Ho Raha Hai?**

* `@cl.on_chat_start` → Jab **chatbot start** hoga, yeh function run hoga.
* `cl.user_session.set("history",[])` → Ek **empty history** list banayi gayi hai jo messages ko store karegi.
* `await cl.Message(content="Hello I Am Roman Urdu Chatbot Instructed by Shaheer Ahmad").send()`
  * Yeh **pehla message** bhejta hai jab chatbot start hota hai.

---

### **Step 8: User Ke Message Ka Jawaab Dena**

```python
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
```

#### **Kya Ho Raha Hai?**

1. `@cl.on_message` → Jab  **user koi message bhejta hai** , yeh function run hoga.
2. `history=cl.user_session.get("history")`
   * Pichle **messages ka history** retrieve kiya gaya hai.
3. `history.append({"role":"user","content":message.content})`
   * **User ka message** history me add kiya gaya.
4. `result=await Runner.run(agent1, input=history, run_config=config)`
   * **AI Model run** ho raha hai aur user ka input diya ja raha hai.
5. `history.append({"role":"assistant","content":result.final_output})`
   * **AI ka jawab** history me add kiya gaya.
6. `cl.user_session.set("history",history)`
   * Updated **history save** kar di gayi.
7. `await cl.Message(content=result.final_output).send()`
   * **AI ka jawab bhej diya gaya** chatbot me.

---

### **Final Summary**

1. **Google Gemini API connect ki gayi.**
2. **Roman Urdu chatbot ka AI model banaya gaya.**
3. **Sirf Roman Urdu me jawab dene ke liye instructions di gayi.**
4. **Chatbot start hone par welcome message bheja gaya.**
5. **User ke message ka jawab AI model se generate karke bheja gaya.**
