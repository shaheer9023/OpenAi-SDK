[Google Colab Link](https://colab.research.google.com/drive/1MPuMX_BP1M8mHL5KVaOS-JRrozR2MDR1?usp=sharing)

Doremon Chatbot Explanation

Socho aap ne ek chatbot banaya jo har user ke sawal ka jawab deta hai — jaise:

> 🧑‍💻 User: "Doremon, time machine kaise kaam karti hai?"

> 🤖 Doremon Bot (Gemini AI se): "Time machine ek aisi device hai jo waqt ke saath travel karne mein madad karti hai..."

Yeh **AI chatbot** Gemini API ka use kar raha hai jo Google ka powerful language model hai — and **Chainlit** uska front-end chat interface banata hai (WhatsApp jaisa).

---

### ✅ **1. Load Environment and API Key**

```python
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("gemini_api_key")
```

🔸 **Real Life Example:**

Jese aap Doremon ka secret code (password) ek diary mein likh ke rakhte ho. Jab zarurat ho, aap diary se nikal ke use karte ho — lekin direct kisi ko nahi batate.

👉 Waise hi, `.env` file mein Gemini ki secret key hoti hai jo yahaan load ho rahi hai.

---

### ✅ **2. Setup Gemini AI Provider**

```python
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
```

🔸 **Real Life Example:**

Socho Doremon ke paas Google ka ek **phone number** hai jahan se woh information mangwa sakta hai.

Yeh `provider` uss phone number ko use karke Gemini API se baat karta hai.

---

### ✅ **3. Model Selection**

```python
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-pro-exp-03-25",
    openai_client=provider,
)
```

🔸 **Real Life Example:**

Jese Doremon ke paas alag alag gadgets hote hain, waise hi Google ke paas bhi AI ke alag alag models hote hain.

Aap yahan **"gemini-2.5-pro"** gadget select kar rahe ho taake best result mile.

---

### ✅ **4. Configuration Setup**

```python
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)
```

🔸 **Real Life Example:**

Jese Nobita ne Doremon ko bola:

> "Sirf mujhe hi jawab dena, aur sab kuch private rakhna!"
>
> Waise hi, yahaan bola gaya ke:

* Ye model use karo
* Ye provider use karo
* **Tracing (recording)** band rakho (private chat)

---

### ✅ **5. Agent = Doremon's Personality**

```python
agent1 = Agent(
    instructions="you are helpful Ai Assistant",
    name="my chatBOT",
)
```

🔸 **Real Life Example:**

Jese Doremon ko bola gaya:

> "Tum helpful assistant ho. Tumhara naam 'Doremon Bot' hai."

Yahaan bhi agent ko define kiya gaya hai:

* Kya kaam kare
* Naam kya ho

---

### ✅ **6. User ne Pehli Baar Chat Start Kiya**

```python
@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="me hoon doremon mere ps hr sawal ka jawab h 😂").send()
```

🔸 **Real Life Example:**

Jese jab koi naya user app kholta hai, to Doremon greet karta hai:

> "Me hoon Doremon! Mujhe kuch bhi poochho!"

* History set ho jaati hai taake baad mein uska context yaad rahe
* Message bheja jaata hai as welcome message

---

### ✅ **7. Jab User Sawal Pooche (Message Send Kare)**

```python
@cl.on_message
async def handle_message(message: cl.Message):
```

🔸 **Real Life Example:**

User ne likha:

> "Doremon, tumhara sabse pasandida gadget kya hai?"

---

#### 🔸 Step 1: Purani History Lo

```python
history = cl.user_session.get("history")
```

➡️ Doremon ko purani baat yaad dila rahe hain — jese pehle kya discussion hua tha.

---

#### 🔸 Step 2: Ek Khaali Message Bana Ke Bhejo

```python
msg = cl.Message(content="")
await msg.send()
```

➡️ Ek khaali bubble screen pe show hota hai — jese "typing..." indicator

---

#### 🔸 Step 3: User ka Message Add Karo

```python
history.append({"role": "user", "content": message.content})
```

➡️ Ye message list mein add ho gaya:

`[{"role": "user", "content": "tumhara fav gadget kya hai?"}]`

---

#### 🔸 Step 4: AI ko Bhejo Sawal + History

```python
result = Runner.run_streamed(
    agent1,
    input=history,
    run_config=config,
)
```

➡️ Doremon (AI) ko user ka sawal aur poori history bheji gayi taake wo achha jawab de.

---

#### 🔸 Step 5: Gemini ka Response Live Stream Karo

```python
async for event in result.stream_events():
    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        await msg.stream_token(event.data.delta)
```

➡️ Doremon har lafz type karta jaata hai — jaise:

```
"Doremon: Mera fav gadget 'Anywhere Door' hai jo kahin bhi le ja sakta hai."
```

Yeh live typing jaise dikhata hai.

---

#### 🔸 Step 6: Final Answer Save Karo

```python
history.append({"role": "assistant", "content": result.final_output})
cl.user_session.set("history", history)
```

➡️ Doremon ka jawab bhi yaad rakha jaata hai taake agli baar context mile.

---

## ✅ **Final Result Example Flow**

```
🧑 User: "Hi Doremon!"
🤖 Doremon: "me hoon doremon mere ps hr sawal ka jawab h 😂"

🧑 User: "Fav gadget kya hai?"
🤖 Doremon: "Mujhe Anywhere Door sabse zyada pasand hai!"
```

---

## 🔚 Summary in Easy Words:

| Code Part                 | Real-Life Example                        |
| ------------------------- | ---------------------------------------- |
| `.env`+`getenv()`     | Doremon ka secret code diary se lena     |
| `provider`              | Google se baat karne wala phone line     |
| `model`                 | Doremon ka brain (Gemini model)          |
| `agent`                 | Doremon ki personality aur naam          |
| `history`               | Pichli baatein yaad rakhna               |
| `Runner.run_streamed()` | Google se live jawab lena                |
| `stream_token()`        | Typing effect dikhana                    |
| `cl.on_message`         | User ke har sawal pe AI ka response dena |

---
