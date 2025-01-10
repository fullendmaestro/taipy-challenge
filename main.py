# TODO #1: Import necessary libraries
import os
import pandas as pd
import taipy.gui.builder as tgb
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from taipy.gui import Gui, notify

from tools.tab import list_tabs, open_tab, close_tab, switch_tab, get_tab_content

# TODO #2: Load environment variables
load_dotenv()

# Define the tools
tools = [
    Tool(
        name="get_tab_content",
        func=get_tab_content,
        description="Get the content of the tab"
    ),
    Tool(
        name="list_tabs",
        func=list_tabs,
        description="List all open tabs"
    ),
    Tool(
        name="open_tab",
        func=open_tab,
        description="Open a new tab with the given URL"
    ),
    Tool(
        name="close_tab",
        func=close_tab,
        description="Close the tab with the given ID"
    ),
    Tool(
        name="switch_tab",
        func=switch_tab,
        description="Switch to the tab with the given ID"
    )
]

# TODO #4: Configure the LLM and agent
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.4,
    max_tokens=512,
    timeout=None,
    max_retries=2,
)

agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description")

# TODO #5: Define the function to query the LLM
def query_llm(query_message):
    response = agent.run(query_message)
    return response

# TODO #6: Initialize chatbot state variables
query_message = ""
messages = []
messages_dict = {}

def on_init(state):
    state.messages = [
        {
            "style": "assistant_message",
            "content": "Hi, I am Browser assistant! How can I help you today?",
        },
    ]
    new_conv = create_conv(state)
    state.conv.update_content(state, new_conv)

# TODO #7: Define helper functions for the chatbot
def create_conv(state):
    messages_dict = {}
    with tgb.Page() as conversation:
        for i, message in enumerate(state.messages):
            text = message["content"].replace("<br>", "\n").replace('"', "'")
            messages_dict[f"message_{i}"] = text
            tgb.text(
                f"{{messages_dict.get('message_{i}') or ''}}",
                class_name=f"message_base {message['style']}",
                mode="md",
            )
    state.messages_dict = messages_dict
    return conversation

def send_message(state):
    state.messages.append(
        {
            "style": "user_message",
            "content": state.query_message,
        }
    )
    state.conv.update_content(state, create_conv(state))
    notify(state, "info", "Sending message...")
    state.messages.append(
        {
            "style": "assistant_message",
            "content": query_llm(state.query_message),
        }
    )
    state.conv.update_content(state, create_conv(state))
    state.query_message = ""

def reset_chat(state):
    state.query_message = ""
    on_init(state)

# TODO #8: Design the GUI layout
with tgb.Page() as page:
    with tgb.part(class_name="flex-column"):
        tgb.part(partial="{conv}", height="90vh", class_name="card card_chat")
        with tgb.part("card mt1 p0"):
            tgb.input(
                "{query_message}",
                on_action=send_message,
                change_delay=-1,
                label="Write your message:",
                class_name="fullwidth",
            )

# TODO #9: Add the application run logic
if __name__ == "__main__":
    gui = Gui(page)
    conv = gui.add_partial("")
    gui.run(title="Taipy Assistant", dark_mode=False, margin="0px", debug=True)