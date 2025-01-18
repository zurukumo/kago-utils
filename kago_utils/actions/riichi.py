class Riichi:
    def __init__(self) -> None:
        pass

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Riichi)

    def __repr__(self) -> str:
        return "Riichi()"
