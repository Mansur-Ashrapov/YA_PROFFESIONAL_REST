from typing import List, Optional

from pydantic import BaseModel


class PrizeIn(BaseModel):
    description: str


class PrizeOut(PrizeIn):
    id: int


class ParticipantIn(BaseModel):
    name: str


class ParticipantOut(ParticipantIn):
    id: int


class PromoIn(BaseModel):
    name: str
    description: Optional[str] = None


class PromoOutWithoutParticipantsAndPrizes(PromoIn):
    id: int


class PromoOutFull(PromoOutWithoutParticipantsAndPrizes):
    prizes: List[PrizeOut]
    participants: List[ParticipantOut]


class Winner(BaseModel):
    winner: ParticipantOut
    prize: PrizeOut
