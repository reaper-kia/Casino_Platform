from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Money:
    amount_minor: int
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount_minor < 0:
            raise ValueError("Money amount cannot be negative")

        normalized_currency = self.currency.strip().upper()

        if len(normalized_currency) != 3:
            raise ValueError("Currency must be a three-letter code")

        object.__setattr__(self, "currency", normalized_currency)
