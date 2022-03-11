from os import name
from fastapi import HTTPException, status

from typing import List
from sqlalchemy.orm import Session

import tables
import schemas


def get_promo_by_id(db: Session, promo_id: int):
    promo = db.query(tables.Promo).filter(tables.Promo.id == promo_id).first()
    return promo

def get_promo_full_information(db: Session, promo_id: int):
    promo = db.query(tables.Promo).filter(tables.Promo.id == promo_id).first()
    prizes_db = db.query(tables.Prize).filter(tables.Prize.promo_id == promo_id).all()
    participants_db = db.query(tables.Participant).filter(tables.Participant.promo_id == promo_id).all()

    prizes = []
    participants = []

    # сериализуем данные из бд
    for prize in prizes_db:
        _prize = schemas.PrizeOut(
            id=prize.id,
            description=prize.description
        )
        prizes.append(_prize)

    for participant in participants_db:
        _participant = schemas.ParticipantOut(
            id=participant.id,
            name=participant.name
        )
        participants.append(_participant)
    

    promo_out_full = schemas.PromoOutFull(
        name=promo.name,
        description=promo.description,
        id=promo_id,
        prizes=prizes,
        participants=participants
    )


    return promo_out_full

def get_promos(db: Session):
    promos_db = db.query(tables.Promo).all()
    promos = []
    
    for promo in promos_db:
        _promo = schemas.PromoOutWithoutParticipantsAndPrizes(
            id=promo.id,
            name=promo.name,
            description=promo.description
        )
        promos.append(_promo)

    return promos

def post_promo(db: Session, promo: schemas.PromoIn):
    db_promo = tables.Promo(
        name=promo.name,
        description=promo.description
    )
    db.add(db_promo)
    db.commit()
    db.refresh(db_promo)

    result = {
        'id': db_promo.id
    }
    
    return result

def put_promo(db: Session, promo: schemas.PromoIn, promo_id: int):
    db_promo = db.query(tables.Promo).filter(tables.Promo.id == promo_id).first()
  
    db_promo.description = promo.description
    db_promo.name = promo.name
    db.add(db_promo)
    db.commit()
    db.refresh(db_promo)

def delete_promo(db: Session, promo_id: int):
    db_promo = db.query(tables.Promo).filter(tables.Promo.id == promo_id).first()
    
    # удаляем связанные с промоакцией призы и участников
    delete_all_participant_from_promo(db, promo_id)
    delete_all_prize_from_promo(db, promo_id)

    db.delete(db_promo)
    db.commit()

def post_participant_in_promo(db: Session, participant: schemas.ParticipantIn, promo_id: int):
    db_participant = tables.Participant(
        name=participant.name,
        promo_id=promo_id
    )
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)

    result = {
        'id': db_participant.id
    }
    
    return result

def delete_participant(db: Session, participant_id: int):
    db_participant = db.query(tables.Participant).filter(tables.Participant.id == participant_id).first()

    db.delete(db_participant)
    db.commit()

def delete_all_participant_from_promo(db: Session, promo_id: int):
    db_participants = db.query(tables.Participant).filter(tables.Participant.promo_id == promo_id)
    for p in db_participants:
        db.delete(p)

def post_prize_in_promo(db: Session, prize: schemas.PrizeIn, promo_id: int):
    db_prize = tables.Prize(
        description=prize.description,
        promo_id=promo_id
    )
    db.add(db_prize)
    db.commit()
    db.refresh(db_prize)

    result = {
        'id': db_prize.id
    }
    
    return result

def delete_prize(db: Session, prize_id: int):
    db_prize = db.query(tables.Prize).filter(tables.Prize.id == prize_id).first()
    
    db.delete(db_prize)
    db.commit()

def delete_all_prize_from_promo(db: Session, promo_id: int):
    db_prizes = db.query(tables.Prize).filter(tables.Prize.promo_id == promo_id)
    for p in db_prizes:
        db.delete(p)
