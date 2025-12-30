
class EnumMixin:
    @classmethod
    def from_str(cls, value: str) -> "EnumMixin":
        return cls[value]

    @classmethod
    def from_int(cls, value: int) -> "EnumMixin":
        return cls(value)

    def __str__(self) -> str:
        return self.name
