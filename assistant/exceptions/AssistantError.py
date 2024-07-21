import traceback

class AssistantError(Exception):
    def __init__(self, message, original_exception=None):
        self.message = message
        self.original_exception = original_exception
        self.traceback = traceback.format_exc()
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}\nException from openAI: {type(self.original_exception).__name__} - {str(self.original_exception)}\n\nTraceback:\n{self.traceback}"
