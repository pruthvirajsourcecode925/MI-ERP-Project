from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Numeric, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base
from enum import Enum as PyEnum


class ComplianceStatus(PyEnum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PENDING = "pending"
    EXEMPT = "exempt"


class RiskLevel(PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AuditType(PyEnum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    SURVEILLANCE = "surveillance"
    CERTIFICATION = "certification"


class ComplianceClause(Base):
    __tablename__ = "compliance_clauses"
    
    id = Column(Integer, primary_key=True, index=True)
    clause_number = Column(String(20), unique=True, nullable=False)
    clause_title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    requirement = Column(Text, nullable=False)
    evidence_required = Column(Text, nullable=True)
    risk_level = Column(Enum(RiskLevel), nullable=False)
    status = Column(Enum(ComplianceStatus), default=ComplianceStatus.PENDING)
    last_reviewed = Column(DateTime(timezone=True), nullable=True)
    next_review = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ComplianceCheck(Base):
    __tablename__ = "compliance_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    clause_id = Column(Integer, ForeignKey("compliance_clauses.id"), nullable=False)
    check_number = Column(String(50), nullable=False)
    check_description = Column(Text, nullable=False)
    check_type = Column(String(50), nullable=False)  # Document, Process, Record, etc.
    frequency = Column(String(50), nullable=False)  # Daily, Weekly, Monthly, etc.
    responsible_person = Column(Integer, nullable=False, default=1)
    status = Column(Enum(ComplianceStatus), default=ComplianceStatus.PENDING)
    last_checked = Column(DateTime(timezone=True), nullable=True)
    next_check = Column(DateTime(timezone=True), nullable=True)
    evidence_location = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    clause = relationship("ComplianceClause")


class ComplianceAudit(Base):
    __tablename__ = "compliance_audits"
    
    id = Column(Integer, primary_key=True, index=True)
    audit_number = Column(String(50), unique=True, nullable=False)
    audit_type = Column(Enum(AuditType), nullable=False)
    audit_title = Column(String(200), nullable=False)
    audit_date = Column(DateTime(timezone=True), nullable=False)
    auditor_id = Column(Integer, nullable=False)
    auditee_id = Column(Integer, nullable=False)
    scope = Column(Text, nullable=False)
    criteria = Column(Text, nullable=False)
    findings = Column(Text, nullable=True)
    non_conformities = Column(Text, nullable=True)
    observations = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    overall_rating = Column(String(50), nullable=True)
    status = Column(String(50), default="planned")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships


class CorrectiveAction(Base):
    __tablename__ = "corrective_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    action_number = Column(String(50), unique=True, nullable=False)
    audit_id = Column(Integer, ForeignKey("compliance_audits.id"), nullable=True)
    source_type = Column(String(50), nullable=False)  # Audit, NCR, Customer Complaint, etc.
    source_id = Column(Integer, nullable=True)
    description = Column(Text, nullable=False)
    root_cause = Column(Text, nullable=True)
    correction = Column(Text, nullable=True)
    corrective_action = Column(Text, nullable=False)
    preventive_action = Column(Text, nullable=True)
    responsible_person = Column(Integer, nullable=False, default=1)
    due_date = Column(DateTime(timezone=True), nullable=False)
    completion_date = Column(DateTime(timezone=True), nullable=True)
    effectiveness_check = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="open")
    priority = Column(Enum(RiskLevel), default=RiskLevel.MEDIUM)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    audit = relationship("ComplianceAudit")


class TrainingRecord(Base):
    __tablename__ = "training_records"
    
    id = Column(Integer, primary_key=True, index=True)
    training_number = Column(String(50), unique=True, nullable=False)
    employee_id = Column(Integer, nullable=False)
    training_title = Column(String(200), nullable=False)
    training_type = Column(String(50), nullable=False)  # AS9100, Quality, Safety, etc.
    training_date = Column(DateTime(timezone=True), nullable=False)
    trainer = Column(String(100), nullable=False)
    duration_hours = Column(Numeric(5, 2), nullable=False)
    competency_level = Column(String(50), nullable=True)
    assessment_score = Column(Numeric(5, 2), nullable=True)
    certificate_number = Column(String(100), nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="completed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships

class SupplierCompliance(Base):
    __tablename__ = "supplier_compliance"
    
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    compliance_score = Column(Numeric(5, 2), nullable=False)
    last_audit_date = Column(DateTime(timezone=True), nullable=True)
    next_audit_date = Column(DateTime(timezone=True), nullable=True)
    certification_status = Column(String(50), nullable=True)
    certification_expiry = Column(DateTime(timezone=True), nullable=True)
    quality_rating = Column(String(50), nullable=True)
    delivery_rating = Column(String(50), nullable=True)
    technical_rating = Column(String(50), nullable=True)
    overall_rating = Column(String(50), nullable=True)
    status = Column(Enum(ComplianceStatus), default=ComplianceStatus.PENDING)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    supplier = relationship("Supplier", foreign_keys=[supplier_id])


class ComplianceDashboard(Base):
    __tablename__ = "compliance_dashboard"
    
    id = Column(Integer, primary_key=True, index=True)
    dashboard_name = Column(String(100), nullable=False)
    total_clauses = Column(Integer, nullable=False)
    compliant_clauses = Column(Integer, nullable=False)
    non_compliant_clauses = Column(Integer, nullable=False)
    pending_clauses = Column(Integer, nullable=False)
    overall_compliance_percentage = Column(Numeric(5, 2), nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
