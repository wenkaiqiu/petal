class ConflictError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.conflict_function = kwargs['conflict_function']
