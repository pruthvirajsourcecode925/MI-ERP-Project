from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from app.database.database import get_db
from app.models.audit import (
    AuditLog, Report, ReportExecution, SystemLog, ActivityLog,
    DataChangeLog, LoginHistory, PerformanceLog, ActionType, ModuleType
)
from app.schemas.audit import (
    AuditLogCreate, AuditLogResponse, ReportCreate, ReportUpdate, ReportResponse,
    ReportExecutionCreate, ReportExecutionResponse, SystemLogCreate, SystemLogResponse,
    ActivityLogCreate, ActivityLogResponse, DataChangeLogCreate, DataChangeLogResponse,
    LoginHistoryCreate, LoginHistoryResponse, PerformanceLogCreate, PerformanceLogResponse,
    AuditLogList, ReportList, ReportExecutionList, SystemLogList, ActivityLogList,
    DataChangeLogList, LoginHistoryList, PerformanceLogList,
    AuditSummary, SystemMetrics, ReportMetrics, DashboardData
)
from app.services.audit import AuditService
from datetime import datetime, timedelta
import uuid

router = APIRouter()


# Audit Log Routes
@router.post("/audit-logs/", response_model=AuditLogResponse)
def create_audit_log(
    audit_log: AuditLogCreate,
    db: Session = Depends(get_db)
):
    """Create an audit log entry."""
    audit_service = AuditService(db)
    log = audit_service.log_action(
        user_id=audit_log.user_id,
        action_type=audit_log.action_type,
        module_type=audit_log.module_type,
        entity_type=audit_log.entity_type,
        entity_id=audit_log.entity_id,
        old_values=audit_log.old_values,
        new_values=audit_log.new_values,
        description=audit_log.description,
        ip_address=audit_log.ip_address,
        user_agent=audit_log.user_agent,
        session_id=audit_log.session_id
    )
    return log


@router.get("/audit-logs/", response_model=AuditLogList)
def list_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    action_type: Optional[ActionType] = Query(None),
    module_type: Optional[ModuleType] = Query(None),
    user_id: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List audit logs with filtering."""
    audit_service = AuditService(db)
    
    if search:
        logs = audit_service.search_audit_logs(
            search_term=search,
            start_date=start_date,
            end_date=end_date,
            action_type=action_type,
            module_type=module_type,
            user_id=user_id,
            limit=limit
        )
        total = len(logs)
    else:
        query = db.query(AuditLog)
        
        if action_type:
            query = query.filter(AuditLog.action_type == action_type)
        
        if module_type:
            query = query.filter(AuditLog.module_type == module_type)
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        
        if start_date:
            query = query.filter(AuditLog.timestamp >= start_date)
        
        if end_date:
            query = query.filter(AuditLog.timestamp <= end_date)
        
        total = query.count()
        logs = query.order_by(desc(AuditLog.timestamp)).offset(skip).limit(limit).all()
    
    return AuditLogList(
        logs=logs,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/audit-logs/summary", response_model=AuditSummary)
def get_audit_summary(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get audit summary for dashboard."""
    audit_service = AuditService(db)
    summary = audit_service.get_audit_summary(start_date, end_date)
    return AuditSummary(**summary)


# Report Management Routes
@router.post("/reports/", response_model=ReportResponse)
def create_report(
    report: ReportCreate,
    db: Session = Depends(get_db)
):
    """Create a new report."""
    db_report = Report(**report.dict(), created_by=1)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


