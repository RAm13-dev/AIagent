from functions.get_files_info import get_files_info

print("Result for current directory:")
print(get_files_info("projects", "."))

print("Result for 'pkg' directory:")
print(get_files_info("projects", "pkg"))

print("Result for '/bin' directory:")
print(get_files_info("projects", "/bin"))

print("Result for '../' directory:")
print(get_files_info("projects", "../"))
