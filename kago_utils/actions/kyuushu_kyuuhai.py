class KyuushuKyuuhai:
    def __eq__(self, other: object) -> bool:
        return isinstance(other, KyuushuKyuuhai)

    def __repr__(self) -> str:
        return "KyuushuKyuuhai()"
