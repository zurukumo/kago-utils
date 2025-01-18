class Skip:
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Skip)

    def __repr__(self) -> str:
        return "Skip()"
