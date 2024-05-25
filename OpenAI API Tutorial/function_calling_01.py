# Importing OpenAI Library
from openai import OpenAI
import json

# Paste Your OpenAI API key here
client = OpenAI(api_key="your_openai_api_key")
model = "gpt-4o"

# Predefined stock prices
stock_prices = {
        'AAPL': 190.00,   # Apple
        'GOOGL': 176.33, # Alphabet (Google)
        'AMZN': 180.75,  # Amazon
        'MSFT': 430.16,   # Microsoft
        'TSLA': 179.24    # Tesla
    }
    

# This is the actual function model will call
def get_stock_price(stock_name):
    # Get the stock price for the given stock name
    return str(stock_prices.get(stock_name.upper(), 'Stock not found'))


def run_conversation(user_input):
    # Step 1: send the conversation and available functions to the model
    messages = [{"role": "system", "content": f"here are available stocks data {stock_prices}"},{"role": "user", "content": user_input}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_stock_price",
                "description": "Get the current stock price",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "stock_name": {
                            "type": "string",
                            "description": "name of stock",
                        },
                    },
                    "required": ["stock_name"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_stock_price": get_stock_price,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                stock_name=function_args.get("stock_name"),
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(model=model,messages= messages,max_tokens=50)
        output=second_response.choices[0].message.content
        # get a new response from the model where it can see the function response
        return output

while True:
  user_input = input("ChatGPT: ")
  print()
  print(run_conversation(user_input))