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
    
    def makeAnswer(self, items, space):
        if len(items["options"]) > 1:
            listItems = [{"type":"list_item", "children":[{"type":"text", "text":x}]} for x in items["options"]]
            if self.options.get("answers") == True:
                assert items["correct"] == listItems[0]["children"][0]["text"]
                listItems[0]["children"][0]["text"] = "\\colorbox{gray!30}{" + str(items["correct"]) + "}"
            self.rand.shuffle(listItems)
            return self.makeList(listItems)
        else:
            if self.options.get("answers") == True:
                answer = str(items["correct"])
                span = "\\colorbox{gray!30}{%answer}"
            else:
                #answer = "\\phantom{" + (space * "A ") + "}"
                answer = space * "A "
                span = "\\colorbox{gray!30}{\\phantom{%answer}}"
            if len(answer) > 50:
                answer = "\\parbox{\\textwidth}{" + answer + "}"
            return span.replace("%answer", answer)

            # if self.options.get("answers") == True:
            #     return "\\colorbox{gray!30}{\\parbox{\\textwidth}{" + str(items["correct"]) + "}}"
            # else:
            #     return "\\colorbox{gray!30}{\\parbox{\\textwidth}\\phantom{" + (space * "A ") + "}}"
            #     #return "\\hlc[gray!30]{}"
            #     #return "\\begin{mycolorbox}[colback=gray!30,hbox]" + (space * "A ") + "\\end{mycolorbox}"
            #     #return "\\colorbox{gray!30}{\\phantom{" + (space * "A ") + "}}"
            #     #return "\\begin{shaded}" + (space * "A ") +  "\\end{shaded}\n"
    
    def makeURL(self, token):
        return self.render(token.get("children")) + " (\\url{" + token["link"] + "})"
    
    def makeTable(self, t):
        return t.toTex(self)
    
    def makeCode(self, token):
        return "$" + token["text"] + "$"