from streamlit_elements.core.statement import ReactStatement


class ReactCallback(ReactStatement):
    """React callback."""
    __slots__ = ()

    def __init__(self, callback):
        args = callback.__code__.co_varnames
        body = callback(*(ReactStatement(arg) for arg in args))._serialize()

        super().__init__(f"({','.join(args)})=>{body}")
