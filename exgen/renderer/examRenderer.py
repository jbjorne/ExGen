from .moodleRenderer import MoodleRenderer

class ExamRenderer(MoodleRenderer):
    def __init__(self, data, options):
        MoodleRenderer.__init__(self, data, options)
    
    def makeAnswer(self, items, space):
        assert len(items["options"]) == 1, items["options"]
        answer = items["options"][0]

        #template = """<span case-sensitive="%case" class="marker" cloze="true" id="%id" numeric="%numeric" precision="0" style="border:1px solid">%answer</span>"""
        #template = template.replace("%case", "false")
        #template = template.replace("%id", "$111")
        template = """<s>%answer</s>"""
        template = template.replace("%answer", str(answer))
        #template = template.replace("%numeric", str(items["correct"].isdigit()).lower())
        assert "%" not in template, template
        return template