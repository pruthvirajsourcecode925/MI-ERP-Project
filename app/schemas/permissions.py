from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.permissions import PermissionType, ModuleType


class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    module: ModuleType
    permission_type: PermissionType


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    module: Optional[ModuleType] = None
    permission_type: Optional[PermissionType] = None


class PermissionResponse(PermissionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int
    expires_at: Optional[datetime] = None
    is_active: bool = True


class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionUpdate(BaseModel):
    role_id: Optional[int] = None
    permission_id: Optional[int] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None


class RolePermissionResponse(RolePermissionBase):
    id: int
    granted_by: Optional[int] = None
    granted_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserPermissionBase(BaseModel):
    user_id: int
    permission_id: int
    expires_at: Optional[datetime] = None
    is_active: bool = True


class UserPermissionCreate(UserPermissionBase):
    pass


class UserPermissionUpdate(BaseModel):
    user_id: Optional[int] = None
    permission_id: Optional[int] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None


class UserPermissionResponse(UserPermissionBase):
    id: int
    granted_by: Optional[int] = None
    granted_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class PermissionAuditBase(BaseModel):
    user_id: int
    permission_id: int
    action: str
    granted_by: Optional[int] = None
    reason: Optional[str] = None


class PermissionAuditCreate(PermissionAuditBase):
    pass


class PermissionAuditResponse(PermissionAuditBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# List response schemas
class PermissionList(BaseModel):
    permissions: List[PermissionResponse]
    total: int
    page: int
    size: int


class RolePermissionList(BaseModel):
    role_permissions: List[RolePermissionResponse]
    total: int
    page: int
    size: int


class UserPermissionList(BaseModel):
    user_permissions: List[UserPermissionResponse]
    total: int
    page: int
    size: int


class PermissionAuditList(BaseModel):
    audits: List[PermissionAuditResponse]
    total: int
    page: int
    size: int


# Permission check response
class PermissionCheckResponse(BaseModel):
    has_permission: bool
    permission: Optional[str] = None
    module: Optional[str] = None
    expires_at: Optional[datetime] = None


class UserPermissionsResponse(BaseModel):
    user_id: int
    permissions: List[dict]  # List of {module: [permissions]}
    role_permissions: List[dict]  # List of {module: [permissions]}
    effective_permissions: List[dict]  # Combined permissions
