from csv import reader
import json

def parseArgsList(text):
    args = []
    kwargs = {}
    parts = [x for x in reader([text], skipinitialspace=True)][0]
    #print("PARTS", text, parts)
    for part in parts:
        name = None
        arg = part
        if "=" in part:
            namePart, argPart = [x.strip() for x in part.split("=", 1)]
            if namePart.isalnum():
                name = namePart
                argPart = argPart
        # Process the argument
        arg = arg.strip("\"").strip("'")
        try:
            f = float(data)
            i = int(data)
            arg = [i if i == f else f]
        except:
            pass
        # Assign the argument
        if name != None:
            kwargs[name] = arg
        else:
            args.append(arg)
    return args, kwargs

def parseArgs(text, mainArgName=None):
    args = []
    kwargs = {}
    if text != None:
        text = text.strip()
    if text != None and text != "":
        if text.startswith("[") or text.startswith("{"): # Try to parse the argument as a JSON object
            jsonObj = None
            try:
                jsonObj = json.loads(text)
            except:
                pass
            if jsonObj != None:
                if isinstance(jsonObj, list):
                    args = jsonObj
                elif isinstance(jsonObj, dict):
                    kwargs = jsonObj
                else:
                    raise Exception("Unsupported JSON object " + str(jsonObj))
        else:
            args, kwargs = parseArgsList(text)
    if mainArgName != None:
        args, kwargs = nameArgs(args, kwargs, [mainArgName])
    return args, kwargs

def nameArgs(args, kwargs, names):
    for i in range(len(names)):
        name = names[i]
        if name in kwargs:
            raise Exception("Multiple values for argument '" + name + "'")
        kwargs[name] = args[i] if i < len(args) else None
    args = args[len(names):]
    return args, kwargs