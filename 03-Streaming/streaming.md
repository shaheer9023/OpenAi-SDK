
---

### 🔄 **Streaming kya hoti hai?**

* Streaming ka matlab hai ke **LLM (Large Language Model)** ka output **step-by-step** ya **token-by-token** aata hai, ek saath poora nahi.
* Jab LLM ka response generate ho raha hota hai, aap **us waqt** ka output dekh saktay ho, bina wait kiye ke poora response ready ho.

---

### ⚙️ **Kaise kaam karti hai (SDK mein)?**

* `Runner.run_streamed()` method se aap streaming mode mein run start karte ho.
* Ye method return karta hai `RunResultStreaming`, jisme `stream_events()` hota hai.
* `stream_events()` ek **async stream** hota hai, jisme aapko har step pe `StreamEvent` milta hai.
* Har `StreamEvent` mein LLM ka naya token ya update hota hai.
* Format mostly OpenAI ke `response.created`, `response.output_text.delta` types mein hota hai.

---

### ✅ **Streaming kyu use karni chahiye?**

* **Better UX (User Experience)** : Users ko turant feedback milta hai jab model response generate kar raha hota hai.
* **Faster feel** : User ko lagta hai ke system fast hai kyunki kuch na kuch turant dikh raha hota hai.
* **Live updates** : Agar aapka LLM kuch step-by-step ya process-wise batata hai, to streaming se har step dikhaya ja sakta hai.
* **Async performance** : Backend ya frontend apps mein real-time output show karna asaan hota hai.

---
