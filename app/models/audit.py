from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Numeric, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base
from enum import Enum as PyEnum


class ActionType(PyEnum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    REJECT = "reject"
    LOGIN = "login"
    LOGOUT = "logout"
    VIEW = "view"
    EXPORT = "export"
    IMPORT = "import"
    PRINT = "print"


class ModuleType(PyEnum):
    SALES = "sales"
    ENGINEERING = "engineering"
    PURCHASE = "purchase"
    STORES = "stores"
    PRODUCTION = "production"
    QUALITY = "quality"
    MAINTENANCE = "maintenance"
    DISPATCH = "dispatch"
    DOCUMENT_CONTROL = "document_control"
    USERS = "users"
    PERMISSIONS = "permissions"
    COMPLIANCE = "compliance"
    ADMIN = "admin"


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    action_type = Column(Enum(ActionType), nullable=False)
    module_type = Column(Enum(ModuleType), nullable=False)
    entity_type = Column(String(100), nullable=False)  # Table name
    entity_id = Column(Integer, nullable=True)  # Record ID
    old_values = Column(JSON, nullable=True)  # Previous values
    new_values = Column(JSON, nullable=True)  # New values
    description = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    session_id = Column(String(100), nullable=True)


class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_name = Column(String(200), nullable=False)
    report_type = Column(String(50), nullable=False)  # sales, production, quality, etc.
    description = Column(Text, nullable=True)
    parameters = Column(JSON, nullable=True)  # Report parameters
    query = Column(Text, nullable=True)  # SQL query or data source
    template = Column(Text, nullable=True)  # Report template
    schedule = Column(String(50), nullable=True)  # daily, weekly, monthly
    recipients = Column(JSON, nullable=True)  # Email recipients
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ReportExecution(Base):
    __tablename__ = "report_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    execution_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="running")  # running, completed, failed
    parameters_used = Column(JSON, nullable=True)
    result_data = Column(JSON, nullable=True)  # Report data
    file_path = Column(String(500), nullable=True)  # Generated file path
    error_message = Column(Text, nullable=True)
    execution_time_seconds = Column(Numeric(10, 2), nullable=True)
    executed_by = Column(Integer, nullable=False)
    
    # Relationships
    report = relationship("Report")


class SystemLog(Base):
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    log_level = Column(String(20), nullable=False)  # INFO, WARNING, ERROR, CRITICAL
    module = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    details = Column(JSON, nullable=True)
    stack_trace = Column(Text, nullable=True)
    user_id = Column(Integer, nullable=True)
    ip_address = Column(String(45), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    activity_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    module = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=True)
    activity_metadata = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class DataChangeLog(Base):
    __tablename__ = "data_change_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String(100), nullable=False)
    record_id = Column(Integer, nullable=False)
    operation = Column(String(20), nullable=False)  # INSERT, UPDATE, DELETE
    changed_by = Column(Integer, nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    field_changes = Column(JSON, nullable=True)  # Specific field changes


class LoginHistory(Base):
    __tablename__ = "login_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    login_time = Column(DateTime(timezone=True), server_default=func.now())
    logout_time = Column(DateTime(timezone=True), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    session_id = Column(String(100), nullable=True)
    login_status = Column(String(20), default="success")  # success, failed
    failure_reason = Column(String(200), nullable=True)


class PerformanceLog(Base):
    __tablename__ = "performance_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(200), nullable=False)
    method = Column(String(10), nullable=False)
    response_time_ms = Column(Numeric(10, 2), nullable=False)
    status_code = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=True)
    ip_address = Column(String(45), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    request_size = Column(Integer, nullable=True)
    response_size = Column(Integer, nullable=True)