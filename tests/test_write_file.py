import os

from functions.get_file_content import get_file_content
from functions.write_file import write_file

files_to_remove = ["calculator/some-content.txt", "calculator/newDir/some-content.txt"]


def teardown_module():
    for file_to_remove in files_to_remove:
        os.remove(file_to_remove)


def test_write_file():
    content = "wait, this isn't lorem ipsum"
    content_override = "lorem ipsum dolor sit amet"
    result = write_file("calculator", "some-content.txt", content)
    print(result)

    written_content = get_file_content("calculator", "some-content.txt")

    assert written_content == content, written_content

    result = write_file("calculator", "some-content.txt", content_override)

    written_content = get_file_content("calculator", "some-content.txt")

    assert written_content == content_override, written_content


def test_write_file_not_existing_dir_should_be_created():
    content = "lorem ipsum dolor sit amet"
    result = write_file("calculator", "newDir/some-content.txt", content)
    print(result)

    written_content = get_file_content("calculator", "newDir/some-content.txt")

    assert written_content == content, written_content


def test_write_file_error_outside_working_dir():
    result = write_file("calculator", "/tmp/something.txt", "some content")
    print(result)

    assert result == 'Error: Cannot write "/tmp/something.txt" as it is outside the permitted working directory', result
