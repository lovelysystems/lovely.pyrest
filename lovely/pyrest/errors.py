class Errors(list):
    """ A list object which holds a dictionary of errors. And a status code """

    def __init__(self, status=400):
        self.status = status
        super(Errors, self).__init__()

    def add(self, location, desc):
        error = {'location': location,
                 'description': desc}
        self.append(error)
