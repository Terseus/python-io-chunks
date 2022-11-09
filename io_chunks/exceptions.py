class ClosedStreamError(ValueError):
    def __init__(self):
        super().__init__("I/O operation on closed chunk")
