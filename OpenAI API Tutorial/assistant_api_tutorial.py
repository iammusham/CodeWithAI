"""
OpenAI Assistant API Tutorial for Beginners!
This Tutorial of Assistant API include Function calling with Assistant API 
"""

"""
Requirements:
Python: (winget install python) for windows
OpenAI Python Library: (pip install openai)
"""

from openai import OpenAI
import time, json, os
from keys import openai_api_key

# Paste your OpenAI API key here!
client = OpenAI(api_key=openai_api_key)

# Paste your Assistant ID here!
assistant_id = "asst_uB6AQZws8Bi5Q677gcfqydvf"

# Select your model!
model = "gpt-4o-mini"

class Assistant:
    functions = {"functions":[]}
    registered_functions = {}

    def __init__(self):
        self.thread_id = "thread_id"

    # Assistant
    def create_assistant(self):
        assistant = client.beta.assistants.create(name="Alpha", instructions="You are Alpha my personal assistant", model=model)
        assistant_id = assistant.id
        print(assistant_id)

    def retrieve_assistant(self):
        my_assistant = client.beta.assistants.retrieve(assistant_id)
        print(my_assistant)

    def modify_assistant(self):
        my_updated_assistant = client.beta.assistants.update(assistant_id=assistant_id,model=model,instructions="You are Alpha my personal Assistant", name = "Alpha", tools=self.functions["functions"])

    # Threads
    def create_thread(self):
        thread = client.beta.threads.create()
        self.thread_id = thread.id

    def delete_thread(self):
        response = client.beta.threads.delete(self.thread_id)
        print('Thread Deleted Successfully')

    # Messages
    def add_message(self,user_input):
        message = client.beta.threads.messages.create(thread_id=self.thread_id, role= 'user', content=user_input)

    def get_message(self):
        messages = client.beta.threads.messages.list(self.thread_id)
        output = messages.data[0].content[0].text.value
        return output
    
    # Runs
    def run_assistant(self):
        run = client.beta.threads.runs.create(thread_id=self.thread_id, assistant_id=assistant_id, instructions="Reply in Brief")
        return run.id
    
    def retrieve_run(self,run_id):
        run = client.beta.threads.runs.retrieve(thread_id=self.thread_id,run_id=run_id)
        return run
    
    # Runs Steps
    def run_require_action(self,run,run_id):
        tool_outputs =[]
        if run.required_action:
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.registered_functions.get(function_name)
                if function_to_call:
                    function_args = json.loads(tool_call.function.arguments)
                    function_response = function_to_call(**function_args)
                    tool_outputs.append({"tool_call_id":tool_call.id, "output":function_response})
            run = client.beta.threads.runs.submit_tool_outputs(thread_id=self.thread_id, run_id=run_id, tool_outputs=tool_outputs)

    def assistant_api(self):
        self.modify_assistant()
        run_id = self.run_assistant()
        run = self.retrieve_run(run_id)
        while run.status=="requires_action" or "queued":
            run = self.retrieve_run(run_id)
            if run.status=="completed":
                break
            self.run_require_action(run,run_id)
        outputs = self.get_message()
        tokens = run.usage.total_tokens
        return outputs, tokens
    
    @classmethod
    def add_func(cls,func):
        cls.registered_functions[func.__name__] = func
        doc_lines = func.__doc__.strip().split('\n')
        func_info = {
        'type': 'function',
        'function': {
            'name': func.__name__,
            'description': doc_lines[0].strip(),
            'parameters': {
                'type': 'object',
                'properties': {k.strip(): {'type': v.strip().split(':')[0].strip(), 'description': v.strip().split(':')[1].strip()} 
                               for k, v in (line.split(':', 1) for line in doc_lines[1:])},
                'required': [k.strip() for k, v in (line.split(':', 1) for line in doc_lines[1:])]}}}
        
        cls.functions["functions"].append(func_info)

    def speak(self,output,tokens):
        print("\nAlpha: ", end='')
        for char in output:
            print(char,end='',flush=True)
            time.sleep(0.08)
        print(f"\nTokens Used: {tokens}")
        print()

@Assistant.add_func
def get_current_date_time():
    """
    get today's date and time im format Thu Jan 25 16:16:40 IST 2024 and always time format is in 12 hours
    """
    from datetime import datetime
    now = datetime.now()
    formatted_datetime = now.strftime("%d/%m/%Y, %H:%M:%S")
    return formatted_datetime

if __name__=="__main__":
    ai = Assistant()
    ai.create_thread()

    try:
        while True:
            user_input = input("You: ")

            if user_input=="0":
                break
            else:
                prompt = user_input

            ai.add_message(prompt)
            output, tokens = ai.assistant_api()
            ai.speak(output,tokens)

    finally:
        ai.delete_thread()  
