from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database.database import Base


class DrawingStatus(PyEnum):
    DRAFT = "draft"
    APPROVED = "approved"
    OBSOLETE = "obsolete"
    UNDER_REVIEW = "under_review"


class Drawing(Base):
    __tablename__ = "drawings"
    
    id = Column(Integer, primary_key=True, index=True)
    drawing_number = Column(String, unique=True, index=True, nullable=False)
    revision = Column(String, nullable=False)
    title = Column(String, nullable=False)
    customer = Column(String, nullable=True)
    status = Column(Enum(DrawingStatus), default=DrawingStatus.DRAFT)
    issue_date = Column(DateTime(timezone=True), server_default=func.now())
    effective_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    route_cards = relationship("RouteCard", back_populates="drawing")


class RouteCard(Base):
    __tablename__ = "route_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    route_card_number = Column(String, unique=True, index=True, nullable=False)
    drawing_id = Column(Integer, ForeignKey("drawings.id"), nullable=False)
    part_number = Column(String, nullable=False)
    revision = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    drawing = relationship("Drawing", back_populates="route_cards")
    operations = relationship("ProcessOperation", back_populates="route_card")


class ProcessOperation(Base):
    __tablename__ = "process_operations"
    
    id = Column(Integer, primary_key=True, index=True)
    route_card_id = Column(Integer, ForeignKey("route_cards.id"), nullable=False)
    operation_number = Column(Integer, nullable=False)
    operation_description = Column(String, nullable=False)
    machine_required = Column(String, nullable=True)
    tooling_required = Column(String, nullable=True)
    setup_time = Column(Integer, default=0)  # in minutes
    run_time = Column(Integer, nullable=False)  # per piece in minutes
    inspection_required = Column(Boolean, default=True)
    special_process = Column(Boolean, default=False)
    process_type = Column(String, nullable=True)  # HT, Plating, NDT, Welding, etc.
    sequence = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    route_card = relationship("RouteCard", back_populates="operations")


class ControlPlan(Base):
    __tablename__ = "control_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_number = Column(String, unique=True, index=True, nullable=False)
    part_number = Column(String, nullable=False)
    drawing_revision = Column(String, nullable=False)
    revision_date = Column(DateTime(timezone=True), server_default=func.now())
    approval_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    characteristics = relationship("ControlCharacteristic", back_populates="control_plan")


class ControlCharacteristic(Base):
    __tablename__ = "control_characteristics"
    
    id = Column(Integer, primary_key=True, index=True)
    control_plan_id = Column(Integer, ForeignKey("control_plans.id"), nullable=False)
    characteristic_number = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    specification = Column(String, nullable=False)
    tolerance = Column(String, nullable=True)
    measurement_method = Column(String, nullable=True)
    sample_size = Column(Integer, nullable=False)
    sample_frequency = Column(String, nullable=True)
    control_method = Column(String, nullable=True)
    reaction_plan = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    control_plan = relationship("ControlPlan", back_populates="characteristics")


class Tooling(Base):
    __tablename__ = "tooling"
    
    id = Column(Integer, primary_key=True, index=True)
    tool_number = Column(String, unique=True, index=True, nullable=False)
    tool_description = Column(String, nullable=False)
    tool_type = Column(String, nullable=False)  # Die, Fixture, Gauge, etc.
    part_number = Column(String, nullable=True)
    drawing_number = Column(String, nullable=True)
    status = Column(String, default="active")
    location = Column(String, nullable=True)
    maintenance_due = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)