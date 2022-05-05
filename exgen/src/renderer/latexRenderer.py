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
    
    def makeAnswer(self, value):
        #value = var["value"]
        #if not isinstance(value, dict):
        #    value = {"correct":value}
        if value.get("choices") != None:
            listItems = [{"type":"list_item", "children":[{"type":"text", "text":x}]} for x in value["choices"]]
            if self.options.get("answers") == True:
                for item in listItems:
                    if item["children"][0]["text"] == value["correct"]:
                        item["children"][0]["text"] = "\\colorbox{gray!30}{" + str(value["correct"]) + "}"
                        break
            if not value.get("ordered"):
                self.rand.shuffle(listItems)
            return self.makeList(listItems)
        else:
            if self.options.get("answers") == True:
                answer = str(value["correct"])
                span = "\\colorbox{gray!30}{%answer}"
            else:
                answer = value.get("space", 5) * "A "
                span = "\\colorbox{gray!30}{\\phantom{%answer}}"
            if len(answer) > 50:
                answer = "\\parbox{\\textwidth}{" + answer + "}"
            return span.replace("%answer", answer)
    
    def makeURL(self, token):
        return self.render(token.get("children")) + " (\\url{" + token["link"] + "})"
    
    def makeTable(self, item):
        item = self.preprocessTable(item)
        rows = item.get("rows")
        numCols = len(rows[0])

        tex = "\\begin{table}[H]\n"
        tex += "\\centering\n"
        if item.get("caption") != None:
            tex += "\\caption*{" + item.get("caption") + "}\n"
            tex += "\\vspace{-3mm}\n"
        tex += "\\begin{tabular}\n"
        if item.get("rowHeaders"):
            tex += "{" + "c | " + " ".join((numCols - 1) * ["c"]) + "}\n"
        else:
            tex += "{" + " ".join(numCols * ["c"]) + "}\n"  
        tex += "\\hline\n"
        if item.get("headers"):
            tex += " & ".join(["\\textbf{" + str(x) + "}" if x is not None else "" for x in rows[0]]) + " \\\\\n"
            tex += "\\hline\n"
            rows = rows[1:]
        numRow = 0
        for row in rows:
            values = [x for x in row]
            for i in range(numCols):
                if isinstance(values[i], dict) and values[i].get("type") == "answer":
                    values[i] = self.makeAnswer(values[i])
                if item.get("rowHeaders") and i == 0:
                    values[i] = "\\textbf{" + str(row[i]) + "}"
            tex += " & ".join([str(x) if x is not None else "" for x in values]) + " \\\\\n"
            numRow += 1
        tex += "\\hline\n"
        tex += "\\end{tabular}\n\\end{table}"
        return tex
    
    def makeCode(self, token):
        return "$" + token["text"] + "$"