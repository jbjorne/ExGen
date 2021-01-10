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
    
    def makeAnswer(self, items, space=10):
        if len(items["options"]) == 1:
            return "{1:SA:=" + str(items["correct"]) + "}"
        else:
            for i in range(len(items["options"])):
                item = items["options"][i]
                assert not item.startswith("=")
                if item == items["correct"]:
                    items["options"][i] = "=" + items["options"][i]
            if not items.get("ordered"):
                self.rand.shuffle(items["options"])
            return "{1:MC:" + "~".join(items["options"]) + "}"
    
    def makeURL(self, token):
        return "<a href=\"" + token["link"] + "\">" + self.render(token.get("children")) + "</a>"
    
    def makeTable(self, t):
        return t.toMoodle(self)
    
    def makeCode(self, token):
        return "$$" + token["text"] + "$$"