from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Numeric, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database.database import Base


class InspectionType(PyEnum):
    INCOMING = "incoming"
    IN_PROCESS = "in_process"
    FINAL = "final"
    SOURCE = "source"


class NCRStatus(PyEnum):
    OPEN = "open"
    UNDER_INVESTIGATION = "under_investigation"
    CORRECTIVE_ACTION = "corrective_action"
    CLOSED = "closed"
    VERIFIED = "verified"


class CAPAStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"
    CLOSED = "closed"


class InspectionReport(Base):
    __tablename__ = "inspection_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_number = Column(String, unique=True, index=True, nullable=False)
    inspection_type = Column(Enum(InspectionType), nullable=False)
    job_card_id = Column(Integer, ForeignKey("job_cards.id"), nullable=True)
    inward_id = Column(Integer, ForeignKey("raw_material_inwards.id"), nullable=True)
    part_number = Column(String, nullable=False)
    drawing_number = Column(String, nullable=False)
    quantity_inspected = Column(Integer, nullable=False)
    quantity_accepted = Column(Integer, nullable=False)
    quantity_rejected = Column(Integer, nullable=False)
    inspection_date = Column(DateTime(timezone=True), server_default=func.now())
    inspector_id = Column(Integer, nullable=False, default=1)
    remarks = Column(Text, nullable=True)
    status = Column(String, default="completed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    job_card = relationship("JobCard")
    inward = relationship("RawMaterialInward")
    characteristics = relationship("InspectionCharacteristic", back_populates="inspection_report")


class InspectionCharacteristic(Base):
    __tablename__ = "inspection_characteristics"
    
    id = Column(Integer, primary_key=True, index=True)
    inspection_report_id = Column(Integer, ForeignKey("inspection_reports.id"), nullable=False)
    characteristic_number = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    specification = Column(String, nullable=False)
    tolerance = Column(String, nullable=True)
    measured_value = Column(String, nullable=True)
    result = Column(String, nullable=False)  # OK, NOT OK
    gauge_used = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    inspection_report = relationship("InspectionReport", back_populates="characteristics")


class FAIReport(Base):
    __tablename__ = "fai_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    fai_number = Column(String, unique=True, index=True, nullable=False)
    part_number = Column(String, nullable=False)
    drawing_number = Column(String, nullable=False)
    revision = Column(String, nullable=False)
    customer = Column(String, nullable=True)
    fai_date = Column(DateTime(timezone=True), server_default=func.now())
    quantity_produced = Column(Integer, nullable=False)
    serial_numbers = Column(Text, nullable=True)
    design_verification = Column(Boolean, default=False)
    process_validation = Column(Boolean, default=False)
    production_capability = Column(Boolean, default=False)
    gage_r_and_r = Column(Boolean, default=False)
    material_verification = Column(Boolean, default=False)
    performance_testing = Column(Boolean, default=False)
    overall_result = Column(String, default="pending")
    approved_by = Column(Integer, nullable=True, default=1)
    approval_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    dimensions = relationship("FAIDimension", back_populates="fai_report")


class FAIDimension(Base):
    __tablename__ = "fai_dimensions"
    
    id = Column(Integer, primary_key=True, index=True)
    fai_report_id = Column(Integer, ForeignKey("fai_reports.id"), nullable=False)
    dimension_number = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    specification = Column(String, nullable=False)
    tolerance = Column(String, nullable=True)
    measurement_1 = Column(Numeric(10, 4), nullable=True)
    measurement_2 = Column(Numeric(10, 4), nullable=True)
    measurement_3 = Column(Numeric(10, 4), nullable=True)
    average = Column(Numeric(10, 4), nullable=True)
    result = Column(String, nullable=False)
    gauge_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    fai_report = relationship("FAIReport", back_populates="dimensions")


class NonConformanceReport(Base):
    __tablename__ = "non_conformance_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    ncr_number = Column(String, unique=True, index=True, nullable=False)
    job_card_id = Column(Integer, ForeignKey("job_cards.id"), nullable=True)
    inward_id = Column(Integer, ForeignKey("raw_material_inwards.id"), nullable=True)
    part_number = Column(String, nullable=False)
    drawing_number = Column(String, nullable=False)
    quantity_affected = Column(Integer, nullable=False)
    defect_description = Column(Text, nullable=False)
    defect_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)  # Major, Minor, Critical
    occurrence_date = Column(DateTime(timezone=True), server_default=func.now())
    detection_stage = Column(String, nullable=False)  # Incoming, In-process, Final, Customer
    immediate_action = Column(Text, nullable=True)
    status = Column(Enum(NCRStatus), default=NCRStatus.OPEN)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    job_card = relationship("JobCard")
    inward = relationship("RawMaterialInward")
    capa_reports = relationship("CAPAReport", back_populates="ncr")


class CAPAReport(Base):
    __tablename__ = "capa_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    capa_number = Column(String, unique=True, index=True, nullable=False)
    ncr_id = Column(Integer, ForeignKey("non_conformance_reports.id"), nullable=True)
    source = Column(String, nullable=False)  # NCR, Audit, Customer Complaint, etc.
    problem_description = Column(Text, nullable=False)
    root_cause_analysis = Column(Text, nullable=True)
    analysis_method = Column(String, nullable=True)  # 5 Why, Fishbone, etc.
    correction_action = Column(Text, nullable=True)
    corrective_action = Column(Text, nullable=True)
    preventive_action = Column(Text, nullable=True)
    responsible_person = Column(Integer, nullable=False, default=1)
    target_date = Column(Date, nullable=False)
    completion_date = Column(Date, nullable=True)
    effectiveness_verification = Column(Text, nullable=True)
    status = Column(Enum(CAPAStatus), default=CAPAStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    ncr = relationship("NonConformanceReport", back_populates="capa_reports")


class GaugeCalibration(Base):
    __tablename__ = "gauge_calibrations"
    
    id = Column(Integer, primary_key=True, index=True)
    gauge_id = Column(String, unique=True, index=True, nullable=False)
    gauge_description = Column(String, nullable=False)
    gauge_type = Column(String, nullable=False)
    range = Column(String, nullable=True)
    accuracy = Column(String, nullable=True)
    location = Column(String, nullable=False)
    last_calibration_date = Column(Date, nullable=False)
    next_calibration_date = Column(Date, nullable=False)
    calibration_agency = Column(String, nullable=True)
    calibration_certificate = Column(String, nullable=True)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)


class InternalAudit(Base):
    __tablename__ = "internal_audits"
    
    id = Column(Integer, primary_key=True, index=True)
    audit_number = Column(String, unique=True, index=True, nullable=False)
    audit_date = Column(Date, nullable=False)
    audit_type = Column(String, nullable=False)  # Process, Product, System
    scope = Column(Text, nullable=False)
    audit_team = Column(Text, nullable=True)
    findings = Column(Text, nullable=True)
    non_conformities = Column(Text, nullable=True)
    observations = Column(Text, nullable=True)
    conclusion = Column(Text, nullable=True)
    lead_auditor = Column(Integer, nullable=False, default=1)
    status = Column(String, default="planned")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())