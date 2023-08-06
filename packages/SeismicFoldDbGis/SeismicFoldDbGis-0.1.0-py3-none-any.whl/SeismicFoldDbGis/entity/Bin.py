from sqlalchemy import Column, Integer
from geoalchemy2 import Geometry
from SeismicFoldDbGis.entity.Base import Base

TABLE_NAME_BIN = 'bins'


class Bin(Base):
    __tablename__ = TABLE_NAME_BIN
    id = Column(Integer, primary_key=True)
    binn = Column(Integer, index=True, unique=True)
    fold = Column(Integer)
    geom = Column(Geometry(geometry_type='POINT', management=True))

