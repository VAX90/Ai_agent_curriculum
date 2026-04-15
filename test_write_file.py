from functions.write_file import write_file
import shutil
import os


def run_test(working_directory, file_path, content):
    print(f"Testing: write_file('{working_directory}', '{file_path}', '{content}')")

    result = write_file(working_directory, file_path, content)
    print("Result:", result)

    # Se è un successo, controlla file
    if result.startswith("Successfully"):
        full_path = os.path.join(working_directory, file_path)

        print("File exists:", os.path.exists(full_path))

        if os.path.exists(full_path):
            with open(full_path, "r") as f:
                print("File content:", f.read())

        # cleanup
        if os.path.exists(working_directory):
            shutil.rmtree(working_directory)

    print("-" * 40)


def main():
    run_test("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    run_test("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    run_test("calculator", "/tmp/temp.txt", "this should not be allowed")


if __name__ == "__main__":
    main()