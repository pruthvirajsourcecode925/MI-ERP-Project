from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Date, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database.database import Base


class MaintenanceType(PyEnum):
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    PREDICTIVE = "predictive"
    EMERGENCY = "emergency"


class MaintenanceStatus(PyEnum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"


class Equipment(Base):
    __tablename__ = "equipment"
    
    id = Column(Integer, primary_key=True, index=True)
    equipment_code = Column(String, unique=True, index=True, nullable=False)
    equipment_name = Column(String, nullable=False)
    equipment_type = Column(String, nullable=False)
    manufacturer = Column(String, nullable=True)
    model = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    location = Column(String, nullable=False)
    installation_date = Column(Date, nullable=True)
    warranty_expiry = Column(Date, nullable=True)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    maintenance_records = relationship("MaintenanceRecord", back_populates="equipment")
    maintenance_plans = relationship("MaintenancePlan", back_populates="equipment")


class MaintenancePlan(Base):
    __tablename__ = "maintenance_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_number = Column(String, unique=True, index=True, nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    plan_name = Column(String, nullable=False)
    maintenance_type = Column(Enum(MaintenanceType), nullable=False)
    frequency = Column(String, nullable=False)  # Daily, Weekly, Monthly, etc.
    frequency_value = Column(Integer, nullable=True)  # Number of days/hours
    activities = Column(Text, nullable=False)
    spare_parts_required = Column(Text, nullable=True)
    estimated_time = Column(Integer, nullable=True)  # in hours
    skill_required = Column(String, nullable=True)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    equipment = relationship("Equipment", back_populates="maintenance_plans")
    schedules = relationship("MaintenanceSchedule", back_populates="maintenance_plan")


class MaintenanceSchedule(Base):
    __tablename__ = "maintenance_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    schedule_number = Column(String, unique=True, index=True, nullable=False)
    plan_id = Column(Integer, ForeignKey("maintenance_plans.id"), nullable=False)
    scheduled_date = Column(DateTime(timezone=True), nullable=False)
    estimated_duration = Column(Integer, nullable=False)  # in hours
    assigned_to = Column(Integer, nullable=True)
    priority = Column(String, default="normal")
    status = Column(String, default="scheduled")
    completion_date = Column(DateTime(timezone=True), nullable=True)
    actual_duration = Column(Integer, nullable=True)  # in hours
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    maintenance_plan = relationship("MaintenancePlan", back_populates="schedules")


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    record_number = Column(String, unique=True, index=True, nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("maintenance_schedules.id"), nullable=True)
    maintenance_type = Column(Enum(MaintenanceType), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    duration = Column(Integer, nullable=True)  # in hours
    performed_by = Column(Integer, nullable=False)
    activities_performed = Column(Text, nullable=False)
    parts_used = Column(Text, nullable=True)
    cost = Column(Numeric(12, 2), nullable=True)
    next_maintenance_date = Column(DateTime(timezone=True), nullable=True)
    remarks = Column(Text, nullable=True)
    status = Column(Enum(MaintenanceStatus), default=MaintenanceStatus.IN_PROGRESS)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    equipment = relationship("Equipment", back_populates="maintenance_records")
    schedule = relationship("MaintenanceSchedule")


class BreakdownRecord(Base):
    __tablename__ = "breakdown_records"
    
    id = Column(Integer, primary_key=True, index=True)
    breakdown_number = Column(String, unique=True, index=True, nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    breakdown_date = Column(DateTime(timezone=True), server_default=func.now())
    breakdown_time = Column(DateTime(timezone=True), server_default=func.now())
    reported_by = Column(Integer, nullable=False)
    symptoms = Column(Text, nullable=False)
    probable_cause = Column(Text, nullable=True)
    downtime_hours = Column(Numeric(8, 2), nullable=True)
    production_loss = Column(Numeric(12, 2), nullable=True)
    repair_cost = Column(Numeric(12, 2), nullable=True)
    resolution_date = Column(DateTime(timezone=True), nullable=True)
    resolution_description = Column(Text, nullable=True)
    preventive_measures = Column(Text, nullable=True)
    status = Column(String, default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    equipment = relationship("Equipment")


class SparePart(Base):
    __tablename__ = "spare_parts"
    
    id = Column(Integer, primary_key=True, index=True)
    part_code = Column(String, unique=True, index=True, nullable=False)
    part_description = Column(String, nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=True)
    manufacturer = Column(String, nullable=True)
    part_number = Column(String, nullable=True)
    specifications = Column(Text, nullable=True)
    current_stock = Column(Integer, default=0)
    minimum_stock = Column(Integer, nullable=True)
    maximum_stock = Column(Integer, nullable=True)
    unit_cost = Column(Numeric(12, 2), nullable=True)
    location = Column(String, nullable=False)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    equipment = relationship("Equipment")