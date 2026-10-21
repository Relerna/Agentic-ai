# pyrefly: ignore[missing-import]
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ["GROQ"])

tools = [
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert a specified amount from one currency to another.",
            "parameters": {
                "type": "object",
                "properties": {
                    "on_list": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "amount": {
                                    "type": "number",
                                    "description": "The amount of money of main currency",
                                },
                                "main_currency": {
                                    "type": "string",
                                    "description": "The source of currency e.g. USD , EUR , JPY , THB",
                                },
                                "target_currency": {
                                    "type": "string",
                                    "description": "The target of currency e.g. USD , EUR , JPY , THB",
                                },
                            },
                            "required": ["amount", "main_currency", "target_currency"],
                            "additionalProperties": False,
                        },
                    }
                },
                "required": ["on_list"],
                "additionalProperties": False,
            },
        },
    }
]


def prompt(userprompt):
    res = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    """ Call a function convert_curency only one and and 
                put every requestion to on_list and Do not calculate anything just put the request into onlist"""
                ),
            },
            {"role": "user", "content": userprompt},
        ],
        tools=tools,
    )
    return res.choices[0].message.tool_calls[0].function.arguments


print(prompt("convert 100 USD to THB , convert to JPY and convert to rupee"))
