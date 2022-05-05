from .. import md
import random
import json

class Renderer:
    def __init__(self, data, options, seed=1, debug=0):
        self.data = data
        self.options = options
        self.rand = random.Random(seed)
        self.headingLevel = 0
        self.skip = False
        self.debug = debug
    
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
                if self.debug >= 2:
                    print(token, tt, children)
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
        # Extract the link value and insert known variables
        linkType = token["link"]
        linkValue = self.render(token.get("children"))
        if linkValue in self.data:
            linkValue = self.data[linkValue]
        if self.debug >= 1:
            print("LINK", {"type":linkType, "value":linkValue})
        
        # Process the link according to its type
        if linkType == "example": # A highlighted example
            return self.makeExample(token)
        elif linkType == "answer":
            return self.processAnswer(linkValue)
        elif linkType.split(":")[0] == "solution":
            if linkType == "solution:begin":
                if self.options["mode"] == "solutions":
                    self.headingLevel += 1
                    return self.beginSolution()
                else:
                    self.skip = True
                    return None
            elif linkType == "solution:end":
                if self.options["mode"] == "solutions":
                    return self.endSolution()
                else:
                    self.skip = False
                    return None
        elif linkType in (None, ""): # An untyped variable
            return self.processVar(linkValue)            
        else:
            return self.makeURL(token)
    
    def processVar(self, value):
        if isinstance(value, dict) and value.get("type") == "table":
            return self.processTable(value)
        else:
            return self.renderString(str(value).strip())
    
    def processTable(self, table):
        if isinstance(table["rows"][0], dict):
            columns = [x for x in table["rows"][0].keys()]
            rows = [columns]
            for row in table["rows"]:
                rows.append([row[col] for col in columns])
            table = {key:value for key, value in table.items()}
            table["rows"] = rows
            table["headers"] = True
        return self.makeTable(table)
    
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
        if self.debug >= 1:
            print("ANSWER", value)
        return self.makeAnswer(value)
    
    def beginSolution(self):
        raise NotImplementedError

    def endSolution(self):
        raise NotImplementedError