from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.database.database import get_db
from app.models.sales import CustomerEnquiry, Quotation, ContractReview, CustomerPurchaseOrder
from app.schemas.sales import (
    CustomerEnquiryCreate, CustomerEnquiryUpdate, CustomerEnquiryResponse,
    QuotationCreate, QuotationUpdate, QuotationResponse, QuotationList,
    ContractReviewCreate, ContractReviewUpdate, ContractReviewResponse, ContractReviewList,
    CustomerPurchaseOrderCreate, CustomerPurchaseOrderResponse, CustomerPurchaseOrderList,
    EnquiryStatus
)
import uuid
from datetime import datetime

router = APIRouter()


def generate_enquiry_number():
    """Generate unique enquiry number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"ENQ-{year}-{random_id}"


def generate_quotation_number():
    """Generate unique quotation number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"QUO-{year}-{random_id}"


def generate_review_number():
    """Generate unique contract review number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"CR-{year}-{random_id}"


def generate_po_number():
    """Generate unique purchase order number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"CPO-{year}-{random_id}"


# Customer Enquiry endpoints
@router.post("/enquiries/", response_model=dict)
def create_enquiry(
    enquiry: CustomerEnquiryCreate,
    db: Session = Depends(get_db)
):
    """Create a new customer enquiry."""
    try:
        enquiry_number = generate_enquiry_number()
        
        # Handle enum status properly
        status_value = enquiry.status.value if hasattr(enquiry.status, 'value') else enquiry.status
        
        db_enquiry = CustomerEnquiry(
            customer_name=enquiry.customer_name,
            customer_email=enquiry.customer_email,
            customer_phone=enquiry.customer_phone,
            customer_address=enquiry.customer_address,
            part_number=enquiry.part_number,
            drawing_number=enquiry.drawing_number,
            revision=enquiry.revision,
            quantity=enquiry.quantity,
            target_price=enquiry.target_price,
            delivery_date=enquiry.delivery_date,
            special_requirements=enquiry.special_requirements,
            drawing_available=enquiry.drawing_available,
            special_processes=enquiry.special_processes,
            capacity_feasible=enquiry.capacity_feasible,
            delivery_feasible=enquiry.delivery_feasible,
            quality_requirements=enquiry.quality_requirements,
            status=status_value,
            enquiry_number=enquiry_number,
            created_by=1  # Default user ID since auth is removed
        )
        db.add(db_enquiry)
        db.commit()
        db.refresh(db_enquiry)
        
        # Return simple response
        return {
            "id": db_enquiry.id,
            "enquiry_number": db_enquiry.enquiry_number,
            "customer_name": db_enquiry.customer_name,
            "part_number": db_enquiry.part_number,
            "status": str(db_enquiry.status.value) if db_enquiry.status else None,
            "created_at": db_enquiry.created_at.isoformat() if db_enquiry.created_at else None
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating enquiry: {str(e)}"
        )


