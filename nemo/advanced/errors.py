class Error404(Exception):
    def __init__(self, message="Page not found"):
        self.message = message
