import inspect


class CallableFirstParameterExtractor:
    @staticmethod
    def extract(_callable):
        if not hasattr(_callable, "__call__"):
            return None

        signature = inspect.signature(_callable.__call__)
        parameters = list(signature.parameters.values())

        if len(parameters) < 1:
            return None

        first_param = parameters[0]
        return (
            first_param.annotation if first_param.annotation != inspect._empty else None
        )
