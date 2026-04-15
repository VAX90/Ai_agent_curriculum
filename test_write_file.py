from functions.write_file import write_file
import os
    


def test_write_file(working_directory, file_path, content):
    result = write_file(working_directory, file_path, content)
    assert result == f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    assert os.path.exists(f"{working_directory}/{file_path}")
    with open(f"{working_directory}/{file_path}", "r") as f:
        assert f.read() == content
    os.remove(f"{working_directory}/{file_path}")
    os.rmdir(working_directory)
    
    
def main():
    test_write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    test_write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    test_write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    
if __name__ == "__main__":
    main()
