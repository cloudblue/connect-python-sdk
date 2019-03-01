import json


class ActivationTileResponse(object):
    tile = 'Activation succeeded'

    def __init__(self, markdown=None, *args, **kwargs):
        if markdown:
            try:
                self.tile = json.loads(markdown)
            except ValueError:
                self.tile = markdown


class ActivationTemplateResponse(object):
    def __init__(self, template_id):
        self.template_id = template_id
