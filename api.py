import inspect
import requests
import os 
import errno
import re

# Function to make directories if they don't exist
def openAndCreate(path):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(os.path.dirname(path)):
            pass
        else:
            raise
    return open(path, 'w')
    
# Read the github file IRI
URI = "https://github.com/belambert/edit-distance/blob/master/edit_distance/code.py"

# Crawl it
URI = URI.replace("github.com", "raw.githubusercontent.com", 1).replace("/blob", "")

print("downloading: ", URI)
raw = requests.get(URI, allow_redirects=True)
with openAndCreate("downloads/rawo.py") as fp:
    fp.write(raw.text)
    fp.close()
    print("rawo.py created successfully")

## Inspect it for code parts
# Imports and libraries (for dependencies)
    # to do later

from downloads import rawo

functions = []

# Function template

# Parameters: rdfs:label "param", rdfs:defaultValue ""^^xsd:type, rdfs:type xsd:type(or class or whatever), fun:required "true, false"^^xsd:boolean
# Function: fun:hasName "", fun:hasArguments [list], fun:language lan:Python3_7, fun:code "code"^^xsd:string

# Function headers
for name, data in inspect.getmembers(rawo, inspect.isfunction):
    sourceCode = inspect.getsource(data)
    argSpec    = inspect.signature(data)
    functions.append([name, sourceCode, argSpec])

with openAndCreate("var/output.nt") as fpttl:
    rdfTurtle = ""
    i = 0
    for function in functions:
        fName, fSource, fArgs = function
        rdfTurtle += f"func:{fName.capitalize()+str(i)} rdfs:label '{fName}'^^xsd:string.\n"
        rdfTurtle += f"func:{fName.capitalize()+str(i)} func:code {repr(fSource)}^^xsd:string.\n"
        for param in fArgs.parameters.values():
            rdfTurtle += f"func:{fName.capitalize()+str(i)} fun:hasArgument func:{fName.capitalize()+str(i)+'_'+param.name}.\n"
            rdfTurtle += f"func:{fName.capitalize()+str(i)+'_'+param.name} rdfs:label '{param.name}'^^xsd:string.\n"
            if(param.default is not param.empty):
                rdfTurtle += f"func:{fName.capitalize()+str(i)+'_'+param.name} func:defaultValue '{param.default}'.\n"
            if(param.annotation is not param.empty):
                rdfTurtle += f"func:{fName.capitalize()+str(i)+'_'+param.name} func:parameterType '{param.annotation}'.\n"
    fpttl.write(rdfTurtle)
    fpttl.close()
