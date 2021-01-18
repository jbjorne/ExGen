from . import table
import random
import json
from . import arguments

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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
                    span = self.processLink(token)
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

    def processLink(self, token):
        var = arguments.parseVar(self.render(token.get("children")), token["link"], self.data)
        print(var)
        if var["type"] == "example":
            return self.makeExample(token)
        elif var["type"] == "answer":
            arguments.nameUnnamed(var, ["space"])
            var["space"] = int(var["space"]) if var["space"] != None else 5
            return self.makeAnswer(var)
        elif var["type"] == "solution":
            arguments.nameUnnamed(var, ["pos"])
            if var["pos"] == None:
                var["pos"] = "begin" if self.skip else "end"
            if var["pos"] == "begin":
                if self.options["mode"] == "solutions":
                    self.headingLevel += 1
                    return self.beginSolution()
                else:
                    self.skip = True
                    return None
            elif var["pos"] == "end":
                if self.options["mode"] == "solutions":
                    return self.endSolution()
                else:
                    self.skip = False
                    return None
        elif var["type"] == None:
            return self.insertVar(var)
        else:
            return self.makeURL(token)
    
    def beginSolution(self):
        raise NotImplementedError

    def endSolution(self):
        raise NotImplementedError

    # def insertAnswer(self, var):
    #     assert var["type"] == "answer"
    #     if isinstance(var["value"], table.Answer):
    #         content = var["value"]
    #     else:
    #         assert token.get("link").startswith("answer")
    #         children = token.get("children")
    #         if len(children) == 1 and children[0]["type"] == "text" and children[0]["text"] in self.data:
    #             content = children[0]["text"]
    #         else:
    #             content = self.render(children)
    #     if content == None:
    #         return ""
 
    #     items = None
    #     if isinstance(content, str) and not isNumber(content):
    #         try:
    #             items = json.loads(content)
    #             assert isinstance(items,dict), items
    #         except ValueError as e:
    #             items = None
    #     if items is None:
    #         items = {}
    #         items["options"] = content.split(";") if isinstance(content, str) and ";" in content else [content]
    #     if len(items["options"]) > len(set(items["options"])):
    #         raise Exception("Answer values not unique in " + str(items))
        
    #     for i in range(len(items["options"])):
    #         if items["options"][i] in self.data:
    #             items["options"][i] = self.getData(items["options"][i])
    #     if "correct" not in items:
    #         items["correct"] = items["options"][0]
    #     assert items["correct"] in items["options"]

    #     items["options"] = [str(x) for x in items["options"]]
    #     items["correct"] = str(items["correct"])
    #     return self.makeAnswer(items, space)

    def insertVar(self, var):
        item = var["value"]
        if isinstance(item, dict) and item.get("type") == "table":
            item = {x:item[x] for x in item if x != "type"}
            item = table.Table(**item)
        if isinstance(item, table.Table):
            return self.makeTable(item) #table.makeLatexTable(item["rows"], rowheaders=item.get("rowheaders"))
        else:
            return str(item)