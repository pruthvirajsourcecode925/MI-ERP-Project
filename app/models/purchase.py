from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Numeric, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database.database import Base


class SupplierStatus(PyEnum):
    APPROVED = "approved"
    PENDING = "pending"
    SUSPENDED = "suspended"
    REJECTED = "rejected"


class EvaluationStatus(PyEnum):
    NEW = "new"
    EVALUATION_PENDING = "evaluation_pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    RE_EVALUATION_DUE = "re_evaluation_due"


class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    supplier_code = Column(String, unique=True, index=True, nullable=False)
    supplier_name = Column(String, nullable=False)
    address = Column(Text, nullable=True)
    contact_person = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    website = Column(String, nullable=True)
    gst_number = Column(String, nullable=True)
    pan_number = Column(String, nullable=True)
    payment_terms = Column(String, nullable=True)
    status = Column(Enum(SupplierStatus), default=SupplierStatus.PENDING)
    approved_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    evaluations = relationship("SupplierEvaluation", back_populates="supplier")
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")
    subcontracting_orders = relationship("SubcontractingOrder", back_populates="supplier")
    supplier_ncrs = relationship("SupplierNCR", back_populates="supplier")


class SupplierEvaluation(Base):
    __tablename__ = "supplier_evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    evaluation_number = Column(String, unique=True, index=True, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    evaluation_date = Column(DateTime(timezone=True), server_default=func.now())
    evaluation_type = Column(String, nullable=False)  # Initial, Re-evaluation
    quality_score = Column(Integer, nullable=False)  # 1-100
    delivery_score = Column(Integer, nullable=False)  # 1-100
    price_score = Column(Integer, nullable=False)  # 1-100
    service_score = Column(Integer, nullable=False)  # 1-100
    overall_score = Column(Integer, nullable=False)  # 1-100
    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    next_evaluation_date = Column(Date, nullable=True)
    status = Column(Enum(EvaluationStatus), default=EvaluationStatus.NEW)
    approved_by = Column(Integer, nullable=True, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    evaluated_by = Column(Integer, nullable=False)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="evaluations")


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String, unique=True, index=True, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    order_date = Column(Date, nullable=False)
    delivery_date = Column(Date, nullable=False)
    total_value = Column(Numeric(12, 2), nullable=False)
    status = Column(String, default="pending")
    terms_and_conditions = Column(Text, nullable=True)
    quality_clauses = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="purchase_order")
    supplier_ncrs = relationship("SupplierNCR", back_populates="purchase_order")


class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    item_number = Column(Integer, nullable=False)
    material_description = Column(String, nullable=False)
    part_number = Column(String, nullable=True)
    drawing_number = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    delivery_date = Column(Date, nullable=True)
    specifications = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    purchase_order = relationship("PurchaseOrder", back_populates="items")


class SubcontractingOrder(Base):
    __tablename__ = "subcontracting_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    process_type = Column(String, nullable=False)  # HT, Plating, NDT, etc.
    part_number = Column(String, nullable=False)
    drawing_number = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    special_instructions = Column(Text, nullable=True)
    order_date = Column(Date, nullable=False)
    delivery_date = Column(Date, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="subcontracting_orders")


class SupplierNCR(Base):
    __tablename__ = "supplier_ncrs"
    
    id = Column(Integer, primary_key=True, index=True)
    ncr_number = Column(String, unique=True, index=True, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=True)
    material_description = Column(String, nullable=False)
    quantity_rejected = Column(Integer, nullable=False)
    rejection_reason = Column(Text, nullable=False)
    rejection_date = Column(DateTime(timezone=True), server_default=func.now())
    action_required = Column(Text, nullable=True)
    status = Column(String, default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="supplier_ncrs")
    purchase_order = relationship("PurchaseOrder", back_populates="supplier_ncrs")