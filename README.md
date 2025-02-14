
This project uses **CrewAI Flows** with `@start`, `@router`, and `@listen` decorators.  
The program **asks the user for a name** and:  
✅ **Checks if the name exists using AI**  
✅ **If found, retrieves its meaning**  
✅ **If not found, displays an error message**  

---

## **🔹 1️⃣ What is This Code Doing?**  
💡 **Simple Explanation**:  
1️⃣ **First, it asks the user for an name.**  
2️⃣ **Then, it checks if AI recognizes the name.**  
   - ✅ If the name exists → **It returns the meaning.**  
   - ❌ If the name is unknown → **It shows an error message.**  
3️⃣ **Finally, the result is displayed.**  

---

## **🔹 2️⃣ Breaking Down the Code**  

### **📌 Step 1: Importing Required Modules**  
```python
from crewai.flow.flow import Flow, start, listen, router
from litellm import completion
import dotenv
import os

dotenv.load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')
```
✅ **What’s Happening Here?**  
- 🛠️ **Loading environment variables** to get the **Gemini API key**.  
- 🔗 **Importing CrewAI tools (`Flow`, `start`, `router`, `listen`)** to structure the AI workflow.  
- 📞 **Using LiteLLM (`completion`)** to connect to the AI model.  

---

### **📌 Step 2: Creating the CrewAI Flow**
```python
class ExampleFlow(Flow):
    model = 'gemini/gemini-1.5-flash'
```
✅ **What’s Happening Here?**  
- 🎯 **Defines a new AI workflow (`ExampleFlow`)**.  
- 🤖 **Uses Gemini 1.5 Flash model** to process the name.  

---

### **📌 Step 3: Asking the User for a Name (`@start`)**
```python
@start()
def ask_user_for_name(self):
    user_name = input("🔹 Enter an Islamic name: ")  # Get user input
    self.state["user_name"] = user_name  # Store the name in state
    return user_name  # Pass the name to the next step
```
✅ **What’s Happening Here?**  
- 📝 **User types a name**, which is stored in memory (`self.state`).  
- ⏭️ This name is **passed to the next step**.  

---

### **📌 Step 4: Checking if the Name Exists (`@router`)**
```python
@router(ask_user_for_name)
def check_name_existence(self):
    user_name = self.state["user_name"]

    response = completion(
        model=self.model,
        messages=[
            {
                "role": "user",
                "content": f"Do you know the meaning of the name '{user_name}'? "
                           "If yes, return 'found'. If not, return 'not_found'."
            }
        ],
    )

    result = response["choices"][0]["message"]["content"].strip().lower()
    if "found" in result:
        return "found"
    else:
        return "not_found"
```
✅ **What’s Happening Here?**  
- 🧠 AI **checks if the name is known**.  
- ✅ If AI **knows the name**, it returns **"found"** → Proceeds to meaning.  
- ❌ If AI **doesn't recognize the name**, it returns **"not_found"** → Shows an error message.  

---

### **📌 Step 5A: Getting the Meaning (`@listen("found")`)**
```python
@listen("found")
def get_meaning_of_name(self):
    user_name = self.state["user_name"]

    response = completion(
        model=self.model,
        messages=[
            {
                "role": "user",
                "content": f"Tell me the meaning of the name '{user_name}'."
            }
        ],
    )

    meaning_of_name = response["choices"][0]["message"]["content"]
    self.state["name_meaning"] = meaning_of_name  # Store meaning
    print(f"✅ Meaning of {user_name}: {meaning_of_name}")
    return meaning_of_name
```
✅ **What’s Happening Here?**  
- 📖 AI **retrieves and displays the meaning** of the name.  
- 📝 The meaning is **stored in memory** for future use.  

---

### **📌 Step 5B: Showing an Error Message (`@listen("not_found")`)**
```python
@listen("not_found")
def name_not_found_message(self):
    user_name = self.state["user_name"]
    message = f"❌ Sorry, I couldn't find the meaning of the name '{user_name}'."
    print(message)
    return message
```
✅ **What’s Happening Here?**  
- ❌ If AI **doesn’t recognize the name**, it **displays an error message**.  
- 🚫 This **prevents the flow from crashing** when the name isn’t found.  

---

### **📌 Step 6: Running the Flow (`kickoff()`)**
```python
def kickoff():
    flow = ExampleFlow()
    result = flow.kickoff()
    print(f" Final Result: {result}")

```
✅ **What’s Happening Here?**  
- 🔥 `kickoff()` **starts the AI flow**.  
- 🏁 Runs **Step 1 → Step 2 → Step 3A/3B** automatically.  
- ✅ **Prints the final result.**  

---

## **🔹 3️⃣ Example Outputs**  

### **Case 1: The Name is Found**
```
🔹 Enter an  name: Ayaan
✅ Meaning of Ayaan: Ayaan means "Gift of God" in Arabic.
🔹 Final Result: Ayaan means "Gift of God" in Arabic.
```

### **Case 2: The Name is Not Found**
```
🔹 Enter an  name: Xylofone
❌ Sorry, I couldn't find the meaning of the name 'Xylofone'.
🔹 Final Result: Sorry, I couldn't find the meaning of the name 'Xylofone'.
```

---

## **🔹 4️⃣ What We Learned?**
| **Concept** | **Explanation** |
|------------|---------------|
| **`@start()`** | **Asks the user** for a name. |
| **`@router(previous_function)`** | **Decides next step** based on AI's response. |
| **`@listen("found")`** | **If name exists**, fetch its meaning. |
| **`@listen("not_found")`** | **If name doesn't exist**, show error message. |
| **`self.state["user_name"]`** | **Stores user input** for later use. |
| **`kickoff()`** | **Executes the entire AI workflow automatically.** |

---

## **🔹 5️⃣ Summary**
1️⃣ **First**, the AI **asks the user for an  name** 🎤.  
2️⃣ **Then**, the AI **checks if the name is recognized** 🧠.  
3️⃣ **If found**, it **returns the meaning** 📖.  
4️⃣ **If not**, it **displays an error message** ❌.  
5️⃣ **Finally**, it **prints the result!** ✅.  
