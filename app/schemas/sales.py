from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from enum import Enum

class EnquiryStatus(str, Enum):
    NEW = "new"
    UNDER_REVIEW = "under_review"
    QUOTED = "quoted"
    CONVERTED = "converted"
    CLOSED = "closed"

class CustomerEnquiryBase(BaseModel):
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    part_number: str
    drawing_number: str
    revision: Optional[str] = None
    quantity: int
    target_price: Optional[Decimal] = None
    delivery_date: Optional[date] = None
    special_requirements: Optional[str] = None
    drawing_available: bool = False
    special_processes: Optional[str] = None
    capacity_feasible: bool = True
    delivery_feasible: bool = True
    quality_requirements: Optional[str] = None
    status: EnquiryStatus = EnquiryStatus.NEW


class CustomerEnquiryCreate(CustomerEnquiryBase):
    pass


class CustomerEnquiryUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    part_number: Optional[str] = None
    drawing_number: Optional[str] = None
    revision: Optional[str] = None
    quantity: Optional[int] = None
    target_price: Optional[Decimal] = None
    delivery_date: Optional[date] = None
    special_requirements: Optional[str] = None
    drawing_available: Optional[bool] = None
    special_processes: Optional[str] = None
    capacity_feasible: Optional[bool] = None
    delivery_feasible: Optional[bool] = None
    quality_requirements: Optional[str] = None
    status: Optional[EnquiryStatus] = None


class CustomerEnquiryResponse(BaseModel):
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    part_number: str
    drawing_number: str
    revision: Optional[str] = None
    quantity: int
    target_price: Optional[Decimal] = None
    delivery_date: Optional[date] = None
    special_requirements: Optional[str] = None
    drawing_available: bool = False
    special_processes: Optional[str] = None
    capacity_feasible: bool = True
    delivery_feasible: bool = True
    quality_requirements: Optional[str] = None
    status: Optional[EnquiryStatus] = None
    id: int
    enquiry_number: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int


class QuotationBase(BaseModel):
    quoted_price: Decimal
    quoted_delivery: date
    terms_and_conditions: Optional[str] = None
    validity_date: date
    status: str = "draft"


class QuotationCreate(QuotationBase):
    enquiry_id: int


class QuotationUpdate(BaseModel):
    quoted_price: Optional[Decimal] = None
    quoted_delivery: Optional[date] = None
    terms_and_conditions: Optional[str] = None
    validity_date: Optional[date] = None
    status: Optional[str] = None


class QuotationResponse(BaseModel):
    quoted_price: Decimal
    quoted_delivery: date
    terms_and_conditions: Optional[str] = None
    validity_date: date
    status: str = "draft"
    id: int
    quotation_number: str
    enquiry_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int


class ContractReviewBase(BaseModel):
    review_date: datetime
    drawing_availability: bool
    special_processes_review: Optional[str] = None
    capacity_suitability: bool
    delivery_feasibility: bool
    quality_requirements_review: Optional[str] = None
    risk_assessment: Optional[str] = None
    approved: bool = False
    approval_comments: Optional[str] = None


class ContractReviewCreate(ContractReviewBase):
    enquiry_id: int


class ContractReviewUpdate(BaseModel):
    drawing_availability: Optional[bool] = None
    special_processes_review: Optional[str] = None
    capacity_suitability: Optional[bool] = None
    delivery_feasibility: Optional[bool] = None
    quality_requirements_review: Optional[str] = None
    risk_assessment: Optional[str] = None
    approved: Optional[bool] = None
    approval_comments: Optional[str] = None


class ContractReviewResponse(ContractReviewBase):
    id: int
    review_number: str
    enquiry_id: int
    created_at: datetime
    reviewed_by: int
    
    class Config:
        from_attributes = True


class CustomerPurchaseOrderBase(BaseModel):
    customer_name: str
    customer_po_number: str
    order_date: date
    delivery_date: date
    total_value: Decimal
    terms_and_conditions: Optional[str] = None
    status: str = "active"


class CustomerPurchaseOrderCreate(CustomerPurchaseOrderBase):
    enquiry_id: Optional[int] = None
    quotation_id: Optional[int] = None


class CustomerPurchaseOrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_po_number: Optional[str] = None
    order_date: Optional[date] = None
    delivery_date: Optional[date] = None
    total_value: Optional[Decimal] = None
    terms_and_conditions: Optional[str] = None
    status: Optional[str] = None


class CustomerPurchaseOrderResponse(CustomerPurchaseOrderBase):
    id: int
    po_number: str
    enquiry_id: Optional[int] = None
    quotation_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


# List response schemas
class CustomerEnquiryList(BaseModel):
    enquiries: List[CustomerEnquiryResponse]
    total: int
    page: int
    size: int


class QuotationList(BaseModel):
    quotations: List[QuotationResponse]
    total: int
    page: int
    size: int


class ContractReviewList(BaseModel):
    reviews: List[ContractReviewResponse]
    total: int
    page: int
    size: int


class CustomerPurchaseOrderList(BaseModel):
    orders: List[CustomerPurchaseOrderResponse]
    total: int
    page: int
    size: int
