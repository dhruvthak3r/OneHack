
from sqlalchemy import Column, Integer, String,Date, ForeignKey,DateTime
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
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    reg_start_date = Column(Date, nullable=True)
    reg_end_date = Column(Date, nullable=True)
    mode = Column(String(50), nullable=False)

    platform_id = Column(Integer, ForeignKey('platform.p_id'), nullable=False)

    platform = relationship("Platform", back_populates="hackathons")


class Users(Base):
    """
    Defines the users table
    """
    __tablename__ = 'users'

    sub = Column(String(100), primary_key=True, autoincrement=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    picture = Column(String(200), nullable=True)


