import os
import base64
import xml.etree.ElementTree as ET
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
    
    def makeItalic(self, tokens):
        return "<i>" + self.render(tokens) + "</i>\n"

    def makeBold(self, tokens):
        return "<b>" + self.render(tokens) + "</b>\n"
    
    def makeList(self, tokens):
        tex = "<ol>\n"
        for token in tokens:
            assert token.get("type") == "list_item"
            tex += "    <li>" + self.render(token.get("children")) + "<br></li>\n"
        tex += "</ol>\n"
        return tex

    def makeImage(self, token):
        filename = os.path.join(self.options["outDir"], token["src"])
        with open(filename, "rb") as f:
            encoded = base64.b64encode(f.read()).decode('UTF-8')

        src="data:image/png;base64," + encoded
        #return "<img src=\"" + src + "\"  width=\"500\" height=\1\/>"
        return "<img src=\"" + src + "\" width=\"500\" height=\"1\" class=\"img-responsive atto_image_button_text-bottom\" />"
    
    def makeExample(self, token):
        text = "<span class=\"\" style=\"color: rgb(125, 159, 211);\">"
        text += self.render(token.get("children")) + "</span>"
        return text
    
    def makeAnswer(self, value):
        #print ("MAKE ANSWER", var)
        #value = var["value"]
        #if not isinstance(value, dict):
        #    value = {"correct":value}
        assert isinstance(value, dict), value
        if value.get("choices") != None:
            items = []
            for i in range(len(value["choices"])):
                item = value["choices"][i]
                if isinstance(item, str):
                    assert not item.startswith("=")
                if item == value["correct"]:
                    item = "=" + str(item)
                items.append(str(item))
            if not value.get("ordered"):
                self.rand.shuffle(items)
            return "{1:MC:" + "~".join(items) + "}"
        else:
            assert "correct" in value, value
            return "{1:SA:=" + str(value["correct"]) + "}"
    
    def makeURL(self, token):
        return "<a href=\"" + token["link"] + "\">" + self.render(token.get("children")) + "</a>"
    
    def makeTable(self, item):
        item = self.preprocessTable(item)
        table = ET.Element("table", style="width: 100%;")
        style = "border-width: 1px; border-style: solid; border-color: rgb(51, 51, 51);"
        headRow = ET.SubElement(ET.SubElement(table, "thead"), "tr")
        rows = item["rows"]
        if item.get("headers"):
            for header in rows[0]:
                ET.SubElement(headRow, "th", scope="col", style=style).text = str(header) if header != None else ""
            rows = rows[1:]
        body = ET.SubElement(table, "tbody")
        numCols = len(rows[0])
        numRow = 0
        for row in rows:
            values = [x for x in row]
            for i in range(numCols):
                if isinstance(values[i], dict) and values[i].get("type") == "answer":
                    values[i] = self.makeAnswer(values[i])
                #if self.rowHeaders and i == 0:
                #    values[i] = "\\textbf{" + str(row[i]) + "}"
            rowElem = ET.SubElement(body, "tr")
            for value in values:
                ET.SubElement(rowElem, "td", style=style).text = str(value) if value != None else ""
            numRow += 1
        return ET.tostring(table).decode()
    
    def makeCode(self, token):
        return "$$" + token["text"] + "$$"