@router.get("/reports/", response_model=ReportList)
def list_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    report_type: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """List reports."""
    query = db.query(Report)
    
    if report_type:
        query = query.filter(Report.report_type == report_type)
    
    if is_active is not None:
        query = query.filter(Report.is_active == is_active)
    
    total = query.count()
    reports = query.offset(skip).limit(limit).all()
    
    return ReportList(
        reports=reports,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.post("/reports/{report_id}/execute", response_model=ReportExecutionResponse)
def execute_report(
    report_id: int,
    parameters: Optional[dict] = None,
    db: Session = Depends(get_db)
):
    """Execute a report."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    execution = ReportExecution(
        report_id=report_id,
        status="running",
        parameters_used=parameters,
        executed_by=1
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)
    
    # Here you would implement the actual report execution logic
    # For now, we'll just mark it as completed with sample data
    
    execution.status = "completed"
    execution.result_data = {"message": "Report executed successfully"}
    execution.execution_time_seconds = 1.5
    db.commit()
    db.refresh(execution)
    
    return execution


@router.get("/reports/{report_id}/executions", response_model=ReportExecutionList)
def list_report_executions(
    report_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List report executions."""
    query = db.query(ReportExecution).filter(ReportExecution.report_id == report_id)
    total = query.count()
    executions = query.order_by(desc(ReportExecution.execution_date)).offset(skip).limit(limit).all()
    
    return ReportExecutionList(
        executions=executions,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# System Log Routes
@router.post("/system-logs/", response_model=SystemLogResponse)
def create_system_log(
    system_log: SystemLogCreate,
    db: Session = Depends(get_db)
):
    """Create a system log entry."""
    audit_service = AuditService(db)
    log = audit_service.log_system_event(
        log_level=system_log.log_level,
        module=system_log.module,
        message=system_log.message,
        details=system_log.details,
        stack_trace=system_log.stack_trace,
        user_id=system_log.user_id,
        ip_address=system_log.ip_address
    )
    return log


@router.get("/system-logs/", response_model=SystemLogList)
def list_system_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    log_level: Optional[str] = Query(None),
    module: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """List system logs."""
    query = db.query(SystemLog)
    
    if log_level:
        query = query.filter(SystemLog.log_level == log_level)
    
    if module:
        query = query.filter(SystemLog.module == module)
    
    if start_date:
        query = query.filter(SystemLog.timestamp >= start_date)
    
    if end_date:
        query = query.filter(SystemLog.timestamp <= end_date)
    
    total = query.count()
    logs = query.order_by(desc(SystemLog.timestamp)).offset(skip).limit(limit).all()
    
    return SystemLogList(
        logs=logs,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Activity Log Routes
@router.post("/activity-logs/", response_model=ActivityLogResponse)
def create_activity_log(
    activity_log: ActivityLogCreate,
    db: Session = Depends(get_db)
):
    """Create an activity log entry."""
    audit_service = AuditService(db)
    log = audit_service.log_activity(
        user_id=activity_log.user_id,
        activity_type=activity_log.activity_type,
        description=activity_log.description,
        module=activity_log.module,
        entity_id=activity_log.entity_id,
        activity_metadata=activity_log.activity_metadata
    )
    return log


@router.get("/activity-logs/", response_model=ActivityLogList)
def list_activity_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: Optional[int] = Query(None),
    activity_type: Optional[str] = Query(None),
    module: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List activity logs."""
    query = db.query(ActivityLog)
    
    if user_id:
        query = query.filter(ActivityLog.user_id == user_id)
    
    if activity_type:
        query = query.filter(ActivityLog.activity_type == activity_type)
    
    if module:
        query = query.filter(ActivityLog.module == module)
    
    total = query.count()
    activities = query.order_by(desc(ActivityLog.timestamp)).offset(skip).limit(limit).all()
    
    return ActivityLogList(
        activities=activities,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Login History Routes
@router.post("/login-history/", response_model=LoginHistoryResponse)
def create_login_history(
    login_history: LoginHistoryCreate,
    db: Session = Depends(get_db)
):
    """Create a login history entry."""
    audit_service = AuditService(db)
    login = audit_service.log_login(
        user_id=login_history.user_id,
        ip_address=login_history.ip_address,
        user_agent=login_history.user_agent,
        session_id=login_history.session_id,
        login_status=login_history.login_status,
        failure_reason=login_history.failure_reason
    )
    return login


@router.get("/login-history/", response_model=LoginHistoryList)
def list_login_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: Optional[int] = Query(None),
    login_status: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """List login history."""
    query = db.query(LoginHistory)
    
    if user_id:
        query = query.filter(LoginHistory.user_id == user_id)
    
    if login_status:
        query = query.filter(LoginHistory.login_status == login_status)
    
    if start_date:
        query = query.filter(LoginHistory.login_time >= start_date)
    
    if end_date:
        query = query.filter(LoginHistory.login_time <= end_date)
    
    total = query.count()
    logins = query.order_by(desc(LoginHistory.login_time)).offset(skip).limit(limit).all()
    
    return LoginHistoryList(
        logins=logins,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Performance Log Routes
@router.post("/performance-logs/", response_model=PerformanceLogResponse)
def create_performance_log(
    performance_log: PerformanceLogCreate,
    db: Session = Depends(get_db)
):
    """Create a performance log entry."""
    audit_service = AuditService(db)
    log = audit_service.log_performance(
        endpoint=performance_log.endpoint,
        method=performance_log.method,
        response_time_ms=float(performance_log.response_time_ms),
        status_code=performance_log.status_code,
        user_id=performance_log.user_id,
        ip_address=performance_log.ip_address,
        request_size=performance_log.request_size,
        response_size=performance_log.response_size
    )
    return log


@router.get("/performance-logs/", response_model=PerformanceLogList)
def list_performance_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    endpoint: Optional[str] = Query(None),
    status_code: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """List performance logs."""
    query = db.query(PerformanceLog)
    
    if endpoint:
        query = query.filter(PerformanceLog.endpoint.ilike(f"%{endpoint}%"))
    
    if status_code:
        query = query.filter(PerformanceLog.status_code == status_code)
    
    if start_date:
        query = query.filter(PerformanceLog.timestamp >= start_date)
    
    if end_date:
        query = query.filter(PerformanceLog.timestamp <= end_date)
    
    total = query.count()
    performances = query.order_by(desc(PerformanceLog.timestamp)).offset(skip).limit(limit).all()
    
    return PerformanceLogList(
        performances=performances,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Dashboard Routes
@router.get("/dashboard/system-metrics", response_model=SystemMetrics)
def get_system_metrics(
    db: Session = Depends(get_db)
):
    """Get system metrics for dashboard."""
    audit_service = AuditService(db)
    metrics = audit_service.get_system_metrics()
    return SystemMetrics(**metrics)


@router.get("/dashboard/report-metrics", response_model=ReportMetrics)
def get_report_metrics(
    db: Session = Depends(get_db)
):
    """Get report metrics for dashboard."""
    audit_service = AuditService(db)
    metrics = audit_service.get_report_metrics()
    return ReportMetrics(**metrics)


@router.get("/dashboard/data", response_model=DashboardData)
def get_dashboard_data(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get complete dashboard data."""
    audit_service = AuditService(db)
    
    audit_summary = audit_service.get_audit_summary(start_date, end_date)
    system_metrics = audit_service.get_system_metrics()
    report_metrics = audit_service.get_report_metrics()
    
    # Get recent alerts (system errors, failed logins, etc.)
    recent_alerts = db.query(SystemLog).filter(
        and_(
            SystemLog.log_level.in_(["ERROR", "CRITICAL"]),
            SystemLog.timestamp >= datetime.utcnow() - timedelta(days=7)
        )
    ).order_by(desc(SystemLog.timestamp)).limit(5).all()
    
    alerts_data = [
        {
            "timestamp": alert.timestamp.isoformat(),
            "level": alert.log_level,
            "module": alert.module,
            "message": alert.message
        }
        for alert in recent_alerts
    ]
    
    # Get upcoming tasks (overdue actions, upcoming audits, etc.)
    from app.models.compliance import CorrectiveAction, ComplianceAudit
    
    overdue_actions = db.query(CorrectiveAction).filter(
        and_(
            CorrectiveAction.due_date < datetime.utcnow(),
            CorrectiveAction.status == "open"
        )
    ).order_by(CorrectiveAction.due_date).limit(5).all()
    
    upcoming_audits = db.query(ComplianceAudit).filter(
        and_(
            ComplianceAudit.audit_date > datetime.utcnow(),
            ComplianceAudit.audit_date <= datetime.utcnow() + timedelta(days=30)
        )
    ).order_by(ComplianceAudit.audit_date).limit(5).all()
    
    tasks_data = [
        {
            "type": "overdue_action",
            "title": f"Overdue Action: {action.action_number}",
            "due_date": action.due_date.isoformat(),
            "priority": action.priority.value
        }
        for action in overdue_actions
    ] + [
        {
            "type": "upcoming_audit",
            "title": f"Upcoming Audit: {audit.audit_number}",
            "due_date": audit.audit_date.isoformat(),
            "priority": "medium"
        }
        for audit in upcoming_audits
    ]
    
    return DashboardData(
        audit_summary=AuditSummary(**audit_summary),
        system_metrics=SystemMetrics(**system_metrics),
        report_metrics=ReportMetrics(**report_metrics),
        recent_alerts=alerts_data,
        upcoming_tasks=tasks_data
    )


# Audit Trail Routes
@router.get("/audit-trail/{entity_type}/{entity_id}")
def get_audit_trail(
    entity_type: str,
    entity_id: int,
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get complete audit trail for an entity."""
    audit_service = AuditService(db)
    trail = audit_service.get_audit_trail(entity_type, entity_id, limit)
    
    return [
        {
            "timestamp": log.timestamp.isoformat(),
            "user": f"User {log.user_id}" if log.user_id else "Unknown",
            "action": log.action_type.value,
            "module": log.module_type.value,
            "description": log.description,
            "old_values": log.old_values,
            "new_values": log.new_values
        }
        for log in trail
    ]


@router.get("/user-activity/{user_id}")
def get_user_activity(
    user_id: int,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get user activity log."""
    audit_service = AuditService(db)
    activities = audit_service.get_user_activity(user_id, start_date, end_date, limit)
    
    return [
        {
            "timestamp": activity.timestamp.isoformat(),
            "activity_type": activity.activity_type,
            "description": activity.description,
            "module": activity.module,
            "activity_metadata": activity.activity_metadata
        }
        for activity in activities
    ]
