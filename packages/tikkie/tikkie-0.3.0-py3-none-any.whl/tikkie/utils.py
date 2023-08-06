from dataclasses import dataclass

from twikey.types import Statement

TIKKIE_ID_PREFIX = "Tikkie ID"


@dataclass
class TikkieMessage:
    tikkie_id: str
    external_id: str
    description: str
    party: str
    iban: str


def is_tikkie_statement(statement: Statement) -> bool:
    return statement.party == "AAB RETAIL INZ TIKKIE"


def parse_tikkie_message(message: str) -> TikkieMessage:
    id_part, external_part, party, iban = message.split(", ")

    if not id_part.startswith(TIKKIE_ID_PREFIX):
        raise ValueError("Invalid Tikkie Message")

    tikkie_id = id_part[len(TIKKIE_ID_PREFIX) + 1 :]

    if not external_part.startswith("E "):
        raise ValueError("Invalid Tikkie Message")

    external_id, description = external_part[2:].split(" ", 1)

    return TikkieMessage(
        tikkie_id=tikkie_id,
        external_id=external_id,
        description=description,
        party=party,
        iban=iban,
    )
