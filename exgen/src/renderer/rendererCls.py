from .. import table
from .. import md
import random
import json
from .. import arguments

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
    
    def renderString(self, s):
        return self.render(md.parseString(s), True) if s != "" else s
    
    def getHeading(self, content):
        raise NotImplementedError
    
    def makeHeading(self, token, children):
        self.headingLevel = token["level"]
        return self.getHeading(self.render(children))

    def makeParagraph(self, tokens):
        raise NotImplementedError
    
    def makeItalic(self, tokens):
        raise NotImplementedError
    
    def makeBold(self, tokens):
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

    def render(self, tokens, skipParagraph=False):
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
                    if skipParagraph:
                        span = self.render(children)
                    else:
                        span = self.makeParagraph(children)
                elif tt == "link":
                    span = self.processLink(token)
                elif tt == "list":
                    span = self.makeList(children)
                elif tt == "image":
                    span = self.makeImage(token)
                elif tt == "codespan":
                    span = self.makeCode(token)
                elif tt == "emphasis":
                    span = self.makeItalic(children)
                elif tt == "strong":
                    span = self.makeBold(children)
                else:
                    print("Unknown token", token)
                if span not in ("", None) and not self.skip:
                    tex += span
        return tex

    def processLink(self, token):
        var = arguments.parseVar(self.render(token.get("children")), token["link"], self.data)
        #print("LINK", token, var)
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

    def insertVar(self, var):
        item = var["value"]
        if isinstance(item, dict) and item.get("type") == "table":
            item = {x:item[x] for x in item if x != "type"}
            item = table.Table(**item)
        if isinstance(item, table.Table):
            return self.makeTable(item) #table.makeLatexTable(item["rows"], rowheaders=item.get("rowheaders"))
        else:
            #print("INSERT VAR", var)
            return self.renderString(str(item).strip())