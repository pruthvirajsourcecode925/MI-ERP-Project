from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.database.database import get_db
from app.models.compliance import (
    ComplianceClause, ComplianceCheck, ComplianceAudit, CorrectiveAction,
    TrainingRecord, SupplierCompliance, ComplianceDashboard,
    ComplianceStatus, RiskLevel, AuditType
)
from app.schemas.compliance import (
    ComplianceClauseCreate, ComplianceClauseUpdate, ComplianceClauseResponse,
    ComplianceCheckCreate, ComplianceCheckUpdate, ComplianceCheckResponse,
    ComplianceAuditCreate, ComplianceAuditUpdate, ComplianceAuditResponse,
    CorrectiveActionCreate, CorrectiveActionUpdate, CorrectiveActionResponse,
    TrainingRecordCreate, TrainingRecordUpdate, TrainingRecordResponse,
    SupplierComplianceCreate, SupplierComplianceUpdate, SupplierComplianceResponse,
    ComplianceDashboardResponse, ComplianceClauseList, ComplianceCheckList,
    ComplianceAuditList, CorrectiveActionList, TrainingRecordList,
    SupplierComplianceList, ComplianceMetrics, ComplianceReport
)
import uuid
from datetime import datetime, timedelta

router = APIRouter()


def generate_audit_number():
    """Generate unique audit number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"AUD-{year}-{random_id}"


def generate_action_number():
    """Generate unique corrective action number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"CA-{year}-{random_id}"