@router.get("/enquiries/", response_model=dict)
def list_enquiries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    enquiry_status: Optional[EnquiryStatus] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List customer enquiries with filtering."""
    try:
        query = db.query(CustomerEnquiry)
        
        # Apply filters
        if enquiry_status:
            query = query.filter(CustomerEnquiry.status == enquiry_status)
        
        if search:
            search_filter = or_(
                CustomerEnquiry.customer_name.ilike(f"%{search}%"),
                CustomerEnquiry.part_number.ilike(f"%{search}%"),
                CustomerEnquiry.enquiry_number.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        enquiries = query.offset(skip).limit(limit).all()
        
        return {
            "total": total,
            "enquiries": [
                {
                    "id": enquiry.id,
                    "enquiry_number": enquiry.enquiry_number,
                    "customer_name": enquiry.customer_name,
                    "part_number": enquiry.part_number,
                    "quantity": enquiry.quantity,
                    "status": str(enquiry.status.value) if enquiry.status else None,
                    "created_at": enquiry.created_at.isoformat() if enquiry.created_at else None
                }
                for enquiry in enquiries
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing enquiries: {str(e)}"
        )


@router.get("/enquiries/{enquiry_id}", response_model=dict)
def get_enquiry(
    enquiry_id: int,
    db: Session = Depends(get_db)
):
    """Get specific customer enquiry."""
    enquiry = db.query(CustomerEnquiry).filter(CustomerEnquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enquiry not found"
        )
    
    return {
        "id": enquiry.id,
        "enquiry_number": enquiry.enquiry_number,
        "customer_name": enquiry.customer_name,
        "customer_email": enquiry.customer_email,
        "customer_phone": enquiry.customer_phone,
        "customer_address": enquiry.customer_address,
        "part_number": enquiry.part_number,
        "drawing_number": enquiry.drawing_number,
        "revision": enquiry.revision,
        "quantity": enquiry.quantity,
        "target_price": enquiry.target_price,
        "delivery_date": enquiry.delivery_date.isoformat() if enquiry.delivery_date else None,
        "special_requirements": enquiry.special_requirements,
        "drawing_available": enquiry.drawing_available,
        "special_processes": enquiry.special_processes,
        "capacity_feasible": enquiry.capacity_feasible,
        "delivery_feasible": enquiry.delivery_feasible,
        "quality_requirements": enquiry.quality_requirements,
        "status": str(enquiry.status.value) if enquiry.status else None,
        "created_at": enquiry.created_at.isoformat() if enquiry.created_at else None
    }


@router.put("/enquiries/{enquiry_id}", response_model=dict)
def update_enquiry(
    enquiry_id: int,
    enquiry_update: CustomerEnquiryUpdate,
    db: Session = Depends(get_db)
):
    """Update customer enquiry."""
    enquiry = db.query(CustomerEnquiry).filter(CustomerEnquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enquiry not found"
        )
    
    try:
        # Update fields
        update_data = enquiry_update.dict(exclude_unset=True)
        
        # Handle enum status
        if 'status' in update_data:
            status_value = update_data['status'].value if hasattr(update_data['status'], 'value') else update_data['status']
            update_data['status'] = status_value
        
        for field, value in update_data.items():
            setattr(enquiry, field, value)
        
        db.commit()
        db.refresh(enquiry)
        
        return {
            "id": enquiry.id,
            "enquiry_number": enquiry.enquiry_number,
            "customer_name": enquiry.customer_name,
            "part_number": enquiry.part_number,
            "status": str(enquiry.status.value) if enquiry.status else None,
            "updated_at": enquiry.updated_at.isoformat() if enquiry.updated_at else None
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating enquiry: {str(e)}"
        )


@router.delete("/enquiries/{enquiry_id}", response_model=dict)
def delete_enquiry(
    enquiry_id: int,
    db: Session = Depends(get_db)
):
    """Delete customer enquiry."""
    enquiry = db.query(CustomerEnquiry).filter(CustomerEnquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enquiry not found"
        )
    
    try:
        db.delete(enquiry)
        db.commit()
        return {"message": "Enquiry deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting enquiry: {str(e)}"
        )


# Quotation endpoints
@router.post("/quotations/", response_model=dict)
def create_quotation(
    quotation: QuotationCreate,
    db: Session = Depends(get_db)
):
    """Create a new quotation."""
    try:
        quotation_number = generate_quotation_number()
        
        # Handle enum status properly
        status_value = quotation.status.value if hasattr(quotation.status, 'value') else quotation.status
        
        db_quotation = Quotation(
            enquiry_id=quotation.enquiry_id,
            quotation_number=quotation_number,
            quoted_price=quotation.quoted_price,
            delivery_terms=quotation.delivery_terms,
            payment_terms=quotation.payment_terms,
            validity_days=quotation.validity_days,
            special_conditions=quotation.special_conditions,
            status=status_value,
            created_by=1  # Default user ID since auth is removed
        )
        db.add(db_quotation)
        db.commit()
        db.refresh(db_quotation)
        
        return {
            "id": db_quotation.id,
            "quotation_number": db_quotation.quotation_number,
            "enquiry_id": db_quotation.enquiry_id,
            "quoted_price": db_quotation.quoted_price,
            "status": str(db_quotation.status.value) if db_quotation.status else None,
            "created_at": db_quotation.created_at.isoformat() if db_quotation.created_at else None
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating quotation: {str(e)}"
        )


@router.get("/quotations/", response_model=dict)
def list_quotations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List quotations with filtering."""
    try:
        query = db.query(Quotation)
        
        if search:
            search_filter = or_(
                Quotation.quotation_number.ilike(f"%{search}%"),
                Quotation.special_conditions.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        total = query.count()
        quotations = query.offset(skip).limit(limit).all()
        
        return {
            "total": total,
            "quotations": [
                {
                    "id": quot.id,
                    "quotation_number": quot.quotation_number,
                    "enquiry_id": quot.enquiry_id,
                    "quoted_price": quot.quoted_price,
                    "status": str(quot.status.value) if quot.status else None,
                    "created_at": quot.created_at.isoformat() if quot.created_at else None
                }
                for quot in quotations
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing quotations: {str(e)}"
        )


@router.get("/quotations/{quotation_id}", response_model=dict)
def get_quotation(
    quotation_id: int,
    db: Session = Depends(get_db)
):
    """Get specific quotation."""
    quotation = db.query(Quotation).filter(Quotation.id == quotation_id).first()
    if not quotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation not found"
        )
    
    return {
        "id": quotation.id,
        "quotation_number": quotation.quotation_number,
        "enquiry_id": quotation.enquiry_id,
        "quoted_price": quotation.quoted_price,
        "delivery_terms": quotation.delivery_terms,
        "payment_terms": quotation.payment_terms,
        "validity_days": quotation.validity_days,
        "special_conditions": quotation.special_conditions,
        "status": str(quotation.status.value) if quotation.status else None,
        "created_at": quotation.created_at.isoformat() if quotation.created_at else None
    }


# Contract Review endpoints
@router.post("/contract-reviews/", response_model=dict)
def create_contract_review(
    review: ContractReviewCreate,
    db: Session = Depends(get_db)
):
    """Create a contract review (AS9100D mandatory)."""
    try:
        review_number = generate_review_number()
        
        db_review = ContractReview(
            quotation_id=review.quotation_id,
            review_number=review_number,
            review_date=review.review_date,
            reviewed_by=review.reviewed_by,
            technical_feasibility=review.technical_feasibility,
            quality_feasibility=review.quality_feasibility,
            delivery_feasibility=review.delivery_feasibility,
            financial_feasibility=review.financial_feasibility,
            risk_assessment=review.risk_assessment,
            special_requirements=review.special_requirements,
            approval_status=review.approval_status,
            notes=review.notes,
            created_by=1  # Default user ID since auth is removed
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        
        return {
            "id": db_review.id,
            "review_number": db_review.review_number,
            "quotation_id": db_review.quotation_id,
            "approval_status": db_review.approval_status,
            "created_at": db_review.created_at.isoformat() if db_review.created_at else None
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating contract review: {str(e)}"
        )


@router.get("/contract-reviews/", response_model=dict)
def list_contract_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List contract reviews."""
    try:
        query = db.query(ContractReview)
        total = query.count()
        reviews = query.offset(skip).limit(limit).all()
        
        return {
            "total": total,
            "reviews": [
                {
                    "id": review.id,
                    "review_number": review.review_number,
                    "quotation_id": review.quotation_id,
                    "approval_status": review.approval_status,
                    "created_at": review.created_at.isoformat() if review.created_at else None
                }
                for review in reviews
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing contract reviews: {str(e)}"
        )


# Customer Purchase Order endpoints
@router.post("/customer-orders/", response_model=dict)
def create_customer_order(
    order: CustomerPurchaseOrderCreate,
    db: Session = Depends(get_db)
):
    """Create a customer purchase order."""
    try:
        po_number = generate_po_number()
        
        db_order = CustomerPurchaseOrder(
            quotation_id=order.quotation_id,
            po_number=po_number,
            customer_po_number=order.customer_po_number,
            order_date=order.order_date,
            delivery_date=order.delivery_date,
            total_value=order.total_value,
            terms_conditions=order.terms_conditions,
            status=order.status,
            created_by=1  # Default user ID since auth is removed
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        return {
            "id": db_order.id,
            "po_number": db_order.po_number,
            "customer_po_number": db_order.customer_po_number,
            "total_value": db_order.total_value,
            "status": db_order.status,
            "created_at": db_order.created_at.isoformat() if db_order.created_at else None
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating customer order: {str(e)}"
        )


@router.get("/customer-orders/", response_model=dict)
def list_customer_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List customer purchase orders."""
    try:
        query = db.query(CustomerPurchaseOrder)
        
        if search:
            search_filter = or_(
                CustomerPurchaseOrder.po_number.ilike(f"%{search}%"),
                CustomerPurchaseOrder.customer_po_number.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        total = query.count()
        orders = query.offset(skip).limit(limit).all()
        
        return {
            "total": total,
            "orders": [
                {
                    "id": order.id,
                    "po_number": order.po_number,
                    "customer_po_number": order.customer_po_number,
                    "total_value": order.total_value,
                    "status": order.status,
                    "created_at": order.created_at.isoformat() if order.created_at else None
                }
                for order in orders
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing customer orders: {str(e)}"
        )
