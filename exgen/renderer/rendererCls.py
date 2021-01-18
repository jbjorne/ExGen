from . import table
import random
import json
from csv import reader

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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

class Renderer:
    def __init__(self, data, options, seed=1):
        self.data = data
        self.options = options
        self.rand = random.Random(seed)
        self.headingLevel = 0
        self.skip = False
    
    def getHeading(self, content):
        raise NotImplementedError
    
    def makeHeading(self, token, children):
        self.headingLevel = token["level"]
        return self.getHeading(self.render(children))

    def makeParagraph(self, tokens):
        raise NotImplementedError

    def makeList(self, tokens):
        raise NotImplementedError

    def makeImage(self, tokens):
        raise NotImplementedError

    def makeExample(self, token):
        raise NotImplementedError

    def makeAnswer(self, items):
        raise NotImplementedError
    
    def makeURL(self, token):
        raise NotImplementedError

    def makeTable(self, table):
        raise NotImplementedError

    def makeCode(self, token):
        raise NotImplementedError

    def render(self, tokens):
        tex = ""
        if tokens != None:
            for token in tokens:
                tt = token["type"]
                children = token.get("children")
                #print(token, tt, children)
                if isinstance(token, str):
                    continue
                span = None
                if tt == "heading":
                    span = self.makeHeading(token, children)
                elif tt == "text":
                    span = token["text"]
                elif tt == "block_text":
                    span = self.render(children)
                elif tt == "paragraph":
                    span = self.makeParagraph(children)
                elif tt == "link":
                    span = self.insertData(token)
                elif tt == "list":
                    span = self.makeList(children)
                elif tt == "image":
                    span = self.makeImage(token)
                elif tt == "codespan":
                    span = self.makeCode(token)
                else:
                    print("Unknown token", token)
                if span not in ("", None) and not self.skip:
                    tex += span
        return tex

    def insertData(self, token):
        data = self.render(token.get("children"))
        args, kwargs = parseArgs(token["link"], "type")
        #print((data, args, kwargs))
        if kwargs["type"] == "example":
            return self.makeExample(token)
        elif kwargs["type"] == "answer":
            args, kwargs = nameArgs(args, kwargs, ["space"])
            kwargs["space"] = int(kwargs["space"]) if kwargs["space"] != None else 5
            return self.getAnswer(token, kwargs["space"])
        elif kwargs["type"] == "solution":
            args, kwargs = nameArgs(args, kwargs, ["pos"])
            if kwargs["pos"] == None:
                kwargs["pos"] = "begin" if self.skip else "end"
            if kwargs["pos"] == "begin":
                if self.options["mode"] == "solutions":
                    self.headingLevel += 1
                    return self.beginSolution()
                else:
                    self.skip = True
                    return None
            elif kwargs["pos"] == "end":
                if self.options["mode"] == "solutions":
                    return self.endSolution()
                else:
                    self.skip = False
                    return None
        elif kwargs["type"] == None and data in self.data:
            return self.getData(data)
        else:
            return self.makeURL(token)
    
    def beginSolution(self):
        raise NotImplementedError

    def endSolution(self):
        raise NotImplementedError

    def getAnswer(self, token, space):
        if isinstance(token, table.Answer):
            content = token.content
        else:
            assert token.get("link").startswith("answer")
            children = token.get("children")
            if len(children) == 1 and children[0]["type"] == "text" and children[0]["text"] in self.data:
                content = children[0]["text"]
            else:
                content = self.render(children)
        if content == None:
            return ""
 
        items = None
        if isinstance(content, str) and not isNumber(content):
            try:
                items = json.loads(content)
                assert isinstance(items,dict), items
            except ValueError as e:
                items = None
        if items is None:
            items = {}
            items["options"] = content.split(";") if isinstance(content, str) and ";" in content else [content]
        if len(items["options"]) > len(set(items["options"])):
            raise Exception("Answer values not unique in " + str(items))
        
        for i in range(len(items["options"])):
            if items["options"][i] in self.data:
                items["options"][i] = self.getData(items["options"][i])
        if "correct" not in items:
            items["correct"] = items["options"][0]
        assert items["correct"] in items["options"]

        items["options"] = [str(x) for x in items["options"]]
        items["correct"] = str(items["correct"])
        return self.makeAnswer(items, space)

    def getData(self, key):
        item = self.data[key]
        if isinstance(item, dict) and item.get("type") == "table":
            item = {x:item[x] for x in item if x != "type"}
            item = table.Table(**item)
        if isinstance(item, table.Table):
            return self.makeTable(item) #table.makeLatexTable(item["rows"], rowheaders=item.get("rowheaders"))
        else:
            return str(item)