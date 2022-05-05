from .. import md
import random
import json
#from .. import arguments

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
        #var = arguments.parseVar(self.render(token.get("children")), token["link"], self.data)
        linkType = token["link"]
        linkValue = self.render(token.get("children"))
        if linkValue in self.data:
            linkValue = self.data[linkValue]
        #assert "value" not in var, var
        #var["value"] = self.processVar(var["text"])
        #print("LINK", {"type":linkType, "value":linkValue})
        if linkType == "example":
            return self.makeExample(token)
        elif linkType == "answer":
            #arguments.nameUnnamed(var, ["space"])
            #var["space"] = int(var["space"]) if var["space"] != None else 5
            return self.processAnswer(linkValue)
        elif linkType.split(",")[0] == "solution":
            #print("SOLUTION", linkType, linkValue)
            #arguments.nameUnnamed(var, ["pos"])
            #if var["pos"] == None:
            #    var["pos"] = "begin" if self.skip else "end"
            if linkType == "solution,begin": #var["pos"] == "begin":
                if self.options["mode"] == "solutions":
                    self.headingLevel += 1
                    return self.beginSolution()
                else:
                    self.skip = True
                    return None
            elif linkType == "solution,end": #var["pos"] == "end":
                if self.options["mode"] == "solutions":
                    return self.endSolution()
                else:
                    self.skip = False
                    return None
        elif linkType in (None, ""):
            return self.insertVar(linkValue)
        else:
            return self.makeURL(token)
    
    def processAnswer(self, value):
        if not isinstance(value, dict):
            if isinstance(value, str):
                value = value.strip()
                if value.startswith("{") and value.endswith("}"):
                    value = json.loads(value)
                elif value.startswith("[") and value.endswith("]"):
                    value = json.loads(value)
                    value = {"choices":value, "correct":value[0]}
                elif not value[0] in ["'", "\""] and not value[-1] in ["'", "\""] and ";" in value:
                    value = value.split(";")
                    value = {"choices":value, "correct":value[0]}
                else:
                    value = {"correct":value}
            else:
                value = {"correct":value}
        #print("ANSWER", value)
        return self.makeAnswer(value)
    
    def beginSolution(self):
        raise NotImplementedError

    def endSolution(self):
        raise NotImplementedError

    def insertVar(self, value):
        if isinstance(value, dict) and value.get("type") == "table":
            return self.makeTable(value)
        else:
            #print("INSERT VAR", var)
            return self.renderString(str(value).strip())
    
    # Utilities ###############################################################

    def isNumber(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def preprocessTable(self, table):
        if isinstance(table["rows"][0], dict):
            columns = [x for x in table["rows"][0].keys()]
            rows = [columns]
            for row in table["rows"]:
                rows.append([row[col] for col in columns])
            table = {key:value for key, value in table.items()}
            table["rows"] = rows
            table["headers"] = True
        return table