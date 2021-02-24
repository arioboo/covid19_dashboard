class Lista(list):
    def __init__(self):
        super(list).__init__()
    
    def to_leandict(self):
        return {k:k for k in self}