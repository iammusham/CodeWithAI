"""
Alpha : My first Personal Assistant 
Created with: GPT-4o-mini
Using: Python and OpenAI APIs 
"""

"""
Requirements:
Python-(winget install python) for windows
OpenAI Library-(pip install openai)
"""

from openai import OpenAI
import time, json, os, threading, subprocess

# Paste your OpenAI API key here!
client = OpenAI(api_key="your_openai_api_key")
# select your model!
model = "gpt-4o-mini"

class Alpha:
    functions = {'functions':[]}
    registered_functions = {}

    def __init__(self):
        self.thread_id="thread_id"

    def create_thread(self):
        thread = client.beta.threads.create()
        self.thread_id = thread.id

    def delete_thread(self):
        response = client.beta.threads.delete(self.thread_id)
        print("Thread Deleted Successfully!")

    def add_message(self,user_input):
        message = client.beta.threads.messages.create(self.thread_id,role="user",content=user_input)

    def get_message(self):
        messages = client.beta.threads.messages.list(self.thread_id)
        output = messages.data[0].content[0].text.value
        return output
    
    def list_memories(self):
        with open("memory.json",'r') as f:
            data = json.load(f)
        memory_titles = [memory['title'] for memory in data]
        return memory_titles
    
    def ask(self,messages_input):
        role = "user"
        messages = [{"role":"system","content":"You are alpha my personal assistant"}]
        thread_messages = client.beta.threads.messages.list(self.thread_id)
        for message in reversed(thread_messages.data):
            message_data = {"role":role,"content":message.content[0].text.value}
            messages.append(message_data)
            role = "assistant" if role =="user" else "user"
        if messages_input:
            messages = messages_input
        response  = client.chat.completions.create(model=model, messages=messages , max_tokens=100)
        output = response.choices[0].message.content
        add_message = client.beta.threads.messages.create(self.thread_id,role="assistant",content=output)
        tokens = response.usage.total_tokens
        return output, tokens
    
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

    def call(self):
        role = "user"
        messages = [{"role":"system","content":"You are alpha my personal assistant"},{"role":"system","content":f"Here are the list of all memory titles available: {self.list_memories()}"}]
        thread_messages = client.beta.threads.messages.list(self.thread_id)
        for message in reversed(thread_messages.data):
            message_data = {"role":role,"content":message.content[0].text.value}
            messages.append(message_data)
            role = "assistant" if role =="user" else "user"
        response = client.chat.completions.create(model=model,messages=messages,tools=self.functions['functions'],tool_choice="auto")
        response_message = response.choices[0].message
        token01 = response.usage.total_tokens
        tool_calls = response_message.tool_calls
        second_response, total_tokens = "Error!", token01
        if tool_calls:
            messages.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.registered_functions.get(function_name)
                if function_to_call:
                    function_args = json.loads(tool_call.function.arguments)
                    function_response = function_to_call(**function_args)
                    messages.append({"tool_call_id":tool_call.id,"role":"tool","name":function_name,"content":function_response,})
            second_response, token02 = self.ask(messages)
        else:
            second_response, token02 = self.ask(None)
        total_tokens = token01+token02
        return second_response, total_tokens
        
    def speak(self,output,tokens):
        print("\nAlpha: ", end='')
        for char in output:
            print(char,end='',flush=True)
            time.sleep(0.08)
        print(f"\nTokens Used: {tokens}")
        print()

@Alpha.add_func
def save_as_memory(title,content):
    """
    Save a small data as a memory to remember for future chats
    title : string : title for memory
    content : string : memory content
    """
    data = []
    if os.path.isfile('memory.json'):
        with open('memory.json','r') as file:
            data = json.load(file)
        data.append({"title":title,"memory":content})
    with open('memory.json','w') as file:
        json.dump(data,file, indent=4)
    return "memory saved successfully"

@Alpha.add_func
def delete_memory(title):
    """
    Delete a memory by its title 
    title : string : title of the memory to delete
    """
    if os.path.isfile('memory.json'):
        with open('memory.json','r') as file:
            data = json.load(file)
        with open('memory.json', 'w') as file:
            updated_data = [memory for memory in data if memory["title"] != title]
            json.dump(updated_data,file, indent=4)
        return f"memory with title '{title}' deleted"
    return "file not found"

@Alpha.add_func
def get_memory(title):
    """
    Retrieve a memory by its title
    title : string : title of the memory to retrieve
    """
    if os.path.isfile("memory.json"):
        with open("memory.json",'r') as file:
            data = json.load(file)
        for memory in data:
            if memory['title']==title:
                return memory['memory']
    return "memory not found"

@Alpha.add_func
def update_memory(title, new_memory):
    """
    Update a memory by its title
    title : string : title of the memory to update
    new_memory : string : new memory or updated memory text
    """
    if os.path.isfile('memory.json'):
        with open('memory.json','r') as file:
            data = json.load(file)
        for memory in data:
            if memory['title']==title:
                memory['memory']==new_memory
                data.remove(memory)
                data.append({"title":title,"memory":new_memory})
                with open("memory.json",'w') as file:
                    json.dump(data,file,indent=4)
                return f"memory with title '{title}' updated"
        return "memory not found"


@Alpha.add_func
def get_current_date_time():
    """
    get today's date and time im format Thu Jan 25 16:16:40 IST 2024 and always time format is in 12 hours
    """
    from datetime import datetime
    now = datetime.now()
    formatted_datetime = now.strftime("%d/%m/%Y, %H:%M:%S")
    return formatted_datetime

if __name__=="__main__":
    ai = Alpha()
    ai.create_thread()

    try:
        while True:
            user_input = input("You: ")

            if user_input=="0":
                break
            else:
                prompt = user_input

            ai.add_message(prompt)
            # output, tokens = ai.ask(None)
            output, tokens = ai.call()
            ai.speak(output,tokens)

    finally:
        ai.delete_thread()