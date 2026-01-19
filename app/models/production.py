from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Numeric, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database.database import Base


class JobStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


class OperationStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REWORK = "rework"


class JobCard(Base):
    __tablename__ = "job_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    job_card_number = Column(String, unique=True, index=True, nullable=False)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=True)
    customer_po = Column(String, nullable=True)
    part_number = Column(String, nullable=False)
    drawing_number = Column(String, nullable=False)
    revision = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    route_card_id = Column(Integer, ForeignKey("route_cards.id"), nullable=True)
    planned_start_date = Column(Date, nullable=False)
    planned_completion_date = Column(Date, nullable=False)
    actual_start_date = Column(DateTime(timezone=True), nullable=True)
    actual_completion_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    priority = Column(String, default="normal")
    special_instructions = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    purchase_order = relationship("PurchaseOrder")
    route_card = relationship("RouteCard")
    operations = relationship("JobCardOperation", back_populates="job_card")


class JobCardOperation(Base):
    __tablename__ = "job_card_operations"
    
    id = Column(Integer, primary_key=True, index=True)
    job_card_id = Column(Integer, ForeignKey("job_cards.id"), nullable=False)
    operation_number = Column(Integer, nullable=False)
    operation_description = Column(String, nullable=False)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=True)
    operator_id = Column(Integer, nullable=True)
    planned_time = Column(Integer, nullable=False)  # minutes
    actual_time = Column(Integer, nullable=True)  # minutes
    quantity_planned = Column(Integer, nullable=False)
    quantity_produced = Column(Integer, nullable=True)
    quantity_rejected = Column(Integer, nullable=True)
    status = Column(Enum(OperationStatus), default=OperationStatus.PENDING)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    job_card = relationship("JobCard", back_populates="operations")
    machine = relationship("Machine")


class Machine(Base):
    __tablename__ = "machines"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_code = Column(String, unique=True, index=True, nullable=False)
    machine_name = Column(String, nullable=False)
    machine_type = Column(String, nullable=False)
    manufacturer = Column(String, nullable=True)
    model = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    capacity = Column(String, nullable=True)
    location = Column(String, nullable=False)
    status = Column(String, default="active")
    installation_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    operations = relationship("JobCardOperation", back_populates="machine")


class ProductionLog(Base):
    __tablename__ = "production_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    log_date = Column(Date, nullable=False)
    shift = Column(String, nullable=False)  # Morning, Evening, Night
    job_card_id = Column(Integer, ForeignKey("job_cards.id"), nullable=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=True)
    operator_id = Column(Integer, nullable=True)
    production_hours = Column(Integer, nullable=False)  # in minutes
    downtime_hours = Column(Integer, nullable=False)  # in minutes
    quantity_produced = Column(Integer, nullable=False)
    quantity_rejected = Column(Integer, nullable=False)
    efficiency = Column(Numeric(5, 2), nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    job_card = relationship("JobCard")
    machine = relationship("Machine")


class FAITrigger(Base):
    __tablename__ = "fai_triggers"
    
    id = Column(Integer, primary_key=True, index=True)
    trigger_number = Column(String, unique=True, index=True, nullable=False)
    job_card_id = Column(Integer, ForeignKey("job_cards.id"), nullable=False)
    trigger_reason = Column(String, nullable=False)
    trigger_date = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(Text, nullable=False)
    status = Column(String, default="pending")
    fai_report_id = Column(Integer, ForeignKey("fai_reports.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    job_card = relationship("JobCard")
    fai_report = relationship("FAIReport", foreign_keys=[fai_report_id])


class ReworkRecord(Base):
    __tablename__ = "rework_records"
    
    id = Column(Integer, primary_key=True, index=True)
    rework_number = Column(String, unique=True, index=True, nullable=False)
    job_card_id = Column(Integer, ForeignKey("job_cards.id"), nullable=False)
    operation_id = Column(Integer, ForeignKey("job_card_operations.id"), nullable=False)
    rework_reason = Column(Text, nullable=False)
    quantity_reworked = Column(Integer, nullable=False)
    rework_time = Column(Integer, nullable=False)  # minutes
    rework_cost = Column(Numeric(12, 2), nullable=True)
    completion_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    job_card = relationship("JobCard")
    operation = relationship("JobCardOperation")