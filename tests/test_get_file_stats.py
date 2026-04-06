from functions.get_file_stats import get_file_stats

print(get_file_stats("projects", "pkg/calculator.py"))
print(get_file_stats("projects", "lorem.txt"))
print(get_file_stats("projects", "pkg/does_not_exist.py"))
