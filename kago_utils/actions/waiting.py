class Waiting:
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Waiting)

    def __repr__(self) -> str:
        return "Waiting()"
