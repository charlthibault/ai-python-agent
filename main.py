import argparse
import logging
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import call_functions_from_llm_response
from functions import (
    schema_get_file_content,
    schema_get_files_info,
    schema_run_command_in_terminal,
    schema_run_python_file,
    schema_write_file,
)
from logger import logger
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("missing GEMINI_API_KEY environment variable")

client = genai.Client(api_key=api_key)


def agent_loop(client: genai.Client, user_prompt: str) -> None:
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(100):
        available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_write_file,
                schema_run_python_file,
                schema_run_command_in_terminal,
            ],
        )

        # Call LLM
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )

        # Add response to message history
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # Make tool's calls and add result in messages history
        if response.function_calls:
            results = call_functions_from_llm_response(response)
            messages.append(types.Content(role="user", parts=results))
            logger.info(f"\n---\n{response.text}\n")
        else:
            logger.info(f"\n\nFinal response: ---\n{response.text}")
            logger.debug(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            logger.debug(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            # There is one answer to the user prompt so stop the loop
            return
    logger.error("Agent reached maximum iteration without any response, stopping now")
    exit(1)


def main(user_prompt):
    logger.debug(f"User prompt: {user_prompt}")
    agent_loop(client, user_prompt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    main(args.user_prompt)
