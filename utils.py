import random
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import crud_utils
import schemas


def do_raffle(promoId: int, db: Session):
    promo = crud_utils.get_promo_full_information(db, promoId)
    count_paticipants = len(promo.participants)
    count_prizes = len(promo.prizes)
    if count_paticipants != count_prizes:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Количество призов и учатников не совпадают. Участников: {count_paticipants}.Призов: {count_prizes}.')
    participants = promo.participants
    prizes = promo.prizes
    # Меняем случайным образом список подарков и учатников
    random.shuffle(participants)
    random.shuffle(prizes)

    winners = []
    for i in range(count_paticipants):
        winner = schemas.Winner(
            winner=participants[i],
            prize=prizes[i]
        )
        winners.append(winner)

    return winners