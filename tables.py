from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class Promo(Base):
    __tablename__ = "promos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

    prizes = relationship("Prize", back_populates="promo")
    participants = relationship("Participant", back_populates="promo")


class Prize(Base):
    __tablename__ = "prizes"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    promo_id = Column(Integer, ForeignKey('promos.id'))

    promo = relationship("Promo", back_populates="prizes")


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    promo_id = Column(Integer, ForeignKey('promos.id'))

    promo = relationship("Promo", back_populates="participants")
