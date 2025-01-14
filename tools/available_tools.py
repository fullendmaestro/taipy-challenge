from langchain.agents import Tool
from tools.browser_tools import (
    list_tabs, open_tab, close_tab, switch_tab, get_tab_content,
    # Bookmark management
    list_bookmarks, add_bookmark, delete_bookmark,
    # History management
    search_history, delete_history_item,
    # Download management
    list_downloads, download_file,
    # Window management
    create_window, list_windows,
    # Clipboard operations
    copy_to_clipboard, read_from_clipboard,
    # Browser settings
    get_zoom_level, set_zoom_level
)

# Define all the tools
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
    ),
    # Bookmark management
    Tool(
        name="list_bookmarks",
        func=list_bookmarks,
        description="List all bookmarks"
    ),
    Tool(
        name="add_bookmark",
        func=add_bookmark,
        description="Add a new bookmark with the given URL and title"
    ),
    Tool(
        name="delete_bookmark",
        func=delete_bookmark,
        description="Delete the bookmark with the given ID"
    ),
    # History management
    Tool(
        name="search_history",
        func=search_history,
        description="Search the browser history with the given query"
    ),
    Tool(
        name="delete_history_item",
        func=delete_history_item,
        description="Delete a history item with the given URL"
    ),
    # Download management
    Tool(
        name="list_downloads",
        func=list_downloads,
        description="List all downloads"
    ),
    Tool(
        name="download_file",
        func=download_file,
        description="Download a file from the given URL"
    ),
    # Window management
    Tool(
        name="create_window",
        func=create_window,
        description="Create a new browser window with the given URL and incognito mode"
    ),
    Tool(
        name="list_windows",
        func=list_windows,
        description="List all open browser windows"
    ),
    # Clipboard operations
    Tool(
        name="copy_to_clipboard",
        func=copy_to_clipboard,
        description="Copy the given text to the clipboard"
    ),
    Tool(
        name="read_from_clipboard",
        func=read_from_clipboard,
        description="Read text from the clipboard"
    ),
    # Browser settings
    Tool(
        name="get_zoom_level",
        func=get_zoom_level,
        description="Get the current zoom level of the browser"
    ),
    Tool(
        name="set_zoom_level",
        func=set_zoom_level,
        description="Set the zoom level of the browser"
    )
]