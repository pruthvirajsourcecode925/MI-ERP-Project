from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from app.models.stores import InspectionStatus, MaterialStatus


class RawMaterialInwardBase(BaseModel):
    po_id: Optional[int] = None
    supplier_id: int
    material_description: str
    part_number: Optional[str] = None
    drawing_number: Optional[str] = None
    heat_number: Optional[str] = None
    batch_number: Optional[str] = None
    quantity_received: int
    quantity_accepted: Optional[int] = None
    quantity_rejected: Optional[int] = None
    inspection_status: InspectionStatus = InspectionStatus.PENDING
    material_status: MaterialStatus = MaterialStatus.PENDING
    inward_date: datetime


class RawMaterialInwardCreate(RawMaterialInwardBase):
    pass


class RawMaterialInwardUpdate(BaseModel):
    po_id: Optional[int] = None
    supplier_id: Optional[int] = None
    material_description: Optional[str] = None
    part_number: Optional[str] = None
    drawing_number: Optional[str] = None
    heat_number: Optional[str] = None
    batch_number: Optional[str] = None
    quantity_received: Optional[int] = None
    quantity_accepted: Optional[int] = None
    quantity_rejected: Optional[int] = None
    inspection_status: Optional[InspectionStatus] = None
    material_status: Optional[MaterialStatus] = None


class RawMaterialInwardResponse(RawMaterialInwardBase):
    id: int
    inward_number: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    inspected_by: Optional[int] = None
    created_by: int
    
    class Config:
        from_attributes = True


class MTCVerificationBase(BaseModel):
    inward_id: int
    mtc_number: str
    mtc_date: date
    chemical_composition_ok: bool = False
    mechanical_properties_ok: bool = False
    dimensions_ok: bool = False
    surface_finish_ok: bool = False
    other_tests_ok: bool = False
    verification_status: str = "pending"
    remarks: Optional[str] = None


class MTCVerificationCreate(MTCVerificationBase):
    pass


class MTCVerificationUpdate(BaseModel):
    mtc_number: Optional[str] = None
    mtc_date: Optional[date] = None
    chemical_composition_ok: Optional[bool] = None
    mechanical_properties_ok: Optional[bool] = None
    dimensions_ok: Optional[bool] = None
    surface_finish_ok: Optional[bool] = None
    other_tests_ok: Optional[bool] = None
    verification_status: Optional[str] = None
    remarks: Optional[str] = None


class MTCVerificationResponse(MTCVerificationBase):
    id: int
    inward_id: int
    verified_by: int
    verification_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class TraceabilityRecordBase(BaseModel):
    record_number: str
    part_number: str
    drawing_number: str
    heat_number: str
    batch_number: str
    customer_po: Optional[str] = None
    customer_name: Optional[str] = None
    quantity: int
    inward_date: datetime
    process_start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    status: str = "active"


class TraceabilityRecordCreate(TraceabilityRecordBase):
    pass


class TraceabilityRecordUpdate(BaseModel):
    record_number: Optional[str] = None
    part_number: Optional[str] = None
    drawing_number: Optional[str] = None
    heat_number: Optional[str] = None
    batch_number: Optional[str] = None
    customer_po: Optional[str] = None
    customer_name: Optional[str] = None
    quantity: Optional[int] = None
    inward_date: Optional[datetime] = None
    process_start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    status: Optional[str] = None


class TraceabilityRecordResponse(TraceabilityRecordBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


class StockRegisterBase(BaseModel):
    material_code: str
    material_description: str
    heat_number: Optional[str] = None
    batch_number: Optional[str] = None
    location: str
    bin_location: Optional[str] = None
    quantity: int
    unit: str
    minimum_stock: Optional[int] = None
    maximum_stock: Optional[int] = None
    reorder_level: Optional[int] = None


class StockRegisterCreate(StockRegisterBase):
    pass


class StockRegisterUpdate(BaseModel):
    material_code: Optional[str] = None
    material_description: Optional[str] = None
    heat_number: Optional[str] = None
    batch_number: Optional[str] = None
    location: Optional[str] = None
    bin_location: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None
    minimum_stock: Optional[int] = None
    maximum_stock: Optional[int] = None
    reorder_level: Optional[int] = None


class StockRegisterResponse(StockRegisterBase):
    id: int
    last_updated: Optional[datetime] = None
    updated_by: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ShelfLifeControlBase(BaseModel):
    material_code: str
    batch_number: str
    material_description: str
    manufacture_date: date
    expiry_date: date
    quantity: int
    location: str
    status: str = "active"
    notification_sent: bool = False


class ShelfLifeControlCreate(ShelfLifeControlBase):
    pass


class ShelfLifeControlUpdate(BaseModel):
    material_code: Optional[str] = None
    batch_number: Optional[str] = None
    material_description: Optional[str] = None
    manufacture_date: Optional[date] = None
    expiry_date: Optional[date] = None
    quantity: Optional[int] = None
    location: Optional[str] = None
    status: Optional[str] = None
    notification_sent: Optional[bool] = None


class ShelfLifeControlResponse(ShelfLifeControlBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


class IdentificationTagBase(BaseModel):
    tag_number: str
    part_number: str
    drawing_number: str
    heat_number: str
    batch_number: str
    quantity: int
    status: str = "active"


class IdentificationTagCreate(IdentificationTagBase):
    pass


class IdentificationTagUpdate(BaseModel):
    tag_number: Optional[str] = None
    part_number: Optional[str] = None
    drawing_number: Optional[str] = None
    heat_number: Optional[str] = None
    batch_number: Optional[str] = None
    quantity: Optional[int] = None
    status: Optional[str] = None


class IdentificationTagResponse(IdentificationTagBase):
    id: int
    issue_date: datetime
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True


# List response schemas
class RawMaterialInwardList(BaseModel):
    inwards: List[RawMaterialInwardResponse]
    total: int
    page: int
    size: int


class MTCVerificationList(BaseModel):
    verifications: List[MTCVerificationResponse]
    total: int
    page: int
    size: int


class TraceabilityRecordList(BaseModel):
    records: List[TraceabilityRecordResponse]
    total: int
    page: int
    size: int


class StockRegisterList(BaseModel):
    stock_registers: List[StockRegisterResponse]
    total: int
    page: int
    size: int


class ShelfLifeControlList(BaseModel):
    shelf_life_controls: List[ShelfLifeControlResponse]
    total: int
    page: int
    size: int


class IdentificationTagList(BaseModel):
    identification_tags: List[IdentificationTagResponse]
    total: int
    page: int
    size: int
