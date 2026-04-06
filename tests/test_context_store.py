from functions.context_store import append_context, load_context

print(append_context("projects", "First local context entry"))
print(append_context("projects", "Second local context entry"))
print(load_context("projects"))
