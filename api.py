import inspect
import requests

# Read the github file IRI
URI = "https://github.com/edsantoshn/Python-Fibonacci/blob/master/Fibonacci.py"

# Crawl it
URI = URI.replace("github.com", "raw.githubusercontent.com", 1).replace("/blob", "")

print("downloading: ", URI)
raw = requests.get(URI, allow_redirects=True)
with open("files/rawo.py", "w") as fp:
    fp.write(raw.text)
    fp.close()
    print("rawo.py created successfully")

## Inspect it for code parts
# Imports and libraries (for dependencies)
    # to do later
from files import rawo

functions = []
# Function headers
for name, data in inspect.getmembers(rawo, inspect.isfunction):
    sourceCode = inspect.getsource(data)
    argSpec    = inspect.getargspec(data)
    print(argSpec[0])
    functions.append([name, sourceCode])
