from .rendererCls import Renderer

class MoodleRenderer(Renderer):
    def __init__(self, data, options):
        Renderer.__init__(self, data, options)
    
    def getHeading(self, content):
        heading = "h" + str(self.headingLevel)
        return "<" + heading + ">" + content + "<br></" + heading + ">\n"
    
    def beginSolution(self):
        return ""

    def endSolution(self):
        return ""
    
    def makeParagraph(self, tokens):
        return "<p>" + self.render(tokens) + "</p>\n"
    
    def makeList(self, tokens):
        tex = "<ol>\n"
        for token in tokens:
            assert token.get("type") == "list_item"
            tex += "    <li>" + self.render(token.get("children")) + "<br></li>\n"
        tex += "</ol>\n"
        return tex

    def makeImage(self, token):
        width = 1.0
        try:
            weight = float(token.get("alt"))
            width = 0.0
        except ValueError:
            pass
        tex = "<p><img src=\"\" class=\"img-responsive atto_image_button_text-bottom\"></p>\n"
        #return tex
        return "[[[" + token["src"] + "]]]"
    
    def makeExample(self, token):
        text = "<span class=\"\" style=\"color: rgb(125, 159, 211);\">"
        text += self.render(token.get("children")) + "</span>"
        return text
    
    def makeAnswer(self, var):
        if isinstance(var["value"], dict):
            value = var["value"]
            items = []
            for i in range(len(value["choices"])):
                item = value["choices"][i]
                assert not item.startswith("=")
                if item == value["correct"]:
                    item = "=" + str(item)
                items.append(str(item))
            if not value.get("ordered"):
                self.rand.shuffle(items)
            return "{1:MC:" + "~".join(items) + "}"
        else:
            return "{1:SA:=" + str(var["value"]) + "}"
    
    def makeURL(self, token):
        return "<a href=\"" + token["link"] + "\">" + self.render(token.get("children")) + "</a>"
    
    def makeTable(self, t):
        return t.toMoodle(self)
    
    def makeCode(self, token):
        return "$$" + token["text"] + "$$"