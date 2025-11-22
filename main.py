# AI Agent in Python

# Tools: Special skills for the model to use
# Agent: Tools in a loop to accomplish a goal

# import os
# import json
# import subprocess
# from anthropic import Anthropic

TOOLS = [
    {
        "name": "list_files",
        "description": "List files and directories at a given path",
        "input schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to list (defaults to current directory)",
                }
            },
        },
    },
    {
        "name": "read_file",
        "description": "Read the contents of a file",
        "input schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file to read"}
            },
            "required": ["path"],
        },
    },
    {
        "name": "run_bash",
        "description": "Run a bash command and return the output",
        "input schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The bash command to run"}
            },
            "required": ["command"],
        },
    },
    {
        "name": "edit_file",
        "description": "Edit a file by replacing old text with new text",
        "input schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file to edit"},
                "old_text": {
                    "type": "string",
                    "description": "Text to search for and replace",
                },
                "new_text": {"type": "string", "description": "Text to replace with"},
            },
            "required": ["path", "old_text", "new_text"],
        },
    },
]
