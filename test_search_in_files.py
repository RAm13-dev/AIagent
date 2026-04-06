from functions.search_in_files import search_in_files

print(search_in_files("calculator", "Calculator"))
print(search_in_files("calculator", "expression", "pkg"))
print(search_in_files("calculator", "does-not-exist"))
