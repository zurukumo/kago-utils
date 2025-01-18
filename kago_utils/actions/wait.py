class Wait:
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Wait)

    def __repr__(self) -> str:
        return "Wait()"
