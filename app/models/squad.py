from sqlalchemy import Column, String, select, Integer, ForeignKey
from app.services.database import Base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from app.models.team import Team

class Squad(Base):
    __tablename__ = "squads"