from functions.get_file_content import get_file_content


def main():
    file_content = get_file_content("calculator", "lorem.txt")
    try:
        print(f"--- {file_content} ---")
    except FileNotFoundError:
        print("File not found.")
        
    file_content_1 = get_file_content("calculator", "main.py")
    try:
        print(f"--- {file_content_1} ---")
    except FileNotFoundError:
        print("File not found.")

    file_content_2 = get_file_content("calculator", "pkg/calculator.py")
    try:
        print(f"--- {file_content_2} ---")
    except FileNotFoundError:
        print("File not found.")
    
    
    file_content_3 = get_file_content("calculator", "/bin/cat")
    try:
        print(f"--- {file_content_3} ---")
    except FileNotFoundError:
        print("File not found.")
    
    file_content_4 = get_file_content("calculator", "pkg/does_not_exist.py")
    try:
        print(f"--- {file_content_4} ---")
    except FileNotFoundError:
        print("File not found.")
    
    
if __name__ == "__main__":
    main()
