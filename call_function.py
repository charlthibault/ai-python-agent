import logging

from google.genai import types

from config import WORKING_DIRECTORY
from functions import get_file_content, get_files_info, run_command_in_terminal, run_python_file, write_file
from logger import logger

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
    "run_command_in_terminal": run_command_in_terminal,
}


def call_functions_from_llm_response(response: types.GenerateContentResponse) -> list[types.Part]:
    function_results = []
    for function_call in response.function_calls:
        logger.info(f"Calling function: {function_call.name}({function_call.args})")
        call_function_response = call_function(function_call)

        if not call_function_response.parts:
            raise RuntimeError(f"No content parts when calling function {function_call.name} with {function_call.args}")
        if call_function_response.parts[0].function_response is None:
            raise RuntimeError(f"No response when calling function {function_call.name} with {function_call.args}")

        function_results.append(
            types.Part(
                function_response=types.FunctionResponse(
                    name=function_call.name, response={"output": call_function_response}
                )
            )
        )
        logger.debug(f"-> {call_function_response.parts[0].function_response.response}")

    return function_results


def call_function(function_call: types.FunctionCall) -> types.Content:
    if logger.getEffectiveLevel() == logging.WARNING:
        logger.warning(f"Calling function: {function_call.name}({function_call.args})")
    else:
        logger.info(f" - Calling function: {function_call.name}")

    function_name = function_call.name or ""

    function_to_call = function_map.get(function_name)
    if not function_to_call:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = WORKING_DIRECTORY

    response = function_to_call(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": response},
            )
        ],
    )
