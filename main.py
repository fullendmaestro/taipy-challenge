import os
import pandas as pd
import taipy.gui.builder as tgb
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from taipy.gui import Gui, notify
from tools.speech import play_response, start_recording, stop_recording
from tools.available_tools import tools

# Load environment variables
load_dotenv()

# Configure the LLM and agent
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.4,
    max_tokens=512,
    timeout=None,
    max_retries=2,
)

agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description")

# Define the function to query the LLM
def query_llm(state):
    response = agent.run(state.query_message)
    if state.speech_enabled:
        play_response(response)
    return response

# Initialize chatbot state variables
query_message = ""
messages = []
messages_dict = {}


# Add speech state variables
speech_enabled = True
is_recording = False

def on_init(state):
    state.messages = [
        {
            "style": "assistant_message",
            "content": "Hi, I am Browser assistant! How can I help you today?",
        },
    ]
    new_header = render_header(state)
    state.header.update_content(state, new_header)
    new_conv = create_conv(state)
    state.conv.update_content(state, new_conv)

# Define helper functions for the chatbot
def create_conv(state):
    messages_dict = {}
    with tgb.Page() as conversation:
        for i, message in enumerate(state.messages):
            text = message["content"].replace("<br>", "\n").replace('"', "'")
            messages_dict[f"message_{i}"] = text
            tgb.text(
                f"{{messages_dict.get('message_{i}') or ''}}",
                class_name=f"message message-content message-bubble message_base {message['style']}",
                mode="md",
            )
    state.messages_dict = messages_dict
    return conversation

def render_header(state):
    with tgb.Page() as header:
        with tgb.part(class_name="header-content"):
            with tgb.part(class_name="header-title"):
                tgb.text("Chat Assistant", class_name="h-5 w-5")
            tgb.part(class_name="header-separator")
            with tgb.part(class_name="header-actions"):
                with tgb.part(class_name="reader-controls"):
                    tgb.button(
                        "⏹️" if state.is_recording else "🎤",
                        on_action=toggle_recording,
                        class_name=f"button {'recording' if state.is_recording else ''}",
                        hover_text="Stop Recording" if state.is_recording else "Start Recording"
                    )
                    tgb.part(class_name="header-separator")
                    tgb.button(
                        "🔇" if state.speech_enabled else "🔊",
                        on_action=toggle_speech,
                        class_name="toggle",
                        hover_text="Toggle audio",
                        aria_label="Toggle audio",
                        aria_pressed=state.speech_enabled
                    )
    return header

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
            "content": query_llm(state),
        }
    )
    state.conv.update_content(state, create_conv(state))
    state.query_message = ""

def reset_chat(state):
    state.query_message = ""
    on_init(state)

def toggle_speech(state):
    state.speech_enabled = not state.speech_enabled
    new_header = render_header(state)
    state.header.update_content(state, new_header)
    print("PLAYBACK", state.speech_enabled)
    
def toggle_recording(state):
    state.is_recording = not state.is_recording
    new_header = render_header(state)
    state.header.update_content(state, new_header)
    print("IS_RECORDING", state.isrecording)
    if state.is_recording:
        start_recording()
    else:
        stop_recording()

# Design the GUI layout
with tgb.Page() as page:
    with tgb.part(class_name="chat-container"):
        tgb.part(partial="{header}", class_name="header")
        with tgb.part(class_name="chat-main"):
            with tgb.part(class_name="chat-content"):
                with tgb.part(class_name="chat-interface"):
                    with tgb.part(class_name="messages-container"):
                        with tgb.part(class_name="messages-list"):
                            tgb.part(partial="{conv}")
                    with tgb.part(class_name="chat-input"):
                        tgb.input(
                            "{query_message}",
                            on_action=send_message,
                            change_delay=-1,
                            label="Type your message...",
                            class_name="fullwidth",
                        )

# Add the application run logic
if __name__ == "__main__":
    gui = Gui(page)
    header = gui.add_partial("")
    conv = gui.add_partial("")
    gui.run(title="Taipy Assistant", dark_mode=False, margin="0px", debug=True)
