from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from app.models.audit import ActionType, ModuleType


class AuditLogBase(BaseModel):
    user_id: int
    action_type: ActionType
    module_type: ModuleType
    entity_type: str
    entity_id: Optional[int] = None
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogResponse(AuditLogBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ReportBase(BaseModel):
    report_name: str
    report_type: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    query: Optional[str] = None
    template: Optional[str] = None
    schedule: Optional[str] = None
    recipients: Optional[List[str]] = None
    is_active: bool = True


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    report_name: Optional[str] = None
    report_type: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    query: Optional[str] = None
    template: Optional[str] = None
    schedule: Optional[str] = None
    recipients: Optional[List[str]] = None
    is_active: Optional[bool] = None


class ReportResponse(ReportBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ReportExecutionBase(BaseModel):
    report_id: int
    status: str = "running"
    parameters_used: Optional[Dict[str, Any]] = None
    result_data: Optional[Dict[str, Any]] = None
    file_path: Optional[str] = None
    error_message: Optional[str] = None
    execution_time_seconds: Optional[Decimal] = None


class ReportExecutionCreate(ReportExecutionBase):
    executed_by: int


class ReportExecutionResponse(ReportExecutionBase):
    id: int
    execution_date: datetime
    executed_by: int
    
    class Config:
        from_attributes = True


class SystemLogBase(BaseModel):
    log_level: str
    module: str
    message: str
    details: Optional[Dict[str, Any]] = None
    stack_trace: Optional[str] = None
    user_id: Optional[int] = None
    ip_address: Optional[str] = None


class SystemLogCreate(SystemLogBase):
    pass


class SystemLogResponse(SystemLogBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ActivityLogBase(BaseModel):
    user_id: int
    activity_type: str
    description: str
    module: str
    entity_id: Optional[int] = None
    activity_metadata: Optional[Dict[str, Any]] = None


class ActivityLogCreate(ActivityLogBase):
    pass


class ActivityLogResponse(ActivityLogBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class DataChangeLogBase(BaseModel):
    table_name: str
    record_id: int
    operation: str
    old_data: Optional[Dict[str, Any]] = None
    new_data: Optional[Dict[str, Any]] = None
    field_changes: Optional[Dict[str, Any]] = None


class DataChangeLogCreate(DataChangeLogBase):
    changed_by: int


class DataChangeLogResponse(DataChangeLogBase):
    id: int
    changed_by: int
    changed_at: datetime
    
    class Config:
        from_attributes = True


class LoginHistoryBase(BaseModel):
    user_id: int
    logout_time: Optional[datetime] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    login_status: str = "success"
    failure_reason: Optional[str] = None


class LoginHistoryCreate(LoginHistoryBase):
    pass


class LoginHistoryResponse(LoginHistoryBase):
    id: int
    login_time: datetime
    
    class Config:
        from_attributes = True


class PerformanceLogBase(BaseModel):
    endpoint: str
    method: str
    response_time_ms: Decimal
    status_code: int
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    request_size: Optional[int] = None
    response_size: Optional[int] = None


class PerformanceLogCreate(PerformanceLogBase):
    pass


class PerformanceLogResponse(PerformanceLogBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


# List response schemas
class AuditLogList(BaseModel):
    logs: List[AuditLogResponse]
    total: int
    page: int
    size: int


class ReportList(BaseModel):
    reports: List[ReportResponse]
    total: int
    page: int
    size: int


class ReportExecutionList(BaseModel):
    executions: List[ReportExecutionResponse]
    total: int
    page: int
    size: int


class SystemLogList(BaseModel):
    logs: List[SystemLogResponse]
    total: int
    page: int
    size: int


class ActivityLogList(BaseModel):
    activities: List[ActivityLogResponse]
    total: int
    page: int
    size: int


class DataChangeLogList(BaseModel):
    changes: List[DataChangeLogResponse]
    total: int
    page: int
    size: int


class LoginHistoryList(BaseModel):
    logins: List[LoginHistoryResponse]
    total: int
    page: int
    size: int


class PerformanceLogList(BaseModel):
    performances: List[PerformanceLogResponse]
    total: int
    page: int
    size: int


# Analytics schemas
class AuditSummary(BaseModel):
    total_actions: int
    actions_by_type: Dict[str, int]
    actions_by_module: Dict[str, int]
    actions_by_user: Dict[str, int]
    recent_activities: List[Dict[str, Any]]
    top_active_users: List[Dict[str, Any]]


class SystemMetrics(BaseModel):
    total_logins: int
    failed_logins: int
    average_response_time: Decimal
    error_rate: Decimal
    active_sessions: int
    system_uptime: str
    database_size: str
    memory_usage: str


class ReportMetrics(BaseModel):
    total_reports: int
    scheduled_reports: int
    executed_today: int
    failed_executions: int
    average_execution_time: Decimal
    most_used_reports: List[Dict[str, Any]]


class ComplianceReport(BaseModel):
    report_period: str
    total_audits: int
    compliance_score: Decimal
    critical_findings: int
    major_findings: int
    minor_findings: int
    overdue_actions: int
    completed_actions: int
    trends: Dict[str, Any]


class DashboardData(BaseModel):
    audit_summary: AuditSummary
    system_metrics: SystemMetrics
    report_metrics: ReportMetrics
    recent_alerts: List[Dict[str, Any]]
    upcoming_tasks: List[Dict[str, Any]]
