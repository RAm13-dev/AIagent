from functions.get_directory_info import get_directory_info

print(get_directory_info("projects", "."))
print(get_directory_info("projects", "pkg"))
print(get_directory_info("projects", "does_not_exist"))
