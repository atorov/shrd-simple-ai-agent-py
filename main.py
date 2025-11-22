# AI Agent in Python

# Tools: Special skills for the model to use
# Agent: Tools in a loop to accomplish a goal

import json
import os
import subprocess

from anthropic import Anthropic
from anthropic.types import ToolParam

TOOLS: list[ToolParam] = [
    {
        "name": "list_files",
        "description": "List files and directories at a given path",
        "input_schema": {
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
        "input_schema": {
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
        "input_schema": {
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
        "input_schema": {
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
    """Execute a tool by name with given arguments."""

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


def run_agent(goal: str):
    """Run the agent with a given prompt."""

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages: list = [{"role": "user", "content": goal}]

    print(f"Working on: {goal}\n")

    while True:
        # Call the AI with tools
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=messages,
            tools=TOOLS,
        )

        # Add AI response to conversation
        messages.append({"role": "assistant", "content": response.content})

        # Check if the AI wants to use a tool
        tool_calls = [c for c in response.content if c.type == "tool_use"]

        if tool_calls:
            tool_results = []
            for call in tool_calls:
                print(f"Using tool: {call.name} with args {call.input}")
                result = execute_tool(call.name, call.input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": call.id,
                        "content": result,
                    }
                )

            # Add tool result to conversation
            messages.append({"role": "user", "content": tool_results})
        else:
            # No more tool calls, finish the loop
            text_blocks = [c for c in response.content if c.type == "text"]
            if text_blocks:
                print(f"AI Response: {text_blocks[0].text}")
            break


if __name__ == "__main__":
    while True:
        try:
            prompt = input("\nWhat wold you like me to do? (or  'quit' to exit)\n> ")
            if prompt.lower() in ("quit", "exit"):
                break
            run_agent(prompt)
        except KeyboardInterrupt:
            print("\nGood bye!Exiting...")
            break
