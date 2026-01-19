from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Numeric, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database.database import Base


class DispatchStatus(PyEnum):
    PENDING = "pending"
    READY = "ready"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class FinalChecklist(Base):
    __tablename__ = "final_checklists"
    
    id = Column(Integer, primary_key=True, index=True)
    checklist_number = Column(String, unique=True, index=True, nullable=False)
    job_card_id = Column(Integer, ForeignKey("job_cards.id"), nullable=False)
    part_number = Column(String, nullable=False)
    drawing_number = Column(String, nullable=False)
    customer_po = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    inspection_completed = Column(Boolean, default=False)
    fai_completed = Column(Boolean, default=False)
    coc_prepared = Column(Boolean, default=False)
    packing_completed = Column(Boolean, default=False)
    documents_verified = Column(Boolean, default=False)
    customer_requirements_met = Column(Boolean, default=False)
    special_instructions_followed = Column(Boolean, default=False)
    remarks = Column(Text, nullable=True)
    checked_by = Column(Integer, nullable=False)
    check_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="completed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    job_card = relationship("JobCard")

class CertificateOfConformance(Base):
    __tablename__ = "certificates_of_conformance"
    
    id = Column(Integer, primary_key=True, index=True)
    coc_number = Column(String, unique=True, index=True, nullable=False)
    job_card_id = Column(Integer, ForeignKey("job_cards.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    customer_po = Column(String, nullable=False)
    part_number = Column(String, nullable=False)
    drawing_number = Column(String, nullable=False)
    revision = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    inspection_report_number = Column(String, nullable=True)
    fai_report_number = Column(String, nullable=True)
    material_specification = Column(String, nullable=True)
    heat_number = Column(String, nullable=True)
    batch_number = Column(String, nullable=True)
    special_processes = Column(Text, nullable=True)
    conformance_statement = Column(Text, nullable=False)
    issued_date = Column(DateTime(timezone=True), server_default=func.now())
    authorized_by = Column(Integer, nullable=False)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    job_card = relationship("JobCard")


class PackingList(Base):
    __tablename__ = "packing_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    packing_number = Column(String, unique=True, index=True, nullable=False)
    job_card_id = Column(Integer, ForeignKey("job_cards.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    customer_po = Column(String, nullable=False)
    dispatch_date = Column(Date, nullable=False)
    package_number = Column(Integer, nullable=False)
    part_number = Column(String, nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    net_weight = Column(Numeric(10, 3), nullable=True)
    gross_weight = Column(Numeric(10, 3), nullable=True)
    dimensions = Column(String, nullable=True)
    packing_type = Column(String, nullable=True)
    special_instructions = Column(Text, nullable=True)
    prepared_by = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    job_card = relationship("JobCard")


class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True, nullable=False)
    job_card_id = Column(Integer, ForeignKey("job_cards.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    customer_po = Column(String, nullable=False)
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    part_number = Column(String, nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    tax_amount = Column(Numeric(12, 2), nullable=True)
    net_amount = Column(Numeric(12, 2), nullable=False)
    payment_terms = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    job_card = relationship("JobCard")


class DeliveryChallan(Base):
    __tablename__ = "delivery_challans"
    
    id = Column(Integer, primary_key=True, index=True)
    challan_number = Column(String, unique=True, index=True, nullable=False)
    job_card_id = Column(Integer, ForeignKey("job_cards.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    customer_po = Column(String, nullable=False)
    dispatch_date = Column(Date, nullable=False)
    vehicle_number = Column(String, nullable=True)
    driver_name = Column(String, nullable=True)
    driver_contact = Column(String, nullable=True)
    lr_number = Column(String, nullable=True)
    transport_name = Column(String, nullable=True)
    destination = Column(String, nullable=False)
    part_number = Column(String, nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    net_weight = Column(Numeric(10, 3), nullable=True)
    gross_weight = Column(Numeric(10, 3), nullable=True)
    delivery_status = Column(Enum(DispatchStatus), default=DispatchStatus.PENDING)
    delivery_date = Column(Date, nullable=True)
    received_by = Column(String, nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    job_card = relationship("JobCard")


class DispatchRecord(Base):
    __tablename__ = "dispatch_records"
    
    id = Column(Integer, primary_key=True, index=True)
    dispatch_number = Column(String, unique=True, index=True, nullable=False)
    job_card_id = Column(Integer, ForeignKey("job_cards.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    customer_po = Column(String, nullable=False)
    dispatch_date = Column(DateTime(timezone=True), server_default=func.now())
    final_checklist_id = Column(Integer, ForeignKey("final_checklists.id"), nullable=True)
    coc_id = Column(Integer, ForeignKey("certificates_of_conformance.id"), nullable=True)
    packing_list_id = Column(Integer, ForeignKey("packing_lists.id"), nullable=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    delivery_challan_id = Column(Integer, ForeignKey("delivery_challans.id"), nullable=True)
    status = Column(Enum(DispatchStatus), default=DispatchStatus.PENDING)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    job_card = relationship("JobCard")
    final_checklist = relationship("FinalChecklist")
    coc = relationship("CertificateOfConformance")
    packing_list = relationship("PackingList")
    invoice = relationship("Invoice")
    delivery_challan = relationship("DeliveryChallan")