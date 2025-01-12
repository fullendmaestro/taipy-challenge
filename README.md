# Taipy Assistant - AI-Powered Browser Control

A powerful Chrome extension that lets you control your browser through natural language conversations using AI. Built with Python, Taipy, and the Chrome Extensions API.

![Browser Assistant Demo](docs/demo.gif)

## 🌟 Key Features

### 1. Natural Language Browser Control

- Control your browser by simply chatting with the AI assistant
- The AI understands context and can perform complex sequences of actions
- Powered by Google's Gemini 1.5 Flash model for fast and accurate responses

### 2. Tab Management

- **List Tabs**: View all open tabs across windows
- **Open Tabs**: Open new tabs with specified URLs
- **Close Tabs**: Close specific tabs by ID or URL
- **Switch Tabs**: Navigate between tabs seamlessly
- **Get Content**: Extract and analyze content from the current tab

## 🛠️ Technical Architecture

### Real-time Communication

- WebSocket-based bidirectional communication between Taipy server and Chrome extension
- Websocket client Identification for the Taipy server and the Extension

### AI Integration

- Leverages Langchain for flexible tool integration
- Uses Google's Gemini model for natural language understanding
- Context-aware command processing

### User Interface

- Clean and responsive chat interface built with Taipy
- Real-time status updates and error handling
- Seamless integration with Chrome's side panel

## 🔧 Code Quality

### Clean Architecture

- **Modular Design**: Separate controllers for different functionalities
- **SOLID Principles**: Each component has a single responsibility
- **Error Handling**: Comprehensive error handling at all levels

### Best Practices

- Type hints for better code maintainability
- Comprehensive documentation and comments
- Consistent code style and formatting
- Proper resource cleanup and memory management

## 📝 Example Usage

Here are some things you can ask the assistant to do:

```plaintext
"Open https://github.com/ in a new tab"
"Show me all my bookmarks about programming"
"What's the content of the current tab?"
"Download this PDF file"
"Clear my browsing history for the last hour"
"Search my history for machine learning articles"
```
