
import extruct

class Extract_schema:

    '''
    From html input, extracts structured schemas (schema.org)
    Returns list of schemas found

    '''


    def __init__(self, base_url, html):

        self.base_url = base_url
        self.html = html

        self._extract()


    def _extract(self):

        data = extruct.extract(self.html, self.base_url, syntaxes=['microdata', 'opengraph', 'rdfa'], uniform=True)

        results = []

        for i in data:
            results += data[i]


        self.schemas = results