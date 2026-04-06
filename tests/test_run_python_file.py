from functions.run_python_file import run_python_file

print(run_python_file("projects", "main.py"))
print(run_python_file("projects", "main.py", ["3 + 5"]))
print(run_python_file("projects", "tests.py"))
print(run_python_file("projects", "../main.py"))
print(run_python_file("projects", "nonexistent.py"))
print(run_python_file("projects", "lorem.txt"))