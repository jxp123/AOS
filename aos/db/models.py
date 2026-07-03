from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from aos.db.session import Base

class SystemMeta(Base):
    __tablename__ = 'system_meta'
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(String, default='')

class Colony(Base):
    __tablename__ = 'colonies'
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    colony_type = Column(String, default='Hive')
    equipment = Column(String, default='Unknown')
    objective = Column(String, default='')
    status = Column(String, default='Active')
    notes = Column(Text, default='')
    inspections = relationship('Inspection', back_populates='colony', cascade='all, delete-orphan')

class Queen(Base):
    __tablename__ = 'queens'
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, default='')
    line = Column(String, default='Unknown')
    source = Column(String, default='')
    current_colony_code = Column(String, default='')
    status = Column(String, default='Active')
    evidence_status = Column(String, default='Unknown')
    temperament_score = Column(Float, default=0)
    brood_score = Column(Float, default=0)
    honey_score = Column(Float, default=0)
    notes = Column(Text, default='')

class Equipment(Base):
    __tablename__ = 'equipment'
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, default='Unknown')
    current_location = Column(String, default='')
    compatible_with = Column(String, default='Unknown')
    status = Column(String, default='')
    notes = Column(Text, default='')

class Inspection(Base):
    __tablename__ = 'inspections'
    id = Column(Integer, primary_key=True)
    colony_id = Column(Integer, ForeignKey('colonies.id'), nullable=False)
    date = Column(String, nullable=False)
    inspection_type = Column(String, default='Brood')
    queen_seen = Column(Boolean, default=False)
    eggs_seen = Column(Boolean, default=False)
    larvae_seen = Column(Boolean, default=False)
    queen_cells = Column(Integer, default=0)
    brood_frames = Column(Float, default=0)
    stores_frames = Column(Float, default=0)
    bee_coverage_frames = Column(Float, default=0)
    temperament = Column(String, default='Unknown')
    notes = Column(Text, default='')
    colony = relationship('Colony', back_populates='inspections')

class GenealogyEvent(Base):
    __tablename__ = 'genealogy_events'
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    event_type = Column(String, default='Unknown')
    source_colony = Column(String, default='')
    target_colony = Column(String, default='')
    queen_code = Column(String, default='')
    details = Column(Text, default='')

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_code = Column(String, default='')
    details = Column(Text, default='')

class PendingCommit(Base):
    __tablename__ = 'pending_commits'
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    entity_type = Column(String, default='')
    entity_code = Column(String, default='')
    payload = Column(Text, default='')
    status = Column(String, default='Pending')
    validation_status = Column(String, default='Not run')
    validation_message = Column(Text, default='')

class WeatherObservation(Base):
    __tablename__ = 'weather_observations'
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    temperature_c = Column(Float, default=0)
    wind = Column(String, default='')
    rain = Column(String, default='')
    forage_flow = Column(String, default='Unknown')
    inspection_suitability = Column(String, default='Unknown')
    notes = Column(Text, default='')
