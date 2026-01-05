import re

from functions.get_files_info import get_files_info


def parse_files_info(files_info):
    # Parse each line with regex: - name, size=X bytes, is_dir=Y
    pattern = r"^- (.+?), size=(.+?) bytes, is_dir=(True|False)$"

    parsed_files = {}
    for line in files_info.split("\n"):
        match = re.match(pattern, line)
        if match:
            name, size, is_dir = match.groups()
            parsed_files[name] = {"size": None if size == "None" else int(size), "is_dir": is_dir == "True"}

    return parsed_files


def test_files_info_outside_working_dir():
    files_info = get_files_info("calculator", "../")

    print("Actual output:")
    print(files_info)

    assert files_info == 'Error: Cannot list "../" as it is outside the permitted working directory', files_info


def test_files_info_non_existing_dir():
    files_info = get_files_info("calculator", "/bin")

    print("Actual output:")
    print(files_info)

    assert files_info == 'Error: Cannot list "/bin" as it is outside the permitted working directory', files_info


def test_files_on_pkg():
    files_info = get_files_info("calculator", "pkg")

    print("Actual output:")
    print(files_info)
    parsed_files = parse_files_info(files_info)

    # Verify expected files are present
    assert "calculator.py" in parsed_files, "calculator.py should be in the output"
    assert "render.py" in parsed_files, "render.py should be in the output"

    # Check calculator.py: should be a file with non-zero size
    assert not parsed_files["calculator.py"]["is_dir"], "calculator.py should be a file"
    assert parsed_files["calculator.py"]["size"] is not None and parsed_files["calculator.py"]["size"] > 0, (
        f"calculator.py should have a non-zero size, got {parsed_files['calculator.py']['size']}"
    )

    # Check render.py: should be a file with non-zero size
    assert not parsed_files["render.py"]["is_dir"], "render.py should be a file"
    assert parsed_files["render.py"]["size"] is not None and parsed_files["render.py"]["size"] > 0, (
        f"render.py should have a non-zero size, got {parsed_files['render.py']['size']}"
    )


def test_files_on_calculator():
    files_info = get_files_info("calculator", ".")

    print("Actual output:")
    print(files_info)
    parsed_files = parse_files_info(files_info)

    # Verify expected files are present
    assert "main.py" in parsed_files, "main.py should be in the output"
    assert "test_calculator.py" in parsed_files, "test_calculator.py should be in the output"
    assert "pkg" in parsed_files, "pkg should be in the output"

    assert not parsed_files["main.py"]["is_dir"], "main.py should be a file"
    assert parsed_files["main.py"]["size"] is not None and parsed_files["main.py"]["size"] > 0, (
        f"main.py should have a non-zero size, got {parsed_files['main.py']['size']}"
    )

    assert not parsed_files["test_calculator.py"]["is_dir"], "test_calculator.py should be a file"
    assert parsed_files["test_calculator.py"]["size"] is not None and parsed_files["test_calculator.py"]["size"] > 0, (
        f"test_calculator.py should have a non-zero size, got {parsed_files['test_calculator.py']['size']}"
    )

    assert parsed_files["pkg"]["is_dir"], "pkg should be a directory"
    assert parsed_files["pkg"]["size"] is None, f"pkg should have size=None, got {parsed_files['pkg']['size']}"
