from kago_utils.hai import Hai


class Dahai:
    __slots__ = ("hai",)

    def __init__(self, hai: Hai) -> None:
        self.hai = hai

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Dahai) and self.hai == other.hai

    def __repr__(self) -> str:
        return f"Dahai(hai={self.hai})"
