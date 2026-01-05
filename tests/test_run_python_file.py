from functions.run_python_file import run_python_file


def test_run_calculator_main():
    output = run_python_file("calculator", "main.py")
    print(output)

    output = run_python_file("calculator", "main.py", ["3 + 5"])
    print(output)

    output = run_python_file("calculator", "tests.py")
    print(output)

    output = run_python_file("calculator", "../main.py")
    print(output)

    output = run_python_file("calculator", "nonexistent.py")
    print(output)

    output = run_python_file("calculator", "lorem.txt")
    print(output)
