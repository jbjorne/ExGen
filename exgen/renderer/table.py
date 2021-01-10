import xml.etree.ElementTree as ET
from . import md

class Answer():
    def __init__(self, content):
        self.content = content

class Table():
    def __init__(self, rows, headers=False, rowHeaders=False, caption=None):
        self.rows = rows
        self.numCols = len(rows[0])
        self.headers = headers
        self.rowHeaders = rowHeaders
        self.caption = caption
    
    def toTex(self, renderer):
        tex = "\\begin{table}[H]\n"
        tex += "\\centering\n"
        if self.caption != None:
            tex += "\\caption*{" + self.caption + "}\n"
            tex += "\\vspace{-3mm}\n"
        tex += "\\begin{tabular}\n"
        if self.rowHeaders:
            tex += "{" + "c | " + " ".join((self.numCols - 1) * ["c"]) + "}\n"
        else:
            tex += "{" + " ".join(self.numCols * ["c"]) + "}\n"  
        tex += "\\hline\n"
        rows = self.rows
        if self.headers:
            tex += " & ".join(["\\textbf{" + str(x) + "}" if x is not None else "" for x in rows[0]]) + " \\\\\n"
            tex += "\\hline\n"
            rows = rows[1:]
        numRow = 0
        for row in rows:
            values = [x for x in row]
            for i in range(self.numCols):
                if isinstance(values[i], Answer):
                    values[i] = renderer.getAnswer(values[i])
                if self.rowHeaders and i == 0:
                    values[i] = "\\textbf{" + str(row[i]) + "}"
            tex += " & ".join([str(x) if x is not None else "" for x in values]) + " \\\\\n"
            numRow += 1
        tex += "\\hline\n"
        tex += "\\end{tabular}\n\\end{table}"
        return tex

    def toMoodle(self, renderer):
        table = ET.Element("table")
        #style = "border: 1px solid black;"
        style = """ border="1" cellpadding="1" cellspacing="1" style="width:500px" """
        headRow = ET.SubElement(ET.SubElement(table, "thead"), "tr")
        rows = self.rows
        if self.headers:
            for header in rows[0]:
                ET.SubElement(headRow, "th", scope="col", style=style).text = str(header) if header != None else ""
            rows = rows[1:]
        body = ET.SubElement(table, "tbody")
        numRow = 0
        for row in rows:
            values = [x for x in row]
            for i in range(self.numCols):
                if isinstance(values[i], Answer):
                    values[i] = renderer.getAnswer(values[i])
                #if self.rowHeaders and i == 0:
                #    values[i] = "\\textbf{" + str(row[i]) + "}"
            rowElem = ET.SubElement(body, "tr")
            for value in values:
                ET.SubElement(rowElem, "td", style=style).text = str(value)
            numRow += 1
        return ET.tostring(table).decode()

# def makeMoodleTable(array, colHeaders, rowHeaders, caption, formatter=None):
#     table = ET.Element("table")
#     style = "border: 1px solid black;"
#     ET.SubElement(table, "caption").text = caption
#     headRow = ET.SubElement(ET.SubElement(table, "thead"), "tr")
#     ET.SubElement(headRow, "th", scope="col", style=style) # Add the corner
#     for header in colHeaders:
#         ET.SubElement(headRow, "th", scope="col", style=style).text = header
#     body = ET.SubElement(table, "tbody")
#     for i in range(array.shape[0]):
#         row = ET.SubElement(body, "tr")
#         ET.SubElement(row, "th", scope="row", style=style).text = rowHeaders[i]
#         for j in range(array.shape[1]):
#             ET.SubElement(row, "td", style=style).text = str(array[i,j])
#     return ET.tostring(table).decode()

#def makeLatexTable(rows, headers=True, rowheaders=False, caption=None, options=None):


