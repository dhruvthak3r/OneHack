
from sqlalchemy import Column, Integer, String,Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase,relationship


class Base(DeclarativeBase):
    pass


class Platform(Base):
    """
    Defines the platform table
    """
    __tablename__ = 'platform'

    p_id = Column(Integer, primary_key=True,autoincrement=False)
    p_name = Column(String(50), nullable=False)

    hackathons = relationship("Hackathon", back_populates="platform")

class Hackathon(Base):
    """
    Defines the hackathon table
    """
    __tablename__ = 'hackathon'

    Hackathon_id = Column(String(36), primary_key=True,autoincrement=False)
    Hackathon_name = Column(String(200), nullable=False)
    Hackathon_url = Column(String(200), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reg_start_date = Column(Date, nullable=False)
    reg_end_date = Column(Date, nullable=False)
    mode = Column(String(50), nullable=False)

    platform_id = Column(Integer, ForeignKey('platform.p_id'), nullable=False)

    platform = relationship("Platform", back_populates="hackathons")

