from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base
from enum import Enum as PyEnum


class PermissionType(PyEnum):
    READ = "read"
    WRITE = "write"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    ADMIN = "admin"


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
    ADMIN = "admin"


class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    module = Column(Enum(ModuleType), nullable=False)
    permission_type = Column(Enum(PermissionType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class RolePermission(Base):
    __tablename__ = "role_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)
    granted_by = Column(Integer, nullable=True)
    granted_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    permission = relationship("Permission")


class UserPermission(Base):
    __tablename__ = "user_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)
    granted_by = Column(Integer, nullable=True)
    granted_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    permission = relationship("Permission")


class PermissionAudit(Base):
    __tablename__ = "permission_audits"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)
    action = Column(String(50), nullable=False)  # GRANTED, REVOKED, EXPIRED
    granted_by = Column(Integer, nullable=True)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    permission = relationship("Permission")