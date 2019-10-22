class FileProperties:
    def __init__(self, name=None, date=None, length=None, url=None):
        self.name = name
        self.date = date
        self.length = length
        self.url = url

    def __str__(self):
        return "[name={}, date={}, length={}, url={}]".format(self.name, self.date, self.length, self.url)

    def __repr__(self):
        return str(self)