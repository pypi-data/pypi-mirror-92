class NewsItem:
    """
    A simple news item consisting of a title and body text.
    """
    def __init__(self, title, body, source):
        self.title = title
        self.body = body.replace("=92", "'")
        self.source = source
