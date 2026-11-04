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
    },
    {
        "type": "function",
        "function": {
            "name": "forecast_thailand_weather",
            "description": "Get the weather forecast for provinces or cities in Thailand.",
            "parameters": {
                "type": "object",
                "properties": {
                    "province": {
                        "type": "string",
                        "description": "The province or city in Thailand, e.g. Bangkok, Chiang Mai, Phuket, Khon Kaen",
                    },
                    "days": {
                        "type": "integer",
                        "description": "The number of days to forecast (e.g. 1 to 7)",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit, defaults to celsius",
                    },
                },
                "required": ["province", "days"],
                "additionalProperties": False,
            },
        },
    },
]


def prompt(userprompt):
    messages = [
        {
            "role": "system",
            "content": (
                """You have two separate tools: `convert_currency` and `forecast_thailand_weather`.
- For currency conversion requests: Call `convert_currency` only once and put every currency request into `on_list`. Do not calculate anything yourself.
- For Thailand weather forecast requests: Call `forecast_thailand_weather` as a separate tool call.
- When the user asks to both convert currency and check the weather in the same prompt, you MUST call both `convert_currency` and `forecast_thailand_weather` as separate tool calls."""
            ),
        },
        {"role": "user", "content": userprompt},
    ]

    tool_calls_list = []
    while True:
        res = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=tools,
        )
        msg = res.choices[0].message
        if not msg.tool_calls:
            break

        messages.append(msg)
        for tool_call in msg.tool_calls:
            tool_calls_list.append(
                {
                    "tool_name": tool_call.function.name,
                    "arguments": json.loads(tool_call.function.arguments),
                }
            )
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": "success",
                }
            )

    return tool_calls_list


print(
    prompt(
        " convert 100 USD to THB , convert to JPY and convert to rupee "
    )
)
