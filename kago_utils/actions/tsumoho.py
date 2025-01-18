class Tsumoho:
    def __init__(self) -> None:
        pass

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Tsumoho)

    def __repr__(self) -> str:
        return "Tsumoho()"
