from typing import List
import uvicorn

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud_utils
import tables
import schemas
import utils

from db import SessionLocal, engine

tables.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/promo/")
def create_promo(promoIn: schemas.PromoIn, db: Session = Depends(get_db)):
    """Запустить новую промоакцию"""
    promo_id = crud_utils.post_promo(db, promoIn)
    return promo_id

@app.get("/promo/", response_model=List[schemas.PromoOutWithoutParticipantsAndPrizes])
def get_all_promos(db: Session = Depends(get_db)):
    """Получить все промоакции"""
    return crud_utils.get_promos(db)

@app.get("/promo/{id}", response_model=schemas.PromoOutFull)
def get_promo(id: int, db: Session = Depends(get_db)):
    """Получить полную информацию о промоакции"""
    promo = crud_utils.get_promo_full_information(db, id)
    if promo is None:
        raise HTTPException(status_code=404, detail='Этой промоакции не существует')
    return promo

@app.put('/promo/{id}')
def update_promo(id: int, promoIn: schemas.PromoIn, db: Session = Depends(get_db)):
    """Изменить название и описание промоакции"""
    promo = crud_utils.get_promo_by_id(db, id)
    if promo is None:
        raise HTTPException(status_code=404, detail='Этой промоакции не существует')
    crud_utils.put_promo(db, promoIn, id)
    return status.HTTP_200_OK

@app.delete('/promo/{id}')
def delete_promo(id: int, db: Session = Depends(get_db)):
    """Удалить промоакцию"""
    promo = crud_utils.get_promo_by_id(db, id)
    if promo is None:
        raise HTTPException(status_code=404, detail='Этой промоакции не существует')
    crud_utils.delete_promo(db, id)
    
    return status.HTTP_200_OK

@app.post('/promo/{id}/participant')
def create_participant(id: int, participantIn: schemas.ParticipantIn, db: Session = Depends(get_db)):
    """Создать участника промоакции"""
    return crud_utils.post_participant_in_promo(db, participantIn, id)

@app.delete('/promo/{promoId}/participant/{participantId}')
def delete_participant(promoId: int, participantId: int, db: Session = Depends(get_db)):
    """Удалить участника промоакции"""
    promo = crud_utils.get_promo_by_id(db, promoId)
    if promo is None:
        raise HTTPException(status_code=404, detail='Этой промоакции не существует')
    crud_utils.delete_participant(db, participantId)
    return status.HTTP_200_OK


@app.post('/promo/{id}/prize')
def create_prize(id: int, prizeIn: schemas.PrizeIn, db: Session = Depends(get_db)):
    """Создать приз для промоакции"""
    return crud_utils.post_prize_in_promo(db, prizeIn, id)

@app.delete('/promo/{promoId}/prize/{prizeId}')
def delete_prize(promoId: int, prizeId: int, db: Session = Depends(get_db)):
    """Удалить приз"""
    promo = crud_utils.get_promo_by_id(db, promoId)
    if promo is None:
        raise HTTPException(status_code=404, detail='Этой промоакции не существует')
    crud_utils.delete_prize(db, prizeId)
    return status.HTTP_200_OK

@app.post('/promo/{id}/raffle')
def raffle(id: int, db: Session = Depends(get_db)):
    """Провести розыгрыш"""
    promo = crud_utils.get_promo_by_id(db, id)
    if promo is None:
        raise HTTPException(status_code=404, detail='Этой промоакции не существует')
    return utils.do_raffle(id, db)

if __name__=='__main__':
    uvicorn.run('main:app',host='0.0.0.0', port=8080, reload=True, debug=True)