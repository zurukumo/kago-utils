from kago_utils.hai import Hai


class Tsumoho:
    def __init__(self) -> None:
        pass

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Tsumoho)

    def __repr__(self) -> str:
        return "Tsumoho()"


class Ronho:
    def __init__(self) -> None:
        pass

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Ronho)

    def __repr__(self) -> str:
        return "Ronho()"


class Riichi:
    def __init__(self) -> None:
        pass

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Riichi)

    def __repr__(self) -> str:
        return "Riichi()"


class Dahai:
    __slots__ = ("hai",)

    def __init__(self, hai: Hai) -> None:
        self.hai = hai

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Dahai) and self.hai == other.hai

    def __repr__(self) -> str:
        return f"Dahai(hai={self.hai})"


class Waiting:
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Waiting)

    def __repr__(self) -> str:
        return "Waiting()"
