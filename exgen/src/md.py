import mistune
from . import table
import os
import random
import json
from .renderer import latexRenderer
from .renderer import moodleRenderer
from .renderer import examRenderer

RENDERERS = {
    "latex":latexRenderer.LatexRenderer, 
    "exam":examRenderer.ExamRenderer, 
    "moodle":moodleRenderer.MoodleRenderer
}

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