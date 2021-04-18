class LightError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__()
    def __str__(self):
        return self.msg