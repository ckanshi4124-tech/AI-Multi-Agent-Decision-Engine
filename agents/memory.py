class SimpleMemory:
    def __init__(self):
        self.history = []

    def add(self, user_input, result=None):
        self.history.append({
            "query": user_input,
            "result": result
        })

    def get_history(self):
        return self.history

    def get_last(self, n=3):
        return self.history[-n:]

    def clear(self):
        self.history = []
        