from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Numeric, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database.database import Base


class InspectionStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    REJECTED = "rejected"


class MaterialStatus(PyEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PENDING = "pending"
    QUARANTINE = "quarantine"


class RawMaterialInward(Base):
    __tablename__ = "raw_material_inwards"
    
    id = Column(Integer, primary_key=True, index=True)
    inward_number = Column(String, unique=True, index=True, nullable=False)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    material_description = Column(String, nullable=False)
    part_number = Column(String, nullable=True)
    drawing_number = Column(String, nullable=True)
    heat_number = Column(String, nullable=True)
    batch_number = Column(String, nullable=True)
    quantity_received = Column(Integer, nullable=False)
    quantity_accepted = Column(Integer, nullable=True)
    quantity_rejected = Column(Integer, nullable=True)
    inspection_status = Column(Enum(InspectionStatus), default=InspectionStatus.PENDING)
    material_status = Column(Enum(MaterialStatus), default=MaterialStatus.PENDING)
    inward_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    inspected_by = Column(Integer, nullable=True, default=1)
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    purchase_order = relationship("PurchaseOrder")
    supplier = relationship("Supplier")
    mtc_verifications = relationship("MTCVerification", back_populates="inward")


class MTCVerification(Base):
    __tablename__ = "mtc_verifications"
    
    id = Column(Integer, primary_key=True, index=True)
    inward_id = Column(Integer, ForeignKey("raw_material_inwards.id"), nullable=False)
    mtc_number = Column(String, nullable=False)
    mtc_date = Column(Date, nullable=False)
    chemical_composition_ok = Column(Boolean, default=False)
    mechanical_properties_ok = Column(Boolean, default=False)
    dimensions_ok = Column(Boolean, default=False)
    surface_finish_ok = Column(Boolean, default=False)
    other_tests_ok = Column(Boolean, default=False)
    verification_status = Column(String, default="pending")
    remarks = Column(Text, nullable=True)
    verified_by = Column(Integer, nullable=False, default=1)
    verification_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    inward = relationship("RawMaterialInward", back_populates="mtc_verifications")


class TraceabilityRecord(Base):
    __tablename__ = "traceability_records"
    
    id = Column(Integer, primary_key=True, index=True)
    record_number = Column(String, unique=True, index=True, nullable=False)
    part_number = Column(String, nullable=False)
    drawing_number = Column(String, nullable=False)
    heat_number = Column(String, nullable=False)
    batch_number = Column(String, nullable=False)
    customer_po = Column(String, nullable=True)
    customer_name = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    inward_date = Column(DateTime(timezone=True), nullable=False)
    process_start_date = Column(DateTime(timezone=True), nullable=True)
    completion_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)


class StockRegister(Base):
    __tablename__ = "stock_registers"
    
    id = Column(Integer, primary_key=True, index=True)
    material_code = Column(String, nullable=False)
    material_description = Column(String, nullable=False)
    heat_number = Column(String, nullable=True)
    batch_number = Column(String, nullable=True)
    location = Column(String, nullable=False)
    bin_location = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)
    minimum_stock = Column(Integer, nullable=True)
    maximum_stock = Column(Integer, nullable=True)
    reorder_level = Column(Integer, nullable=True)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_by = Column(Integer, nullable=True, default=1)


class ShelfLifeControl(Base):
    __tablename__ = "shelf_life_controls"
    
    id = Column(Integer, primary_key=True, index=True)
    material_code = Column(String, nullable=False)
    batch_number = Column(String, nullable=False)
    material_description = Column(String, nullable=False)
    manufacture_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, default="active")
    notification_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)


class IdentificationTag(Base):
    __tablename__ = "identification_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    tag_number = Column(String, unique=True, index=True, nullable=False)
    part_number = Column(String, nullable=False)
    drawing_number = Column(String, nullable=False)
    heat_number = Column(String, nullable=True)
    batch_number = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="active")
    issue_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, nullable=False, default=1)