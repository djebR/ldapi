import inspect
import requests
import os 
import errno
import re
import sys

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
    
# Specify the URI of the code file as an argument
URI = sys.argv[1]
#URI = "https://github.com/agrdivyam99/Byld-HackEve-1/blob/master/fib1.py"

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

# Arguments: rdfs:label "param", func:defaultValue ""^^xsd:type, rdfs:type xsd:type(or class or whatever), fun:required "true, false"^^xsd:boolean
# Function: func:hasName "", func:hasArguments [list], func:language lan:Python3_7, func:code "code"^^xsd:string

j = 0
# Function headers
for name, data in inspect.getmembers(rawo, inspect.isfunction):
    j = j + 1
    sourceCode = inspect.getsource(data)
    argSpec    = inspect.signature(data)
    functions.append([name, sourceCode, argSpec])
    print(str(j) + " : " + name)

functionNumber = input('Choose a function to be reified into RDF code: ')

with openAndCreate("var/output.nt") as fpttl:
    rdfTurtle = ""
    i = 0
    fName, fSource, fArgs = functions[int(functionNumber)-1]


    rdfTurtle += f"ex:{fName.capitalize()+str(i)} rdfs:label '{fName}'^^xsd:string.\n"
    rdfTurtle += f"ex:{fName.capitalize()+str(i)} func:code {repr(fSource)}^^xsd:string.\n"
    for param in fArgs.parameters.values():
        rdfTurtle += f"ex:{fName.capitalize()+str(i)} func:argument ex:{fName.capitalize()+str(i)+'_'+param.name}.\n"
        rdfTurtle += f"ex:{fName.capitalize()+str(i)+'_'+param.name} rdfs:label '{param.name}'^^xsd:string.\n"
        
        # to do: add the type to the default value (if exist in xsd)
        if(param.default is not param.empty):
            rdfTurtle += f"ex:{fName.capitalize()+str(i)+'_'+param.name} func:defaultValue '{param.default}'.\n"
        
        # To do: map referenceable types instead of annotations (either existing or create)
        if(param.annotation is not param.empty):
            rdfTurtle += f"ex:{fName.capitalize()+str(i)+'_'+param.name} rdf:type '{param.annotation}'.\n"
    fpttl.write(rdfTurtle)
    fpttl.close()
    print('RDF written successfully.')
