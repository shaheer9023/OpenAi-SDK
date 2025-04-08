[Google Colab Link](https://colab.research.google.com/drive/1MPuMX_BP1M8mHL5KVaOS-JRrozR2MDR1?usp=sharing)


# Explanation

---

## ✅ **1. Load Environment and API Key**

```python
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("gemini_api_key")
```

🧠 **Explanation (Roman Urdu):**

* `load_dotenv()` `.env` file load karta hai — jisme sensitive cheezein hoti hain (like API key).
* `find_dotenv()` automatically `.env` file ko locate karta hai.
* `os.getenv("gemini_api_key")` se `.env` file ke andar se `"gemini_api_key"` nikal ke `gemini_api_key` variable mein store ki jaati hai.

> Ye isliye hota hai taake key code mein na likhni pare (secure banane ke liye).

---

## ✅ **2. Setup Gemini AI Provider**

```python
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
```

🧠 **Explanation:**

* `AsyncOpenAI` ek class hai jo OpenAI-compatible async API banati hai.
* Hum isme `api_key` aur `base_url` dete hain — Gemini API se connect karne ke liye.

> Yahaan `base_url` Google ke Gemini ka endpoint hai.

---

## ✅ **3. Model Selection**

```python
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-pro-exp-03-25",
    openai_client=provider,
)
```

🧠 **Explanation:**

* `OpenAIChatCompletionsModel` ka object bana rahe hain.
* `"gemini-2.5-pro..."` model ka naam hai — jo hum use karna chahte hain.
* `openai_client=provider` matlab Gemini ke API connection se is model ko bind kar rahe hain.

---

## ✅ **4. Configuration Setup**

```python
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)
```

🧠 **Explanation:**

* `RunConfig` mein hum batate hain ke:
  * Kaunsa model use ho
  * Kaunsa provider use ho
  * Tracing (logging) band ho — taake private rakha ja sake

---

## ✅ **5. Agent = AI Bot Banaya**

```python
agent1 = Agent(
    instructions="you are helpful Ai Assistant",
    name="my chatBOT",
)
```

🧠 **Explanation:**

* Agent banaya gaya jo batata hai AI ko ke:
  * Aap helpful ho
  * Aapka naam `"my chatBOT"` hai

> Yeh AI ki personality set karta hai.

---

## ✅ **Point 6: Jab Chat Start Hota Hai (User app kholta hai)**

```python
@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="me hoon doremon mere ps hr sawal ka jawab h 😂").send()
```

### 🔍 Roman Urdu Explanation:

* `@cl.on_chat_start` → Jab user naye se chat shuru karta hai (app kholta hai), yeh function call hota hai.
* `cl.user_session.set("history", [])` → Chat ka pura **history array** khaali set kar diya gaya (fresh session).
* `await cl.Message(...).send()` → User ko ek **welcome message** bheja gaya — yahan simple message hai.

💡 **Yeh bilkul waise hai jaise jab WhatsApp par aap pehli baar kisi se chat shuru karte ho to wo "Hello!" bhejta hai.**

---

## ✅ **Point 7: Jab User Message Likhta Hai**

```python
@cl.on_message
async def handle_message(message: cl.Message):
```

Yeh function tab chalta hai jab user koi bhi sawal ya message bhejta hai.

---

### ✅ **Step 1: Purani Chat History Lo**

```python
history = cl.user_session.get("history")
```

📘 **Roman Urdu:**

* Pehle se jo bhi messages hue they (user aur AI ke) — wo yahan `history` variable mein nikal rahe hain.
* **Yeh important hai context ke liye** , taake AI samajh sake ke pehle kya baat ho chuki hai.

---

### ✅ **Step 2: Temporary (Khaali) Message Display Karo**

```python
msg = cl.Message(content="")
await msg.send()
```

📘 **Roman Urdu:**

* Ek khaali message bubble bana diya gaya screen pe — yeh later fill hoga jab AI jawab dega.
* Isse **typing effect** create hota hai jaise AI soch raha ho.

---

### ✅ **Step 3: User ka Message Add Karo History Mein**

```python
history.append({"role": "user", "content": message.content})
```

📘 **Roman Urdu:**

* User ne jo likha wo ek dictionary form mein store ho gaya history mein:
  ```json
  {"role": "user", "content": "Tumhara fav gadget kya hai?"}
  ```

---

### ✅ **Step 4: AI ko Message + History Do (RunConfig ke sath)**

```python
result = Runner.run_streamed(
    agent1,
    input=history,
    run_config=config,
)
```

📘 **Roman Urdu:**

* Ab AI ko `Runner.run_streamed()` ke zariye pura message + pehle ki history bhej rahe hain.
* `agent1` = AI ki personality (helpful bot)
* `run_config` = uske settings/configuration

🧠 Ab AI server se soch ke jawab generate karega.

---

### ✅ **Step 5: AI ka Response Live Stream Karo (Typing Effect ke sath)**

```python
async for event in result.stream_events():
    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        await msg.stream_token(event.data.delta)
```

📘 **Roman Urdu:**

* AI ka response ek sath nahi aata — **ek ek lafz ya sentence** stream hota hai.
* `stream_token()` har word ko screen pe live display karta hai.
* Yeh bilkul **typing effect** jaisa dikhata hai: "Mujhe Anywhere Door pasand hai..."

---

### ✅ **Step 6: Final Answer ko History Mein Save Karo**

```python
history.append({"role": "assistant", "content": result.final_output})
cl.user_session.set("history", history)
```

📘 **Roman Urdu:**

* Jab pura AI ka response mil gaya to usko bhi history mein store kar liya:
  ```json
  {"role": "assistant", "content": "Mujhe Anywhere Door pasand hai"}
  ```
* `cl.user_session.set()` se updated history dobara save kar di gayi session mein.

---

## 🔚 **Toh Summary of Point 6-7:**

| Step                              | Explanation                                           |
| --------------------------------- | ----------------------------------------------------- |
| `on_chat_start`                 | Jab user pehli baar aata hai, welcome message bhejo   |
| `on_message`                    | Jab user message bheje to process shuru karo          |
| `get("history")`                | Pichli chat yaad karo                                 |
| `msg = cl.Message()`            | Ek khaali bubble banao screen pe                      |
| `append({"role": "user"})`      | User ka message add karo list mein                    |
| `Runner.run_streamed()`         | Gemini AI se jawab lo                                 |
| `stream_token()`                | Har word ko live screen pe show karo                  |
| `append({"role": "assistant"})` | AI ka jawab bhi save karo                             |
| `set("history")`                | Puri updated history ko session mein dobara save karo |
