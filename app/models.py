from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,String,Date
from . import db,app

class Patients(db.Model):
    id: Mapped[int]=mapped_column(primary_key=True,nullable=False)
    Name: Mapped[str]= mapped_column(String(50),nullable=False)
    Address: Mapped[str] = mapped_column(String(200),nullable=False)
    Contact:Mapped[str] = mapped_column(String(20),nullable=False)
    Age:Mapped[int]= mapped_column(nullable=False)
    date:Mapped[str]=mapped_column(String(20),nullable=False)
    UHID:Mapped[str]=mapped_column(String(100),nullable=False,unique=True)
    opd:Mapped[str]=mapped_column(String(100),nullable=False)
    consultantName:Mapped[str]= mapped_column(String(100),nullable=False)
                                              