def generate_training_number():
    """Generate unique training number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"TRN-{year}-{random_id}"


# Compliance Clause Routes
@router.post("/clauses/", response_model=ComplianceClauseResponse)
def create_compliance_clause(
    clause: ComplianceClauseCreate,
    db: Session = Depends(get_db)
):
    """Create a new compliance clause."""
    db_clause = ComplianceClause(**clause.dict())
    db.add(db_clause)
    db.commit()
    db.refresh(db_clause)
    return db_clause


@router.get("/clauses/", response_model=ComplianceClauseList)
def list_compliance_clauses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[ComplianceStatus] = Query(None),
    risk_level: Optional[RiskLevel] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List compliance clauses with filtering."""
    query = db.query(ComplianceClause)
    
    if status:
        query = query.filter(ComplianceClause.status == status)
    
    if risk_level:
        query = query.filter(ComplianceClause.risk_level == risk_level)
    
    if search:
        query = query.filter(
            or_(
                ComplianceClause.clause_number.ilike(f"%{search}%"),
                ComplianceClause.clause_title.ilike(f"%{search}%"),
                ComplianceClause.description.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    clauses = query.offset(skip).limit(limit).all()
    
    return ComplianceClauseList(
        clauses=clauses,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/clauses/{clause_id}", response_model=ComplianceClauseResponse)
def get_compliance_clause(
    clause_id: int,
    db: Session = Depends(get_db)
):
    """Get specific compliance clause."""
    clause = db.query(ComplianceClause).filter(ComplianceClause.id == clause_id).first()
    if not clause:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compliance clause not found"
        )
    return clause


@router.put("/clauses/{clause_id}", response_model=ComplianceClauseResponse)
def update_compliance_clause(
    clause_id: int,
    clause_update: ComplianceClauseUpdate,
    db: Session = Depends(get_db)
):
    """Update compliance clause."""
    clause = db.query(ComplianceClause).filter(ComplianceClause.id == clause_id).first()
    if not clause:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compliance clause not found"
        )
    
    update_data = clause_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(clause, field, value)
    
    db.commit()
    db.refresh(clause)
    return clause


# Compliance Check Routes
@router.post("/checks/", response_model=ComplianceCheckResponse)
def create_compliance_check(
    check: ComplianceCheckCreate,
    db: Session = Depends(get_db)
):
    """Create a new compliance check."""
    db_check = ComplianceCheck(**check.dict())
    db.add(db_check)
    db.commit()
    db.refresh(db_check)
    return db_check


@router.get("/checks/", response_model=ComplianceCheckList)
def list_compliance_checks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[ComplianceStatus] = Query(None),
    db: Session = Depends(get_db)
):
    """List compliance checks."""
    query = db.query(ComplianceCheck)
    
    if status:
        query = query.filter(ComplianceCheck.status == status)
    
    total = query.count()
    checks = query.offset(skip).limit(limit).all()
    
    return ComplianceCheckList(
        checks=checks,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.put("/checks/{check_id}/complete")
def complete_compliance_check(
    check_id: int,
    evidence_location: Optional[str] = Query(None),
    notes: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Complete a compliance check."""
    check = db.query(ComplianceCheck).filter(ComplianceCheck.id == check_id).first()
    if not check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compliance check not found"
        )
    
    check.status = ComplianceStatus.COMPLIANT
    check.last_checked = datetime.utcnow()
    check.evidence_location = evidence_location
    check.notes = notes
    
    # Update next check date based on frequency
    if check.frequency == "daily":
        check.next_check = datetime.utcnow() + timedelta(days=1)
    elif check.frequency == "weekly":
        check.next_check = datetime.utcnow() + timedelta(weeks=1)
    elif check.frequency == "monthly":
        check.next_check = datetime.utcnow() + timedelta(days=30)
    elif check.frequency == "quarterly":
        check.next_check = datetime.utcnow() + timedelta(days=90)
    elif check.frequency == "yearly":
        check.next_check = datetime.utcnow() + timedelta(days=365)
    
    db.commit()
    db.refresh(check)
    return {"message": "Compliance check completed successfully"}


# Compliance Audit Routes
@router.post("/audits/", response_model=ComplianceAuditResponse)
def create_compliance_audit(
    audit: ComplianceAuditCreate,
    db: Session = Depends(get_db)
):
    """Create a new compliance audit."""
    audit_number = generate_audit_number()
    
    # Verify auditor and auditee exist
    auditor = db.query(User).filter(User.id == audit.auditor_id).first()
    if not auditor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Auditor not found"
        )
    
    auditee = db.query(User).filter(User.id == audit.auditee_id).first()
    if not auditee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Auditee not found"
        )
    
    db_audit = ComplianceAudit(**audit.dict(), audit_number=audit_number)
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    return db_audit


@router.get("/audits/", response_model=ComplianceAuditList)
def list_compliance_audits(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    audit_type: Optional[AuditType] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List compliance audits."""
    query = db.query(ComplianceAudit)
    
    if audit_type:
        query = query.filter(ComplianceAudit.audit_type == audit_type)
    
    if status:
        query = query.filter(ComplianceAudit.status == status)
    
    total = query.count()
    audits = query.offset(skip).limit(limit).all()
    
    return ComplianceAuditList(
        audits=audits,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Corrective Action Routes
@router.post("/corrective-actions/", response_model=CorrectiveActionResponse)
def create_corrective_action(
    action: CorrectiveActionCreate,
    db: Session = Depends(get_db)
):
    """Create a new corrective action."""
    action_number = generate_action_number()
    
    # Verify responsible person exists
    responsible = db.query(User).filter(User.id == action.responsible_person).first()
    if not responsible:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Responsible person not found"
        )
    
    db_action = CorrectiveAction(**action.dict(), action_number=action_number)
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action


@router.get("/corrective-actions/", response_model=CorrectiveActionList)
def list_corrective_actions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    priority: Optional[RiskLevel] = Query(None),
    db: Session = Depends(get_db)
):
    """List corrective actions."""
    query = db.query(CorrectiveAction)
    
    if status:
        query = query.filter(CorrectiveAction.status == status)
    
    if priority:
        query = query.filter(CorrectiveAction.priority == priority)
    
    total = query.count()
    actions = query.offset(skip).limit(limit).all()
    
    return CorrectiveActionList(
        actions=actions,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.put("/corrective-actions/{action_id}/complete")
def complete_corrective_action(
    action_id: int,
    effectiveness_check_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Complete a corrective action."""
    action = db.query(CorrectiveAction).filter(CorrectiveAction.id == action_id).first()
    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corrective action not found"
        )
    
    action.status = "completed"
    action.completion_date = datetime.utcnow()
    action.effectiveness_check = effectiveness_check_date
    
    db.commit()
    db.refresh(action)
    return {"message": "Corrective action completed successfully"}


# Training Record Routes
@router.post("/training-records/", response_model=TrainingRecordResponse)
def create_training_record(
    training: TrainingRecordCreate,
    db: Session = Depends(get_db)
):
    """Create a new training record."""
    training_number = generate_training_number()
    
    # Verify employee exists
    employee = db.query(User).filter(User.id == training.employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    db_training = TrainingRecord(**training.dict(), training_number=training_number)
    db.add(db_training)
    db.commit()
    db.refresh(db_training)
    return db_training


@router.get("/training-records/", response_model=TrainingRecordList)
def list_training_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    training_type: Optional[str] = Query(None),
    employee_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List training records."""
    query = db.query(TrainingRecord)
    
    if training_type:
        query = query.filter(TrainingRecord.training_type == training_type)
    
    if employee_id:
        query = query.filter(TrainingRecord.employee_id == employee_id)
    
    total = query.count()
    trainings = query.offset(skip).limit(limit).all()
    
    return TrainingRecordList(
        trainings=trainings,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Supplier Compliance Routes
@router.post("/supplier-compliance/", response_model=SupplierComplianceResponse)
def create_supplier_compliance(
    compliance: SupplierComplianceCreate,
    db: Session = Depends(get_db)
):
    """Create supplier compliance record."""
    # Verify supplier exists
    from app.models.purchase import Supplier
    supplier = db.query(Supplier).filter(Supplier.id == compliance.supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    db_compliance = SupplierCompliance(**compliance.dict())
    db.add(db_compliance)
    db.commit()
    db.refresh(db_compliance)
    return db_compliance


@router.get("/supplier-compliance/", response_model=SupplierComplianceList)
def list_supplier_compliance(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[ComplianceStatus] = Query(None),
    db: Session = Depends(get_db)
):
    """List supplier compliance records."""
    query = db.query(SupplierCompliance)
    
    if status:
        query = query.filter(SupplierCompliance.status == status)
    
    total = query.count()
    compliances = query.offset(skip).limit(limit).all()
    
    return SupplierComplianceList(
        suppliers=compliances,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Compliance Dashboard Routes
@router.get("/dashboard/metrics", response_model=ComplianceMetrics)
def get_compliance_metrics(
    db: Session = Depends(get_db)
):
    """Get compliance dashboard metrics."""
    # Get clause metrics
    total_clauses = db.query(ComplianceClause).count()
    compliant_clauses = db.query(ComplianceClause).filter(ComplianceClause.status == ComplianceStatus.COMPLIANT).count()
    non_compliant_clauses = db.query(ComplianceClause).filter(ComplianceClause.status == ComplianceStatus.NON_COMPLIANT).count()
    pending_clauses = db.query(ComplianceClause).filter(ComplianceClause.status == ComplianceStatus.PENDING).count()
    
    overall_compliance_percentage = (compliant_clauses / total_clauses * 100) if total_clauses > 0 else 0
    
    # Get risk metrics
    high_risk_items = db.query(ComplianceClause).filter(ComplianceClause.risk_level == RiskLevel.HIGH).count()
    medium_risk_items = db.query(ComplianceClause).filter(ComplianceClause.risk_level == RiskLevel.MEDIUM).count()
    low_risk_items = db.query(ComplianceClause).filter(ComplianceClause.risk_level == RiskLevel.LOW).count()
    
    # Get overdue checks
    overdue_checks = db.query(ComplianceCheck).filter(
        and_(
            ComplianceCheck.next_check < datetime.utcnow(),
            ComplianceCheck.status != ComplianceStatus.COMPLIANT
        )
    ).count()
    
    # Get pending audits
    pending_audits = db.query(ComplianceAudit).filter(ComplianceAudit.status == "planned").count()
    
    # Get open corrective actions
    open_corrective_actions = db.query(CorrectiveAction).filter(CorrectiveAction.status == "open").count()
    
    return ComplianceMetrics(
        total_clauses=total_clauses,
        compliant_clauses=compliant_clauses,
        non_compliant_clauses=non_compliant_clauses,
        pending_clauses=pending_clauses,
        overall_compliance_percentage=overall_compliance_percentage,
        high_risk_items=high_risk_items,
        medium_risk_items=medium_risk_items,
        low_risk_items=low_risk_items,
        overdue_checks=overdue_checks,
        pending_audits=pending_audits,
        open_corrective_actions=open_corrective_actions
    )


@router.get("/dashboard/report", response_model=ComplianceReport)
def get_compliance_report(
    db: Session = Depends(get_db)
):
    """Generate comprehensive compliance report."""
    metrics = get_compliance_metrics(db, current_user)
    
    # Get clauses by status
    clauses_by_status = {}
    for status in ComplianceStatus:
        count = db.query(ComplianceClause).filter(ComplianceClause.status == status).count()
        clauses_by_status[status.value] = count
    
    # Get clauses by risk
    clauses_by_risk = {}
    for risk in RiskLevel:
        count = db.query(ComplianceClause).filter(ComplianceClause.risk_level == risk).count()
        clauses_by_risk[risk.value] = count
    
    # Get upcoming audits
    upcoming_audits = db.query(ComplianceAudit).filter(
        and_(
            ComplianceAudit.audit_date > datetime.utcnow(),
            ComplianceAudit.status == "planned"
        )
    ).order_by(ComplianceAudit.audit_date).limit(10).all()
    
    # Get overdue actions
    overdue_actions = db.query(CorrectiveAction).filter(
        and_(
            CorrectiveAction.due_date < datetime.utcnow(),
            CorrectiveAction.status == "open"
        )
    ).order_by(CorrectiveAction.due_date).limit(10).all()
    
    # Get supplier compliance summary
    supplier_compliance_summary = {}
    supplier_compliances = db.query(SupplierCompliance).all()
    for compliance in supplier_compliances:
        supplier_compliance_summary[compliance.supplier_id] = {
            "compliance_score": compliance.compliance_score,
            "status": compliance.status.value,
            "overall_rating": compliance.overall_rating
        }
    
    return ComplianceReport(
        report_date=datetime.utcnow(),
        metrics=metrics,
        clauses_by_status=clauses_by_status,
        clauses_by_risk=clauses_by_risk,
        upcoming_audits=[
            {
                "audit_number": audit.audit_number,
                "audit_title": audit.audit_title,
                "audit_date": audit.audit_date,
                "auditor": audit.auditor.full_name if audit.auditor else "Unknown"
            }
            for audit in upcoming_audits
        ],
        overdue_actions=[
            {
                "action_number": action.action_number,
                "description": action.description,
                "due_date": action.due_date,
                "priority": action.priority.value,
                "responsible": action.responsible.full_name if action.responsible else "Unknown"
            }
            for action in overdue_actions
        ],
        supplier_compliance_summary=supplier_compliance_summary
    )


# Initialize AS9100D Clauses
@router.post("/initialize-as9100d-clauses")
def initialize_as9100d_clauses(
    db: Session = Depends(get_db)
):
    """Initialize AS9100D standard clauses."""
    as9100d_clauses = [
        {
            "clause_number": "4.2",
            "clause_title": "Documentation Requirements",
            "description": "Documentation requirements for quality management system",
            "requirement": "Quality management system documentation shall include documented procedures",
            "risk_level": RiskLevel.MEDIUM
        },
        {
            "clause_number": "5.1",
            "clause_title": "Management Commitment",
            "description": "Top management commitment to quality management system",
            "requirement": "Top management shall provide evidence of its commitment",
            "risk_level": RiskLevel.HIGH
        },
        {
            "clause_number": "5.3",
            "clause_title": "Quality Policy",
            "description": "Quality policy requirements",
            "requirement": "Top management shall ensure quality policy is communicated and understood",
            "risk_level": RiskLevel.MEDIUM
        },
        {
            "clause_number": "6.1",
            "clause_title": "Resource Provision",
            "description": "Resource provision requirements",
            "requirement": "Organization shall determine and provide resources needed",
            "risk_level": RiskLevel.MEDIUM
        },
        {
            "clause_number": "7.1",
            "clause_title": "Planning of Product Realization",
            "description": "Planning of product realization processes",
            "requirement": "Organization shall plan and develop product realization processes",
            "risk_level": RiskLevel.HIGH
        },
        {
            "clause_number": "7.2",
            "clause_title": "Customer-Related Processes",
            "description": "Customer-related processes requirements",
            "requirement": "Organization shall determine customer requirements",
            "risk_level": RiskLevel.HIGH
        },
        {
            "clause_number": "7.3",
            "clause_title": "Design and Development",
            "description": "Design and development requirements",
            "requirement": "Organization shall plan and control design and development",
            "risk_level": RiskLevel.HIGH
        },
        {
            "clause_number": "7.4",
            "clause_title": "Purchasing",
            "description": "Purchasing process requirements",
            "requirement": "Organization shall ensure purchased product conforms to requirements",
            "risk_level": RiskLevel.HIGH
        },
        {
            "clause_number": "7.5",
            "clause_title": "Production and Service Provision",
            "description": "Production and service provision requirements",
            "requirement": "Organization shall plan and control production and service provision",
            "risk_level": RiskLevel.HIGH
        },
        {
            "clause_number": "7.6",
            "clause_title": "Control of Monitoring and Measuring Equipment",
            "description": "Control of monitoring and measuring equipment",
            "requirement": "Organization shall determine monitoring and measuring equipment needed",
            "risk_level": RiskLevel.MEDIUM
        },
        {
            "clause_number": "8.1",
            "clause_title": "Measurement, Analysis and Improvement",
            "description": "Measurement, analysis and improvement requirements",
            "requirement": "Organization shall plan and implement monitoring, measurement, analysis and improvement",
            "risk_level": RiskLevel.MEDIUM
        },
        {
            "clause_number": "8.2",
            "clause_title": "Monitoring and Measurement",
            "description": "Monitoring and measurement requirements",
            "requirement": "Organization shall monitor and measure quality management system processes",
            "risk_level": RiskLevel.MEDIUM
        },
        {
            "clause_number": "8.3",
            "clause_title": "Control of Nonconforming Product",
            "description": "Control of nonconforming product requirements",
            "requirement": "Organization shall ensure product which does not conform is identified and controlled",
            "risk_level": RiskLevel.HIGH
        },
        {
            "clause_number": "8.4",
            "clause_title": "Analysis of Data",
            "description": "Analysis of data requirements",
            "requirement": "Organization shall collect and analyze appropriate data",
            "risk_level": RiskLevel.MEDIUM
        },
        {
            "clause_number": "8.5",
            "clause_title": "Improvement",
            "description": "Improvement requirements",
            "requirement": "Organization shall continually improve the effectiveness of the quality management system",
            "risk_level": RiskLevel.MEDIUM
        }
    ]
    
    created_count = 0
    for clause_data in as9100d_clauses:
        existing = db.query(ComplianceClause).filter(ComplianceClause.clause_number == clause_data["clause_number"]).first()
        if not existing:
            clause = ComplianceClause(**clause_data)
            db.add(clause)
            created_count += 1
    
    db.commit()
    return {"message": f"Initialized {created_count} AS9100D clauses"}
