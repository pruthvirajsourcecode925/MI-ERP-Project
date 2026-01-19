from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from app.models.audit import (
    AuditLog, Report, ReportExecution, SystemLog, ActivityLog,
    DataChangeLog, LoginHistory, PerformanceLog, ActionType, ModuleType
)
from datetime import datetime, timedelta
import json


class AuditService:
    
    def __init__(self, db: Session):
        self.db = db
    
    def log_action(
        self,
        user_id: int,
        action_type: ActionType,
        module_type: ModuleType,
        entity_type: str,
        entity_id: Optional[int] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> AuditLog:
        """Log user action for audit trail."""
        audit_log = AuditLog(
            user_id=user_id,
            action_type=action_type,
            module_type=module_type,
            entity_type=entity_type,
            entity_id=entity_id,
            old_values=old_values,
            new_values=new_values,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id
        )
        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)
        return audit_log
    
    def log_data_change(
        self,
        table_name: str,
        record_id: int,
        operation: str,
        changed_by: int,
        old_data: Optional[Dict[str, Any]] = None,
        new_data: Optional[Dict[str, Any]] = None,
        field_changes: Optional[Dict[str, Any]] = None
    ) -> DataChangeLog:
        """Log data changes for complete audit trail."""
        data_change = DataChangeLog(
            table_name=table_name,
            record_id=record_id,
            operation=operation,
            changed_by=changed_by,
            old_data=old_data,
            new_data=new_data,
            field_changes=field_changes
        )
        self.db.add(data_change)
        self.db.commit()
        self.db.refresh(data_change)
        return data_change
    
    def log_activity(
        self,
        user_id: int,
        activity_type: str,
        description: str,
        module: str,
        entity_id: Optional[int] = None,
        activity_metadata: Optional[Dict[str, Any]] = None
    ) -> ActivityLog:
        """Log user activity."""
        activity = ActivityLog(
            user_id=user_id,
            activity_type=activity_type,
            description=description,
            module=module,
            entity_id=entity_id,
            activity_metadata=activity_metadata
        )
        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        return activity
    
    def log_login(
        self,
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        login_status: str = "success",
        failure_reason: Optional[str] = None
    ) -> LoginHistory:
        """Log user login."""
        login = LoginHistory(
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            login_status=login_status,
            failure_reason=failure_reason
        )
        self.db.add(login)
        self.db.commit()
        self.db.refresh(login)
        return login
    
    def log_logout(self, user_id: int, session_id: str):
        """Log user logout."""
        login = self.db.query(LoginHistory).filter(
            and_(
                LoginHistory.user_id == user_id,
                LoginHistory.session_id == session_id,
                LoginHistory.logout_time.is_(None)
            )
        ).first()
        
        if login:
            login.logout_time = datetime.utcnow()
            self.db.commit()
    
    def log_system_event(
        self,
        log_level: str,
        module: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        stack_trace: Optional[str] = None,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None
    ) -> SystemLog:
        """Log system events."""
        system_log = SystemLog(
            log_level=log_level,
            module=module,
            message=message,
            details=details,
            stack_trace=stack_trace,
            user_id=user_id,
            ip_address=ip_address
        )
        self.db.add(system_log)
        self.db.commit()
        self.db.refresh(system_log)
        return system_log
    
    def log_performance(
        self,
        endpoint: str,
        method: str,
        response_time_ms: float,
        status_code: int,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        request_size: Optional[int] = None,
        response_size: Optional[int] = None
    ) -> PerformanceLog:
        """Log API performance metrics."""
        performance = PerformanceLog(
            endpoint=endpoint,
            method=method,
            response_time_ms=response_time_ms,
            status_code=status_code,
            user_id=user_id,
            ip_address=ip_address,
            request_size=request_size,
            response_size=response_size
        )
        self.db.add(performance)
        self.db.commit()
        self.db.refresh(performance)
        return performance
    
    def get_audit_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get audit summary for dashboard."""
        query = self.db.query(AuditLog)
        
        if start_date:
            query = query.filter(AuditLog.timestamp >= start_date)
        
        if end_date:
            query = query.filter(AuditLog.timestamp <= end_date)
        
        total_actions = query.count()
        
        # Actions by type
        actions_by_type = {}
        for action_type in ActionType:
            count = query.filter(AuditLog.action_type == action_type).count()
            actions_by_type[action_type.value] = count
        
        # Actions by module
        actions_by_module = {}
        for module_type in ModuleType:
            count = query.filter(AuditLog.module_type == module_type).count()
            actions_by_module[module_type.value] = count
        
        # Actions by user
        actions_by_user = {}
        user_actions = self.db.query(
            AuditLog.user_id,
            func.count(AuditLog.id).label('count')
        ).group_by(AuditLog.user_id).all()
        
        for user_id, count in user_actions:
            actions_by_user[f"User {user_id}"] = count
        
        # Recent activities
        recent_activities = query.order_by(desc(AuditLog.timestamp)).limit(10).all()
        recent_activities_data = [
            {
                "timestamp": activity.timestamp.isoformat(),
                "user": f"User {activity.user_id}" if activity.user_id else "Unknown",
                "action": activity.action_type.value,
                "module": activity.module_type.value,
                "description": activity.description
            }
            for activity in recent_activities
        ]
        
        # Top active users
        top_active_users = self.db.query(
            AuditLog.user_id,
            func.count(AuditLog.id).label('count')
        ).group_by(AuditLog.user_id).order_by(desc('count')).limit(5).all()
        
        top_active_users_data = [
            {
                "user": f"User {user_id}",
                "actions": count
            }
            for user_id, count in top_active_users
        ]
        
        return {
            "total_actions": total_actions,
            "actions_by_type": actions_by_type,
            "actions_by_module": actions_by_module,
            "actions_by_user": actions_by_user,
            "recent_activities": recent_activities_data,
            "top_active_users": top_active_users_data
        }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system metrics for dashboard."""
        # Total logins
        total_logins = self.db.query(LoginHistory).count()
        
        # Failed logins
        failed_logins = self.db.query(LoginHistory).filter(
            LoginHistory.login_status == "failed"
        ).count()
        
        # Average response time
        avg_response_time = self.db.query(
            func.avg(PerformanceLog.response_time_ms)
        ).scalar() or 0
        
        # Error rate
        total_requests = self.db.query(PerformanceLog).count()
        error_requests = self.db.query(PerformanceLog).filter(
            PerformanceLog.status_code >= 400
        ).count()
        error_rate = (error_requests / total_requests * 100) if total_requests > 0 else 0
        
        # Active sessions
        active_sessions = self.db.query(LoginHistory).filter(
            LoginHistory.logout_time.is_(None)
        ).count()
        
        return {
            "total_logins": total_logins,
            "failed_logins": failed_logins,
            "average_response_time": float(avg_response_time),
            "error_rate": float(error_rate),
            "active_sessions": active_sessions,
            "system_uptime": "24h 15m",  # Would calculate from system start time
            "database_size": "2.3 GB",  # Would calculate from database
            "memory_usage": "45%"  # Would get from system metrics
        }
    
    def get_report_metrics(self) -> Dict[str, Any]:
        """Get report metrics for dashboard."""
        # Total reports
        total_reports = self.db.query(Report).count()
        
        # Scheduled reports
        scheduled_reports = self.db.query(Report).filter(
            Report.schedule.isnot(None)
        ).count()
        
        # Executed today
        today = datetime.utcnow().date()
        executed_today = self.db.query(ReportExecution).filter(
            func.date(ReportExecution.execution_date) == today
        ).count()
        
        # Failed executions
        failed_executions = self.db.query(ReportExecution).filter(
            ReportExecution.status == "failed"
        ).count()
        
        # Average execution time
        avg_execution_time = self.db.query(
            func.avg(ReportExecution.execution_time_seconds)
        ).scalar() or 0
        
        # Most used reports
        most_used_reports = self.db.query(
            Report.report_name,
            func.count(ReportExecution.id).label('count')
        ).join(ReportExecution).group_by(Report.id).order_by(desc('count')).limit(5).all()
        
        most_used_reports_data = [
            {"report_name": report_name, "executions": count}
            for report_name, count in most_used_reports
        ]
        
        return {
            "total_reports": total_reports,
            "scheduled_reports": scheduled_reports,
            "executed_today": executed_today,
            "failed_executions": failed_executions,
            "average_execution_time": float(avg_execution_time),
            "most_used_reports": most_used_reports_data
        }
    
    def get_audit_trail(
        self,
        entity_type: str,
        entity_id: int,
        limit: int = 50
    ) -> List[AuditLog]:
        """Get complete audit trail for an entity."""
        return self.db.query(AuditLog).filter(
            and_(
                AuditLog.entity_type == entity_type,
                AuditLog.entity_id == entity_id
            )
        ).order_by(desc(AuditLog.timestamp)).limit(limit).all()
    
    def get_user_activity(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[AuditLog]:
        """Get user activity log."""
        query = self.db.query(AuditLog).filter(AuditLog.user_id == user_id)
        
        if start_date:
            query = query.filter(AuditLog.timestamp >= start_date)
        
        if end_date:
            query = query.filter(AuditLog.timestamp <= end_date)
        
        return query.order_by(desc(AuditLog.timestamp)).limit(limit).all()
    
    def search_audit_logs(
        self,
        search_term: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        action_type: Optional[ActionType] = None,
        module_type: Optional[ModuleType] = None,
        user_id: Optional[int] = None,
        limit: int = 100
    ) -> List[AuditLog]:
        """Search audit logs."""
        query = self.db.query(AuditLog)
        
        if search_term:
            query = query.filter(
                or_(
                    AuditLog.description.ilike(f"%{search_term}%"),
                    AuditLog.entity_type.ilike(f"%{search_term}%")
                )
            )
        
        if start_date:
            query = query.filter(AuditLog.timestamp >= start_date)
        
        if end_date:
            query = query.filter(AuditLog.timestamp <= end_date)
        
        if action_type:
            query = query.filter(AuditLog.action_type == action_type)
        
        if module_type:
            query = query.filter(AuditLog.module_type == module_type)
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        
        return query.order_by(desc(AuditLog.timestamp)).limit(limit).all()
