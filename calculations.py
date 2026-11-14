from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")
ONE_HUNDRED = Decimal("100")

DecimalInput = Decimal | int | float | str


def _to_decimal(value: DecimalInput, name: str) -> Decimal:
    try:
        number = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError(f"{name} must be a valid number.") from error

    if not number.is_finite():
        raise ValueError(f"{name} must be a finite number.")
    return number


def calculate_split(
    number_of_people: int,
    bill: DecimalInput,
    tip_percent: DecimalInput,
) -> tuple[Decimal, Decimal, list[Decimal]]:
    if isinstance(number_of_people, bool) or number_of_people < 1:
        raise ValueError("Number of people must be at least 1.")

    bill_amount = _to_decimal(bill, "Bill")
    tip_rate = _to_decimal(tip_percent, "Tip percentage")

    if bill_amount < 0:
        raise ValueError("Bill cannot be negative.")
    if tip_rate < 0:
        raise ValueError("Tip percentage cannot be negative.")

    bill_amount = bill_amount.quantize(CENT, rounding=ROUND_HALF_UP)
    tip_amount = (bill_amount * tip_rate / ONE_HUNDRED).quantize(
        CENT, rounding=ROUND_HALF_UP
    )
    total_cents = int((bill_amount + tip_amount) * ONE_HUNDRED)
    base_cents, extra_cent_count = divmod(total_cents, number_of_people)

    shares = [
        Decimal(base_cents + (index < extra_cent_count)) / ONE_HUNDRED
        for index in range(number_of_people)
    ]
    return bill_amount, tip_amount, shares
