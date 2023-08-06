class VocabularyValidator(object):
    def __init__(self, vocabulary):
        self.vocabulary = vocabulary

    def __call__(self, request, schema, field, value, mode=None):
        vocab = request.app.get_vocabulary(request=request, name=self.vocabulary)
        if vocab is None:
            return "Configuration error: Unknown vocabulary {}".format(self.vocabulary)

        found = False
        for v in vocab:
            if v["value"] == value:
                found = True
                break

        if not found:
            return "Invalid value: {}".format(value)
