# __all__ = ['PostBase', 'user', 'patient', 'doctor', 'visit', 'episode',
#            'assistant', 'relation', 'prescription', 'active_compound', 'compound_set', 'comercial_drug']

from sqlalchemy.schema import Identity
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Date, DateTime, String, Integer, Float, ForeignKey, Text
from davidoc.core.db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, Identity(), primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    email = Column(String(50), unique=True)
    hashed_password = Column(String)

    doctor = relationship('Doctor', back_populates='user')
    patient = relationship('Patient', back_populates='user')
    assistant = relationship('Assistant', back_populates='user')


class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer, Identity(), primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    fullname = Column(String(100))
    birthdate = Column(Date)
    gender = Column(String(2))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)

    user = relationship('User', back_populates='patient')
    doctors = relationship('Relation',  back_populates='patient')
    episodes = relationship('Episode', back_populates='patient')


class Doctor(Base):
    __tablename__ = 'doctor'
    id = Column(Integer, Identity(), primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    fullname = Column(String(100))
    birthdate = Column(Date)
    gender = Column(String(2))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=True)

    user = relationship('User', back_populates='doctor')
    patients = relationship('Relation', back_populates='doctor')



class Assistant(Base):
    __tablename__ = 'assistant'
    id = Column(Integer, Identity(), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=True)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    fullname = Column(String(100))
    birthdate = Column(Date)
    gender = Column(String(2))

    user = relationship('User', back_populates='assistant')


class Relation(Base):
    __tablename__ = 'relation'
    id = Column(Integer, Identity(), primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    patient_id = Column(Integer, ForeignKey('patient.id'))
    doctor_id = Column(Integer, ForeignKey('doctor.id'))

    patient = relationship('Patient', back_populates='doctors')
    doctor = relationship('Doctor', back_populates='patients')
    visits = relationship('Visit', back_populates='relation')



class Visit(Base):
    __tablename__ = 'visit'
    id = Column(Integer, Identity(), primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    relation_id = Column(Integer, ForeignKey('relation.id'))
    start = Column(DateTime)
    notes = Column(Text, nullable=True)

    relation = relationship('Relation', back_populates='visits')




class Episode(Base):
    __tablename__ = 'episode'
    id = Column(Integer, Identity(), primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    title = Column(String)

    start = Column(Date, nullable=True)
    final = Column(Date, nullable=True)
    relevance = Column(Integer, nullable=True)
    symptoms = Column(String, nullable=True)
    context = Column(String, nullable=True)
    notes = Column(Text, nullable=True)


    patient_id = Column(Integer, ForeignKey('patient.id'))
    patient = relationship('Patient', back_populates='episodes')


class ActiveCompound(Base):
    __tablename__ = 'active_compound'
    id = Column(Integer, Identity(), primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)

    compound_sets = relationship('CompoundSet', back_populates='active_compound')



class ComercialDrug(Base):
    __tablename__ = 'comercial_drug'
    id = Column(Integer, Identity(), primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    title = Column(String, nullable=False)
    compound_sets = relationship('CompoundSet', back_populates='comercial_drug')
    prescriptions = relationship('Prescription', back_populates='comercial_drug')



class CompoundSet(Base):
    __tablename__ = 'compound_set'
    id = Column(Integer, Identity(), primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    comercial_drug_id = Column(Integer, ForeignKey('comercial_drug.id'))
    active_compound_id = Column(Integer, ForeignKey('active_compound.id'))
    value = Column(Float)
    measure_unit = Column(String)
    active_compound = relationship('ActiveCompound', back_populates='compound_sets')
    comercial_drug = relationship('ComercialDrug', back_populates='compound_sets')

class Prescription(Base):
    __tablename__ = 'prescription'
    id = Column(Integer, Identity(), primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    comercial_drug_id = Column(Integer, ForeignKey('comercial_drug.id'))
    comercial_drug = relationship('ComercialDrug', back_populates='prescriptions')



PostBase = Base


user = User.__table__
patient = Patient.__table__
doctor = Doctor.__table__
prescription = Prescription.__table__
compound_set = CompoundSet.__table__
comercial_drug = ComercialDrug.__table__
active_compound = ActiveCompound.__table__
relation = Relation.__table__
episode = Episode.__table__
visit = Visit.__table__
assistant = Assistant.__table__