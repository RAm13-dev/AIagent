from functions.get_file_stats import get_file_stats

print(get_file_stats("calculator", "pkg/calculator.py"))
print(get_file_stats("calculator", "lorem.txt"))
print(get_file_stats("calculator", "pkg/does_not_exist.py"))
