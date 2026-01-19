from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models.compliance import ComplianceStatus, RiskLevel, AuditType


class ComplianceClauseBase(BaseModel):
    clause_number: str
    clause_title: str
    description: Optional[str] = None
    requirement: str
    evidence_required: Optional[str] = None
    risk_level: RiskLevel
    status: ComplianceStatus = ComplianceStatus.PENDING
    last_reviewed: Optional[datetime] = None
    next_review: Optional[datetime] = None


class ComplianceClauseCreate(ComplianceClauseBase):
    pass


class ComplianceClauseUpdate(BaseModel):
    clause_number: Optional[str] = None
    clause_title: Optional[str] = None
    description: Optional[str] = None
    requirement: Optional[str] = None
    evidence_required: Optional[str] = None
    risk_level: Optional[RiskLevel] = None
    status: Optional[ComplianceStatus] = None
    last_reviewed: Optional[datetime] = None
    next_review: Optional[datetime] = None


class ComplianceClauseResponse(ComplianceClauseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ComplianceCheckBase(BaseModel):
    clause_id: int
    check_number: str
    check_description: str
    check_type: str
    frequency: str
    responsible_person: int
    status: ComplianceStatus = ComplianceStatus.PENDING
    last_checked: Optional[datetime] = None
    next_check: Optional[datetime] = None
    evidence_location: Optional[str] = None
    notes: Optional[str] = None


class ComplianceCheckCreate(ComplianceCheckBase):
    pass


class ComplianceCheckUpdate(BaseModel):
    clause_id: Optional[int] = None
    check_number: Optional[str] = None
    check_description: Optional[str] = None
    check_type: Optional[str] = None
    frequency: Optional[str] = None
    responsible_person: Optional[int] = None
    status: Optional[ComplianceStatus] = None
    last_checked: Optional[datetime] = None
    next_check: Optional[datetime] = None
    evidence_location: Optional[str] = None
    notes: Optional[str] = None


class ComplianceCheckResponse(ComplianceCheckBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ComplianceAuditBase(BaseModel):
    audit_number: str
    audit_type: AuditType
    audit_title: str
    audit_date: datetime
    auditor_id: int
    auditee_id: int
    scope: str
    criteria: str
    findings: Optional[str] = None
    non_conformities: Optional[str] = None
    observations: Optional[str] = None
    recommendations: Optional[str] = None
    overall_rating: Optional[str] = None
    status: str = "planned"


class ComplianceAuditCreate(ComplianceAuditBase):
    pass


class ComplianceAuditUpdate(BaseModel):
    audit_number: Optional[str] = None
    audit_type: Optional[AuditType] = None
    audit_title: Optional[str] = None
    audit_date: Optional[datetime] = None
    auditor_id: Optional[int] = None
    auditee_id: Optional[int] = None
    scope: Optional[str] = None
    criteria: Optional[str] = None
    findings: Optional[str] = None
    non_conformities: Optional[str] = None
    observations: Optional[str] = None
    recommendations: Optional[str] = None
    overall_rating: Optional[str] = None
    status: Optional[str] = None


class ComplianceAuditResponse(ComplianceAuditBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CorrectiveActionBase(BaseModel):
    action_number: str
    audit_id: Optional[int] = None
    source_type: str
    source_id: Optional[int] = None
    description: str
    root_cause: Optional[str] = None
    correction: Optional[str] = None
    corrective_action: str
    preventive_action: Optional[str] = None
    responsible_person: int
    due_date: datetime
    completion_date: Optional[datetime] = None
    effectiveness_check: Optional[datetime] = None
    status: str = "open"
    priority: RiskLevel = RiskLevel.MEDIUM


class CorrectiveActionCreate(CorrectiveActionBase):
    pass


class CorrectiveActionUpdate(BaseModel):
    action_number: Optional[str] = None
    audit_id: Optional[int] = None
    source_type: Optional[str] = None
    source_id: Optional[int] = None
    description: Optional[str] = None
    root_cause: Optional[str] = None
    correction: Optional[str] = None
    corrective_action: Optional[str] = None
    preventive_action: Optional[str] = None
    responsible_person: Optional[int] = None
    due_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    effectiveness_check: Optional[datetime] = None
    status: Optional[str] = None
    priority: Optional[RiskLevel] = None


class CorrectiveActionResponse(CorrectiveActionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TrainingRecordBase(BaseModel):
    training_number: str
    employee_id: int
    training_title: str
    training_type: str
    training_date: datetime
    trainer: str
    duration_hours: Decimal
    competency_level: Optional[str] = None
    assessment_score: Optional[Decimal] = None
    certificate_number: Optional[str] = None
    expiry_date: Optional[datetime] = None
    status: str = "completed"


class TrainingRecordCreate(TrainingRecordBase):
    pass


class TrainingRecordUpdate(BaseModel):
    training_number: Optional[str] = None
    employee_id: Optional[int] = None
    training_title: Optional[str] = None
    training_type: Optional[str] = None
    training_date: Optional[datetime] = None
    trainer: Optional[str] = None
    duration_hours: Optional[Decimal] = None
    competency_level: Optional[str] = None
    assessment_score: Optional[Decimal] = None
    certificate_number: Optional[str] = None
    expiry_date: Optional[datetime] = None
    status: Optional[str] = None


class TrainingRecordResponse(TrainingRecordBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SupplierComplianceBase(BaseModel):
    supplier_id: int
    compliance_score: Decimal
    last_audit_date: Optional[datetime] = None
    next_audit_date: Optional[datetime] = None
    certification_status: Optional[str] = None
    certification_expiry: Optional[datetime] = None
    quality_rating: Optional[str] = None
    delivery_rating: Optional[str] = None
    technical_rating: Optional[str] = None
    overall_rating: Optional[str] = None
    status: ComplianceStatus = ComplianceStatus.PENDING
    notes: Optional[str] = None


class SupplierComplianceCreate(SupplierComplianceBase):
    pass


class SupplierComplianceUpdate(BaseModel):
    supplier_id: Optional[int] = None
    compliance_score: Optional[Decimal] = None
    last_audit_date: Optional[datetime] = None
    next_audit_date: Optional[datetime] = None
    certification_status: Optional[str] = None
    certification_expiry: Optional[datetime] = None
    quality_rating: Optional[str] = None
    delivery_rating: Optional[str] = None
    technical_rating: Optional[str] = None
    overall_rating: Optional[str] = None
    status: Optional[ComplianceStatus] = None
    notes: Optional[str] = None


class SupplierComplianceResponse(SupplierComplianceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ComplianceDashboardBase(BaseModel):
    dashboard_name: str
    total_clauses: int
    compliant_clauses: int
    non_compliant_clauses: int
    pending_clauses: int
    overall_compliance_percentage: Decimal
    last_updated: Optional[datetime] = None


class ComplianceDashboardResponse(ComplianceDashboardBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# List response schemas
class ComplianceClauseList(BaseModel):
    clauses: List[ComplianceClauseResponse]
    total: int
    page: int
    size: int


class ComplianceCheckList(BaseModel):
    checks: List[ComplianceCheckResponse]
    total: int
    page: int
    size: int


class ComplianceAuditList(BaseModel):
    audits: List[ComplianceAuditResponse]
    total: int
    page: int
    size: int


class CorrectiveActionList(BaseModel):
    actions: List[CorrectiveActionResponse]
    total: int
    page: int
    size: int


class TrainingRecordList(BaseModel):
    trainings: List[TrainingRecordResponse]
    total: int
    page: int
    size: int


class SupplierComplianceList(BaseModel):
    suppliers: List[SupplierComplianceResponse]
    total: int
    page: int
    size: int


# Compliance metrics
class ComplianceMetrics(BaseModel):
    total_clauses: int
    compliant_clauses: int
    non_compliant_clauses: int
    pending_clauses: int
    overall_compliance_percentage: Decimal
    high_risk_items: int
    medium_risk_items: int
    low_risk_items: int
    overdue_checks: int
    pending_audits: int
    open_corrective_actions: int


class ComplianceReport(BaseModel):
    report_date: datetime
    metrics: ComplianceMetrics
    clauses_by_status: dict
    clauses_by_risk: dict
    upcoming_audits: List[dict]
    overdue_actions: List[dict]
    supplier_compliance_summary: dict
