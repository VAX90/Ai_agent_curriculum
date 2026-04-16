from functions.run_python_file import run_python_file


def main():
    # test calculator, should print usage instructions
    calculator_result = run_python_file("calculator", "main.py")
    print(calculator_result)

    # test of calculatro computation
    calculator_result_2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print(calculator_result_2)

    # run calcultaor tests (should be succesful)
    calculator_result_3 = run_python_file(
        "calculator",
        "tests.py",
    )
    print(calculator_result_3)

    # test outside folder with ../ should fail with return error
    calculator_result_4 = run_python_file("calculator", "../main.py")
    print(calculator_result_4)

    # test nonexistent.py should fail with return error
    calculator_result_5 = run_python_file("calculator", "nonexistent.py")
    print(calculator_result_5)

    # test lorem.txt should fail with retutn error
    calculator_result_6 = run_python_file("calculator", "lorem.txt")
    print(calculator_result_6)


if __name__ == "__main__":
    main()
