# Taipy Assistant

![Taipy Assistant Demo](https://github.com/fullendmaestro/taipy-challenge/blob/main/docs/taipy.webp)
Taipy Assistant is an innovative concept for an AI-powered browser extension that aims to seamlessly integrate with your web browsing experience. Leveraging the power of Google's Gemini 1.5 Flash model and the flexibility of Taipy's GUI framework, this assistant proposes an advanced level of interaction with your browser.

## 🚧 Project Status: Concept and Early Development

**Important Note**: Many features described in this README are conceptual or in very early stages of development. The project currently serves as a proof-of-concept and a framework for future implementation.

## 🌟 Proposed Key Features

### 1. AI-Powered Browser Control (Partially Implemented)

- Utilizes Google's Gemini 1.5 Flash model for advanced natural language understanding
- Aims to execute complex browser actions through simple conversational commands

### 2. Comprehensive Browser Integration (Mostly Conceptual)

- **Tab Management**: Open, close, switch, and list tabs (Basic implementation)
- **Bookmark Operations**: Add, delete, and list bookmarks (Not yet implemented)
- **History Management**: Search and manage browsing history (Not yet implemented)
- **Download Control**: Initiate and monitor downloads (Not yet implemented)
- **Window Management**: Create new windows, including incognito mode (Not yet implemented)
- **Clipboard Integration**: Copy and paste with voice commands (Not yet implemented)
- **Browser Settings**: Adjust zoom levels and other settings (Not yet implemented)

### 3. Real-time Communication (Basic Implementation)

- WebSocket server enables communication between the AI and the browser extension
- Asynchronous operations for responsive user experience

### 4. User-Friendly Interface (Partially Implemented)

- Taipy-powered GUI for interaction (Basic implementation)
- Markdown support for rich text responses (Implemented)

## 🚀 Innovation

- **AI-Browser Synergy**: Unique concept of integrating AI capabilities with browser APIs
- **Natural Language Browser Control**: Pioneering idea of using conversational AI for browser manipulation
- **Extensible Architecture**: Framework designed for easy addition of new browser functionalities

## 💻 Current Code Base

- **Modular Design**: Initial structure with separation between AI, WebSocket server, and browser extension
- **Asynchronous Programming**: Utilizes Python's `asyncio` for WebSocket communication
- **Best Practices**: Aims to follow extension development guidelines and Python coding standards

### Interaction Flow

1. **User Input**: The user provides a natural language command.
2. **AI Processing**: The AI component interprets the command and determines the appropriate action.
3. **WebSocket Communication**: The AI component sends the action to the WebSocket server using asynchronous communication.
4. **Command Execution**: The WebSocket server forwards the action to the browser extension.
5. **Browser Manipulation**: The browser extension performs the action, such as opening a new tab or navigating to a URL.

## 🛠 Setup and Installation (For Development Purposes)

1. Clone the repository:

```bash
git clone https://github.com/yourusername/taipy-assistant.git
cd taipy-assistant
```

2. Set up a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Start the WebSocket server:

```bash
taipy run main.py --use-reloader
```

5. Start the taipy server:

```bash
python websocket_server.py
```

5. Start the WebSocket server:

```bash
python websocket_server.py
```

6. Load the browser extension:

- Open Chrome and navigate to `chrome://extensions/`
- Enable "Developer mode" using the toggle switch in the top right corner
- Click "Load unpacked" and select the `extension` directory from the cloned repository

7. Interact with the Taipy Assistant through the browser extension interface.

## 🛠 Tech Stack

- **Programming Language**: Python
- **AI Model**: Google's Gemini 1.5 Flash
- **Web Framework**: Taipy
- **Communication Protocol**: WebSocket
- **Browser Extension**: JavaScript, HTML, CSS
- **Environment Management**: Virtualenv
- **Version Control**: Git
- **Package Management**: pip
