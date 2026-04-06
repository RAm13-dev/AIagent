from functions.search_in_files import search_in_files

print(search_in_files("projects", "Calculator"))
print(search_in_files("projects", "expression", "pkg"))
print(search_in_files("projects", "does-not-exist"))
