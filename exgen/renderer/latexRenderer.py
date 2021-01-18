from .rendererCls import Renderer

class LatexRenderer(Renderer):
    def __init__(self, data, options):
        Renderer.__init__(self, data, options)
    
    def getHeading(self, content):
        heading = "section"
        for i in range(1, self.headingLevel):
            heading = "sub" + heading
        return "\\" + heading + "{" + content + "}\n\n"

    def beginSolution(self):
        return "\\begin{shaded}\n"

    def endSolution(self):
        return "\\end{shaded}\n"
    
    def makeParagraph(self, tokens):
        return self.render(tokens) + "\n\n"
    
    def makeList(self, tokens):
        tex = "\\begin{enumerate}\n"
        for token in tokens:
            assert token.get("type") == "list_item"
            tex += "\\item " + self.render(token.get("children")) + "\n"
        tex += "\\end{enumerate}\n\n"
        return tex

    def makeImage(self, token):
        width = "\\textwidth"
        try:
            weight = float(token.get("alt"))
            width = str(weight) + width
        except ValueError:
            pass
        tex = "\n"
        tex += "\n\\begin{figure}[H]\n"
        tex += "\\centering\n"
        src = token["src"]
        if (not "." in src) and ("imageFormat" in self.options):
            src += "." + self.options["imageFormat"]
        tex += "\\includegraphics[width=" + width + "]{" + src + "}\n"
        tex += "\\end{figure}\n\n"
        return tex
    
    def makeExample(self, token):
        return "\\textcolor{blue}{" + self.render(token.get("children")) + "}"
    
    def makeAnswer(self, var):
        if isinstance(var["value"], dict): # Multiple choice
            listItems = [{"type":"list_item", "children":[{"type":"text", "text":x}]} for x in var["value"]["choices"]]
            if self.options.get("answers") == True:
                assert var["value"]["correct"] == listItems[0]["children"][0]["text"]
                listItems[0]["children"][0]["text"] = "\\colorbox{gray!30}{" + str(var["value"]["correct"]) + "}"
            self.rand.shuffle(listItems)
            return self.makeList(listItems)
        else: # Single value
            if self.options.get("answers") == True:
                answer = str(var["value"])
                span = "\\colorbox{gray!30}{%answer}"
            else:
                answer = var.get("space", 5) * "A "
                span = "\\colorbox{gray!30}{\\phantom{%answer}}"
            if len(answer) > 50:
                answer = "\\parbox{\\textwidth}{" + answer + "}"
            return span.replace("%answer", answer)
    
    def makeURL(self, token):
        return self.render(token.get("children")) + " (\\url{" + token["link"] + "})"
    
    def makeTable(self, t):
        return t.toTex(self)
    
    def makeCode(self, token):
        return "$" + token["text"] + "$"