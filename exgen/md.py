import mistune
import exgen.table as table
import os
import random
import json
from exgen.renderer import LatexRenderer, MoodleRenderer, ExamRenderer

RENDERERS = {"latex":LatexRenderer, "exam":ExamRenderer, "moodle":MoodleRenderer}

def parse(mdPath, data=None):
    markdown = mistune.create_markdown(renderer=mistune.AstRenderer())
    with open(mdPath, "rt") as f:
        tokens = markdown(f.read())
    if data == None:
        data = {}
    return {"tokens":tokens, "data":data}

def renderElements(elements, options):
    content = ""
    for element in elements:
        if content != "":
            content += "\n\n"
        renderer = RENDERERS[options["format"]](element["data"], options)
        content += renderer.render(element["tokens"])
    return content

def renderDoc(elements, options):
    content = renderElements(elements, options)
    if options["format"] == "latex":   
        with open(options["template"], "rt") as f:
            template = f.read()
            template = template.replace("\\titletext{}", options.get("title", "Exercises"))
            template = template.replace("\\content{}", content)
        if options["fileStem"] != None:
            with open(options["fileStem"] + ".tex", "wt") as f:
                f.write(template)
        return template
    else:
        with open(options["fileStem"] + ".html", "wt") as f:
            f.write(content)