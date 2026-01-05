from config import MAX_CHARS
from functions.get_file_content import get_file_content


def test_get_gile_content_too_big():
    content = get_file_content("calculator", "lorem.txt")
    last_line = content.splitlines()[-1]

    assert f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]' in last_line, last_line


def test_get_file_content_calculator_main():
    content = get_file_content("calculator", "main.py")

    print(content)


def test_get_file_content_calculator():
    content = get_file_content("calculator", "pkg/calculator.py")

    print(content)


def test_get_file_content_error_outside():
    content = get_file_content("calculator", "/bin/cat")

    assert content == 'Error: Cannot read "/bin/cat" as it is outside the permitted working directory', content


def test_get_file_content_error_does_not_exists():
    content = get_file_content("calculator", "pkg/does_not_exists.txt")

    assert content == 'Error: File not found or is not a regular file: "pkg/does_not_exists.txt"', content
