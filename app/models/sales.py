from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Numeric, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database.database import Base


class EnquiryStatus(PyEnum):
    NEW = "new"
    UNDER_REVIEW = "under_review"
    QUOTED = "quoted"
    CONVERTED = "converted"
    CLOSED = "closed"


class CustomerEnquiry(Base):
    __tablename__ = "customer_enquiries"
    
    id = Column(Integer, primary_key=True, index=True)
    enquiry_number = Column(String, unique=True, index=True, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=True)
    customer_phone = Column(String, nullable=True)
    customer_address = Column(String, nullable=True)
    part_number = Column(String, nullable=False)
    drawing_number = Column(String, nullable=False)
    revision = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    target_price = Column(Numeric(12, 2), nullable=True)
    delivery_date = Column(Date, nullable=True)
    special_requirements = Column(Text, nullable=True)
    drawing_available = Column(Boolean, default=False)
    special_processes = Column(Text, nullable=True)
    capacity_feasible = Column(Boolean, default=True)
    delivery_feasible = Column(Boolean, default=True)
    quality_requirements = Column(Text, nullable=True)
    status = Column(Enum(EnquiryStatus), default=EnquiryStatus.NEW)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    quotations = relationship("Quotation", back_populates="enquiry")
    contract_reviews = relationship("ContractReview", back_populates="enquiry")


class Quotation(Base):
    __tablename__ = "quotations"
    
    id = Column(Integer, primary_key=True, index=True)
    quotation_number = Column(String, unique=True, index=True, nullable=False)
    enquiry_id = Column(Integer, ForeignKey("customer_enquiries.id"), nullable=False)
    quoted_price = Column(Numeric(12, 2), nullable=False)
    quoted_delivery = Column(Date, nullable=False)
    terms_and_conditions = Column(Text, nullable=True)
    validity_date = Column(Date, nullable=False)
    status = Column(String, default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    enquiry = relationship("CustomerEnquiry", back_populates="quotations")


class ContractReview(Base):
    __tablename__ = "contract_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    review_number = Column(String, unique=True, index=True, nullable=False)
    enquiry_id = Column(Integer, ForeignKey("customer_enquiries.id"), nullable=False)
    review_date = Column(DateTime(timezone=True), server_default=func.now())
    drawing_availability = Column(Boolean, nullable=False)
    special_processes_review = Column(Text, nullable=True)
    capacity_suitability = Column(Boolean, nullable=False)
    delivery_feasibility = Column(Boolean, nullable=False)
    quality_requirements_review = Column(Text, nullable=True)
    risk_assessment = Column(Text, nullable=True)
    approved = Column(Boolean, default=False)
    approval_comments = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    enquiry = relationship("CustomerEnquiry", back_populates="contract_reviews")


class CustomerPurchaseOrder(Base):
    __tablename__ = "customer_purchase_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String, unique=True, index=True, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_po_number = Column(String, nullable=False)
    enquiry_id = Column(Integer, ForeignKey("customer_enquiries.id"), nullable=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=True)
    order_date = Column(Date, nullable=False)
    delivery_date = Column(Date, nullable=False)
    total_value = Column(Numeric(12, 2), nullable=False)
    status = Column(String, default="active")
    terms_and_conditions = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    enquiry = relationship("CustomerEnquiry")
    quotation = relationship("Quotation")
