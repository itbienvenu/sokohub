import os
import json
from django.conf import settings
from groq import Groq
from .models import Conversation
from .tools import search_products, add_to_cart, get_vendor_stats

class GroqService:
    def __init__(self):
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
             pass
        self.client = Groq(api_key=api_key)

    def get_tool_definitions(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_products",
                    "description": "Search for products in the marketplace.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search keywords (e.g. 'black shoes')"},
                            "min_price": {"type": "number", "description": "Minimum price"},
                            "max_price": {"type": "number", "description": "Maximum price"},
                            "category_name": {"type": "string", "description": "Category name to filter by"}
                        },
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "add_to_cart",
                    "description": "Add a specific product to the user's shopping cart.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "product_id": {"type": "integer", "description": "The ID of the product to add"},
                            "quantity": {"type": "integer", "description": "Quantity to add (default 1)"}
                        },
                        "required": ["product_id"]
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_vendor_stats",
                    "description": "Get sales and inventory statistics for the current logged-in vendor.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                }
            }
        ]

    def process_message(self, token, message_text, user):
        conversation, created = Conversation.objects.get_or_create(token=token)
        
        if user.is_authenticated and not conversation.user:
            conversation.user = user
            conversation.save()

        messages = [
            {
                "role": "system",
                "content": f"You are SokoBot, an intelligent assistant for SokoHub. "
                           f"User: {user.username if user.is_authenticated else 'Guest'}. "
                           f"Role: {user.user_type if user.is_authenticated else 'Visitor'}. "
                           "Use the available tools to fulfill user requests efficiently. "
                           "If a tool returns an error, explain it to the user. "
                           "Be helpful, concise, and professional."
            }
        ]
        
        messages.extend(conversation.history[-20:])
        
        messages.append({"role": "user", "content": message_text})

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=self.get_tool_definitions(),
            tool_choice="auto",
            max_tokens=1024
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            messages.append(response_message)
            
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                tool_response = None

                if function_name == "search_products":
                    tool_response = search_products(**function_args)
                elif function_name == "add_to_cart":
                    tool_response = add_to_cart(user, **function_args)
                elif function_name == "get_vendor_stats":
                    tool_response = get_vendor_stats(user)
                
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(tool_response),
                    }
                )
            
            second_response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages
            )
            final_reply = second_response.choices[0].message.content
        else:
            final_reply = response_message.content

        conversation.history.append({"role": "user", "content": message_text})
        conversation.history.append({"role": "assistant", "content": final_reply})
        conversation.save()

        return final_reply
