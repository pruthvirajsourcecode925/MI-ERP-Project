from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from app.models.production import JobStatus, OperationStatus


class JobCardBase(BaseModel):
    customer_po: Optional[str] = None
    part_number: str
    drawing_number: str
    revision: str
    quantity: int
    route_card_id: Optional[int] = None
    planned_start_date: date
    planned_completion_date: date
    priority: str = "normal"
    special_instructions: Optional[str] = None
    status: JobStatus = JobStatus.PENDING


class JobCardCreate(JobCardBase):
    pass


class JobCardUpdate(BaseModel):
    customer_po: Optional[str] = None
    part_number: Optional[str] = None
    drawing_number: Optional[str] = None
    revision: Optional[str] = None
    quantity: Optional[int] = None
    route_card_id: Optional[int] = None
    planned_start_date: Optional[date] = None
    planned_completion_date: Optional[date] = None
    priority: Optional[str] = None
    special_instructions: Optional[str] = None
    status: Optional[JobStatus] = None


class JobCardResponse(JobCardBase):
    id: int
    job_card_number: str
    actual_start_date: Optional[datetime] = None
    actual_completion_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


class JobCardOperationBase(BaseModel):
    operation_number: int
    operation_description: str
    machine_id: Optional[int] = None
    operator_id: Optional[int] = None
    planned_time: int  # minutes
    actual_time: Optional[int] = None  # minutes
    quantity_planned: int
    quantity_produced: Optional[int] = None
    quantity_rejected: Optional[int] = None
    status: OperationStatus = OperationStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    remarks: Optional[str] = None


class JobCardOperationCreate(JobCardOperationBase):
    job_card_id: int


class JobCardOperationUpdate(BaseModel):
    operation_number: Optional[int] = None
    operation_description: Optional[str] = None
    machine_id: Optional[int] = None
    operator_id: Optional[int] = None
    planned_time: Optional[int] = None
    actual_time: Optional[int] = None
    quantity_planned: Optional[int] = None
    quantity_produced: Optional[int] = None
    quantity_rejected: Optional[int] = None
    status: Optional[OperationStatus] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    remarks: Optional[str] = None


class JobCardOperationResponse(JobCardOperationBase):
    id: int
    job_card_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class MachineBase(BaseModel):
    machine_code: str
    machine_name: str
    machine_type: str
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    capacity: Optional[str] = None
    location: str
    status: str = "active"
    installation_date: Optional[date] = None


class MachineCreate(MachineBase):
    pass


class MachineUpdate(BaseModel):
    machine_code: Optional[str] = None
    machine_name: Optional[str] = None
    machine_type: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    capacity: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    installation_date: Optional[date] = None


class MachineResponse(MachineBase):
    id: int
    machine_code: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


class ProductionLogBase(BaseModel):
    log_date: date
    shift: str  # Morning, Evening, Night
    job_card_id: Optional[int] = None
    machine_id: Optional[int] = None
    operator_id: Optional[int] = None
    production_hours: int  # in minutes
    downtime_hours: int  # in minutes
    quantity_produced: int
    quantity_rejected: int
    efficiency: Optional[Decimal] = None
    remarks: Optional[str] = None


class ProductionLogCreate(ProductionLogBase):
    pass


class ProductionLogResponse(ProductionLogBase):
    id: int
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True


class FAITriggerBase(BaseModel):
    trigger_reason: str
    trigger_date: datetime
    description: str
    status: str = "pending"
    fai_report_id: Optional[int] = None


class FAITriggerCreate(FAITriggerBase):
    job_card_id: int


class FAITriggerUpdate(BaseModel):
    trigger_reason: Optional[str] = None
    trigger_date: Optional[datetime] = None
    description: Optional[str] = None
    status: Optional[str] = None
    fai_report_id: Optional[int] = None


class FAITriggerResponse(FAITriggerBase):
    id: int
    trigger_number: str
    job_card_id: int
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True


class ReworkRecordBase(BaseModel):
    rework_reason: str
    quantity_reworked: int
    rework_time: int  # minutes
    rework_cost: Optional[Decimal] = None
    completion_date: Optional[datetime] = None
    status: str = "pending"


class ReworkRecordCreate(ReworkRecordBase):
    job_card_id: int
    operation_id: int


class ReworkRecordUpdate(BaseModel):
    rework_reason: Optional[str] = None
    quantity_reworked: Optional[int] = None
    rework_time: Optional[int] = None
    rework_cost: Optional[Decimal] = None
    completion_date: Optional[datetime] = None
    status: Optional[str] = None


class ReworkRecordResponse(ReworkRecordBase):
    id: int
    rework_number: str
    job_card_id: int
    operation_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


# List response schemas
class JobCardList(BaseModel):
    job_cards: List[JobCardResponse]
    total: int
    page: int
    size: int


class JobCardOperationList(BaseModel):
    operations: List[JobCardOperationResponse]
    total: int
    page: int
    size: int


class MachineList(BaseModel):
    machines: List[MachineResponse]
    total: int
    page: int
    size: int


class ProductionLogList(BaseModel):
    logs: List[ProductionLogResponse]
    total: int
    page: int
    size: int


class FAITriggerList(BaseModel):
    triggers: List[FAITriggerResponse]
    total: int
    page: int
    size: int


class ReworkRecordList(BaseModel):
    rework_records: List[ReworkRecordResponse]
    total: int
    page: int
    size: int
