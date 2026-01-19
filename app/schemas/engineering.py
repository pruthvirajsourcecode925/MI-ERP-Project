from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from app.models.engineering import DrawingStatus


class DrawingBase(BaseModel):
    drawing_number: str
    revision: str
    title: str
    customer: Optional[str] = None
    status: DrawingStatus = DrawingStatus.DRAFT
    issue_date: Optional[datetime] = None
    effective_date: Optional[datetime] = None


class DrawingCreate(DrawingBase):
    pass


class DrawingUpdate(BaseModel):
    drawing_number: Optional[str] = None
    revision: Optional[str] = None
    title: Optional[str] = None
    customer: Optional[str] = None
    status: Optional[DrawingStatus] = None
    issue_date: Optional[datetime] = None
    effective_date: Optional[datetime] = None


class DrawingResponse(DrawingBase):
    id: int
    drawing_number: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


class RouteCardBase(BaseModel):
    route_card_number: str
    part_number: str
    revision: str
    quantity: int
    status: str = "active"


class RouteCardCreate(RouteCardBase):
    drawing_id: int


class RouteCardUpdate(BaseModel):
    route_card_number: Optional[str] = None
    part_number: Optional[str] = None
    revision: Optional[str] = None
    quantity: Optional[int] = None
    status: Optional[str] = None


class RouteCardResponse(RouteCardBase):
    id: int
    route_card_number: str
    drawing_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


class ProcessOperationBase(BaseModel):
    operation_number: int
    operation_description: str
    machine_required: Optional[str] = None
    tooling_required: Optional[str] = None
    setup_time: int = 0
    run_time: int
    inspection_required: bool = True
    special_process: bool = False
    process_type: Optional[str] = None
    sequence: int


class ProcessOperationCreate(ProcessOperationBase):
    route_card_id: int


class ProcessOperationUpdate(BaseModel):
    operation_number: Optional[int] = None
    operation_description: Optional[str] = None
    machine_required: Optional[str] = None
    tooling_required: Optional[str] = None
    setup_time: Optional[int] = None
    run_time: Optional[int] = None
    inspection_required: Optional[bool] = None
    special_process: Optional[bool] = None
    process_type: Optional[str] = None
    sequence: Optional[int] = None


class ProcessOperationResponse(ProcessOperationBase):
    id: int
    route_card_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ControlPlanBase(BaseModel):
    plan_number: str
    part_number: str
    drawing_revision: str
    revision_date: Optional[datetime] = None
    approval_date: Optional[datetime] = None
    status: str = "draft"


class ControlPlanCreate(ControlPlanBase):
    pass


class ControlPlanUpdate(BaseModel):
    plan_number: Optional[str] = None
    part_number: Optional[str] = None
    drawing_revision: Optional[str] = None
    revision_date: Optional[datetime] = None
    approval_date: Optional[datetime] = None
    status: Optional[str] = None


class ControlPlanResponse(ControlPlanBase):
    id: int
    plan_number: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


class ControlCharacteristicBase(BaseModel):
    characteristic_number: int
    description: str
    specification: str
    tolerance: Optional[str] = None
    measurement_method: Optional[str] = None
    sample_size: int
    sample_frequency: Optional[str] = None
    control_method: Optional[str] = None
    reaction_plan: Optional[str] = None


class ControlCharacteristicCreate(ControlCharacteristicBase):
    control_plan_id: int


class ControlCharacteristicResponse(ControlCharacteristicBase):
    id: int
    control_plan_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ToolingBase(BaseModel):
    tool_number: str
    tool_description: str
    tool_type: str  # Die, Fixture, Gauge, etc.
    part_number: Optional[str] = None
    drawing_number: Optional[str] = None
    status: str = "active"
    location: Optional[str] = None
    maintenance_due: Optional[datetime] = None


class ToolingCreate(ToolingBase):
    pass


class ToolingUpdate(BaseModel):
    tool_number: Optional[str] = None
    tool_description: Optional[str] = None
    tool_type: Optional[str] = None
    part_number: Optional[str] = None
    drawing_number: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None
    maintenance_due: Optional[datetime] = None


class ToolingResponse(ToolingBase):
    id: int
    tool_number: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


# List response schemas
class DrawingList(BaseModel):
    drawings: List[DrawingResponse]
    total: int
    page: int
    size: int


class RouteCardList(BaseModel):
    route_cards: List[RouteCardResponse]
    total: int
    page: int
    size: int


class ProcessOperationList(BaseModel):
    operations: List[ProcessOperationResponse]
    total: int
    page: int
    size: int


class ControlPlanList(BaseModel):
    control_plans: List[ControlPlanResponse]
    total: int
    page: int
    size: int


class ToolingList(BaseModel):
    tooling: List[ToolingResponse]
    total: int
    page: int
    size: int
