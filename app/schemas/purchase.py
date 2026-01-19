from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from app.models.purchase import SupplierStatus, EvaluationStatus


class SupplierBase(BaseModel):
    supplier_code: str
    supplier_name: str
    address: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    gst_number: Optional[str] = None
    pan_number: Optional[str] = None
    payment_terms: Optional[str] = None
    status: SupplierStatus = SupplierStatus.PENDING


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    supplier_code: Optional[str] = None
    supplier_name: Optional[str] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    gst_number: Optional[str] = None
    pan_number: Optional[str] = None
    payment_terms: Optional[str] = None
    status: Optional[SupplierStatus] = None


class SupplierResponse(SupplierBase):
    id: int
    supplier_code: str
    approved_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


class SupplierEvaluationBase(BaseModel):
    evaluation_number: str
    supplier_id: int
    evaluation_date: datetime
    evaluation_type: str  # Initial, Re-evaluation
    quality_score: int  # 1-100
    delivery_score: int  # 1-100
    price_score: int  # 1-100
    service_score: int  # 1-100
    overall_score: int  # 1-100
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    recommendations: Optional[str] = None
    next_evaluation_date: Optional[date] = None
    status: EvaluationStatus = EvaluationStatus.NEW


class SupplierEvaluationCreate(SupplierEvaluationBase):
    pass


class SupplierEvaluationUpdate(BaseModel):
    evaluation_type: Optional[str] = None
    quality_score: Optional[int] = None
    delivery_score: Optional[int] = None
    price_score: Optional[int] = None
    service_score: Optional[int] = None
    overall_score: Optional[int] = None
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    recommendations: Optional[str] = None
    next_evaluation_date: Optional[date] = None
    status: Optional[EvaluationStatus] = None


class SupplierEvaluationResponse(SupplierEvaluationBase):
    id: int
    evaluation_number: str
    supplier_id: int
    approved_by: Optional[int] = None
    evaluated_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PurchaseOrderItemBase(BaseModel):
    item_number: int
    material_description: str
    part_number: Optional[str] = None
    drawing_number: Optional[str] = None
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    delivery_date: Optional[date] = None
    specifications: Optional[str] = None


class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    po_id: int


class PurchaseOrderItemResponse(PurchaseOrderItemBase):
    id: int
    po_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class PurchaseOrderBase(BaseModel):
    supplier_id: int
    order_date: date
    delivery_date: date
    total_value: Decimal
    status: str = "pending"
    terms_and_conditions: Optional[str] = None
    quality_clauses: Optional[str] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    items: List[PurchaseOrderItemCreate]


class PurchaseOrderUpdate(BaseModel):
    supplier_id: Optional[int] = None
    order_date: Optional[date] = None
    delivery_date: Optional[date] = None
    total_value: Optional[Decimal] = None
    status: Optional[str] = None
    terms_and_conditions: Optional[str] = None
    quality_clauses: Optional[str] = None


class PurchaseOrderResponse(PurchaseOrderBase):
    id: int
    po_number: str
    supplier_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


class SubcontractingOrderBase(BaseModel):
    supplier_id: int
    process_type: str  # HT, Plating, NDT, etc.
    part_number: str
    drawing_number: str
    quantity: int
    special_instructions: Optional[str] = None
    order_date: date
    delivery_date: date
    status: str = "pending"


class SubcontractingOrderCreate(SubcontractingOrderBase):
    pass


class SubcontractingOrderUpdate(BaseModel):
    supplier_id: Optional[int] = None
    process_type: Optional[str] = None
    part_number: Optional[str] = None
    drawing_number: Optional[str] = None
    quantity: Optional[int] = None
    special_instructions: Optional[str] = None
    order_date: Optional[date] = None
    delivery_date: Optional[date] = None
    status: Optional[str] = None


class SubcontractingOrderResponse(SubcontractingOrderBase):
    id: int
    order_number: str
    supplier_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


class SupplierNCRBase(BaseModel):
    supplier_id: int
    po_id: Optional[int] = None
    material_description: str
    quantity_rejected: int
    rejection_reason: str
    rejection_date: datetime
    action_required: Optional[str] = None
    status: str = "open"


class SupplierNCRCreate(SupplierNCRBase):
    pass


class SupplierNCRUpdate(BaseModel):
    supplier_id: Optional[int] = None
    po_id: Optional[int] = None
    material_description: Optional[str] = None
    quantity_rejected: Optional[int] = None
    rejection_reason: Optional[str] = None
    action_required: Optional[str] = None
    status: Optional[str] = None


class SupplierNCRResponse(SupplierNCRBase):
    id: int
    ncr_number: str
    supplier_id: int
    purchase_order: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


# List response schemas
class SupplierList(BaseModel):
    suppliers: List[SupplierResponse]
    total: int
    page: int
    size: int


class SupplierEvaluationList(BaseModel):
    evaluations: List[SupplierEvaluationResponse]
    total: int
    page: int
    size: int


class PurchaseOrderList(BaseModel):
    orders: List[PurchaseOrderResponse]
    total: int
    page: int
    size: int


class SubcontractingOrderList(BaseModel):
    orders: List[SubcontractingOrderResponse]
    total: int
    page: int
    size: int


class SupplierNCRList(BaseModel):
    ncrs: List[SupplierNCRResponse]
    total: int
    page: int
    size: int
