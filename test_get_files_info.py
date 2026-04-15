
from functions.get_files_info import get_files_info

def main():
    calculator_result = get_files_info("calculator", ".")
    print(calculator_result)
    
    calculator_pkg_result = get_files_info("calculator", "pkg")
    print(calculator_pkg_result)
    
    calculator_bin_result = get_files_info("calculator", "/bin")
    print(calculator_bin_result)
    
    calculator__result = get_files_info("calculator", "../")
    print(calculator__result)
    

if __name__ == "__main__":
    main()