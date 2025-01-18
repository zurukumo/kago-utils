class Ronho:
    def __init__(self) -> None:
        pass

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Ronho)

    def __repr__(self) -> str:
        return "Ronho()"
