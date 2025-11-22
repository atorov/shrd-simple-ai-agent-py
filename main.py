# AI Agent in Python

# Tools: Special skills for the model to use
# Agent: Tools in a loop to accomplish a goal

import json
import os
import subprocess

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


def execute_tool(name, arguments):
    if name == "list_files":
        path = arguments.get("path", ".")
        try:
            files = os.listdir(path)
            return json.dumps(files, indent=2)
        except OSError as e:
            return f"Error listing files: {str(e)}"

    elif name == "read_file":
        path = arguments["path"]
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            return content
        except OSError as e:
            return f"Error reading file: {str(e)}"

    elif name == "run_bash":
        command = arguments["command"]
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=False,
            )
            return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        except (subprocess.SubprocessError, OSError) as e:
            return f"Error running bash command: {str(e)}"

    elif name == "edit_file":
        path = arguments["path"]
        old_text = arguments["old_text"]
        new_text = arguments["new_text"]

        try:

            # Create new file if old_text is empty
            if old_text == "":
                with open(path, "a", encoding="utf-8") as file:
                    file.write(new_text)
                return "File created"

            # Read the existing file content
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()

            # Replace text
            new_content = content.replace(old_text, new_text)

            # Write back to the file
            with open(path, "w", encoding="utf-8") as file:
                file.write(new_content)
            return "File edited successfully"
        except OSError as e:
            return f"Error editing file: {str(e)}"
    else:
        return f"Unknown tool: {name}"
