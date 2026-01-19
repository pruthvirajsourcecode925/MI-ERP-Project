from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database.database import Base


class DocumentStatus(PyEnum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    OBSOLETE = "obsolete"


class DocumentType(PyEnum):
    SOP = "sop"
    WORK_INSTRUCTION = "work_instruction"
    FORM = "form"
    SPECIFICATION = "specification"
    DRAWING = "drawing"
    MANUAL = "manual"
    POLICY = "policy"
    PROCEDURE = "procedure"


class MasterDocumentList(Base):
    __tablename__ = "master_document_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    document_number = Column(String, unique=True, index=True, nullable=False)
    document_title = Column(String, nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    department = Column(String, nullable=False)
    revision = Column(String, nullable=False)
    revision_date = Column(DateTime(timezone=True), server_default=func.now())
    effective_date = Column(DateTime(timezone=True), nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.DRAFT)
    approved_by = Column(Integer, nullable=True, default=1)
    approval_date = Column(DateTime(timezone=True), nullable=True)
    retention_period = Column(Integer, nullable=True)  # in years
    location = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    revisions = relationship("DocumentRevision", back_populates="master_document")


class DocumentRevision(Base):
    __tablename__ = "document_revisions"
    
    id = Column(Integer, primary_key=True, index=True)
    master_document_id = Column(Integer, ForeignKey("master_document_lists.id"), nullable=False)
    revision_number = Column(String, nullable=False)
    revision_date = Column(DateTime(timezone=True), server_default=func.now())
    change_description = Column(Text, nullable=False)
    reason_for_change = Column(Text, nullable=True)
    changed_by = Column(Integer, nullable=False)
    approved_by = Column(Integer, nullable=True, default=1)
    approval_date = Column(DateTime(timezone=True), nullable=True)
    file_path = Column(String, nullable=True)
    status = Column(String, default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    master_document = relationship("MasterDocumentList", back_populates="revisions")


class DocumentChangeRequest(Base):
    __tablename__ = "document_change_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    dcr_number = Column(String, unique=True, index=True, nullable=False)
    document_id = Column(Integer, ForeignKey("master_document_lists.id"), nullable=False)
    current_revision = Column(String, nullable=False)
    proposed_revision = Column(String, nullable=False)
    change_description = Column(Text, nullable=False)
    reason_for_change = Column(Text, nullable=False)
    urgency = Column(String, default="normal")
    requested_by = Column(Integer, nullable=False)
    request_date = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_by = Column(Integer, nullable=True)
    review_date = Column(DateTime(timezone=True), nullable=True)
    review_comments = Column(Text, nullable=True)
    approved_by = Column(Integer, nullable=True, default=1)
    approval_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    document = relationship("MasterDocumentList")


class RecordRetentionMatrix(Base):
    __tablename__ = "record_retention_matrices"
    
    id = Column(Integer, primary_key=True, index=True)
    record_type = Column(String, nullable=False)
    record_description = Column(String, nullable=False)
    department = Column(String, nullable=False)
    retention_period = Column(Integer, nullable=False)  # in years
    retention_start = Column(String, nullable=False)  # From creation date, completion date, etc.
    disposal_method = Column(String, nullable=True)
    responsible_person = Column(Integer, nullable=False, default=1)
    last_review_date = Column(Date, nullable=True)
    next_review_date = Column(Date, nullable=True)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)


class ObsoleteDocumentControl(Base):
    __tablename__ = "obsolete_document_controls"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("master_document_lists.id"), nullable=False)
    obsolete_revision = Column(String, nullable=False)
    obsolete_date = Column(DateTime(timezone=True), server_default=func.now())
    obsolete_reason = Column(Text, nullable=False)
    replacement_document = Column(String, nullable=True)
    replacement_revision = Column(String, nullable=True)
    disposal_date = Column(DateTime(timezone=True), nullable=True)
    disposal_method = Column(String, nullable=True)
    disposed_by = Column(Integer, nullable=True)
    status = Column(String, default="obsolete")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)
    
    # Relationships
    document = relationship("MasterDocumentList")


class DocumentAccessLog(Base):
    __tablename__ = "document_access_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("master_document_lists.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    access_type = Column(String, nullable=False)  # View, Download, Print, Edit
    access_date = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    document = relationship("MasterDocumentList")


class ControlledDocument(Base):
    __tablename__ = "controlled_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    document_number = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    current_revision = Column(String, nullable=False)
    effective_date = Column(DateTime(timezone=True), nullable=False)
    next_review_date = Column(DateTime(timezone=True), nullable=True)
    distribution_list = Column(Text, nullable=True)
    access_level = Column(String, nullable=False)  # Public, Restricted, Confidential
    approval_required = Column(Boolean, default=True)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.DRAFT)
    file_path = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    checksum = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, nullable=False, default=1)