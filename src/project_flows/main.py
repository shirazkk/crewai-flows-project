from crewai.flow.flow import Flow ,start, listen , router
from litellm import completion
import dotenv
import os

dotenv.load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')


class ExampleFlow(Flow):
    model = 'gemini/gemini-1.5-flash'
    @start()
    def ask_user_name(self):
        print("Ask user for name...")
        user = input("Enter your name...")
        self.state["user"] = user
        return user
    @router(ask_user_name)
    def check_name_exist(self):
        user_name=self.state["user"]
        response = completion(
            model = self.model,
            messages =[
                {
                    "role":"user",
                    "content":f"Do you know the meaning of the name '{user_name}'? "
                               "If yes, return 'found'. If not, return 'not_found'."
                }
            ]

         )
        
        result = response["choices"][0]["message"]["content"].strip().lower()
        if result == "found":
            return "found"
        else:
            return "not_found"

      
    
    @listen("found")
    def meaning_of_name(self):
        print(f"meaning of {self.state["user"]}")
        user_name = self.state["user"]

        response = completion(
            model= self.model,
            messages=[
                {
                    "role":"user",
                    "content": f"Tell me the meaning of the name '{user_name}'."
                }
            ]
        )

        meaning_of_name = response["choices"][0]["message"]["content"]
        self.state["name_meaning"] =meaning_of_name
        return meaning_of_name
    
    @listen("not_found")
    def name_not_found_message(self):
        print("Name not found. Please try again.")
        user_name = self.state["user"]
        message = f" Sorry, I couldn't find the meaning of the name '{user_name}'."
        print(message)
        return message
def kickoff():
    flows = ExampleFlow()
    result = flows.kickoff()

    print(f" Final Result:{result}")
       
        
    