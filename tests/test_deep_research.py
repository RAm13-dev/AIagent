from functions.deep_research import deep_research

print("Testing deep_research empty query")
result = deep_research("projects", "")
print(result)
assert result == "Error: query must not be empty"

print("Testing deep_research basic query")
result = deep_research("projects", "python programming", max_results=1)
print(result)
assert isinstance(result, dict) or isinstance(result, str)
if isinstance(result, dict):
    assert result["query"] == "python programming"
    assert isinstance(result["results"], list)
    assert len(result["results"]) <= 1
