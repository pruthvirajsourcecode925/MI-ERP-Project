from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.database.database import get_db
from app.models.purchase import (
    Supplier, SupplierEvaluation, PurchaseOrder, PurchaseOrderItem,
    SubcontractingOrder, SupplierNCR, SupplierStatus, EvaluationStatus
)
from app.schemas.purchase import (
    SupplierCreate, SupplierUpdate, SupplierResponse,
    SupplierEvaluationCreate, SupplierEvaluationUpdate, SupplierEvaluationResponse,
    PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderResponse,
    PurchaseOrderItemCreate, PurchaseOrderItemResponse,
    SubcontractingOrderCreate, SubcontractingOrderUpdate, SubcontractingOrderResponse,
    SupplierNCRCreate, SupplierNCRUpdate, SupplierNCRResponse,
    SupplierList, SupplierEvaluationList, PurchaseOrderList,
    SubcontractingOrderList, SupplierNCRList
)
import uuid
from datetime import datetime

router = APIRouter()


def generate_supplier_code():
    """Generate unique supplier code."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"SUP-{year}-{random_id}"


def generate_evaluation_number():
    """Generate unique evaluation number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"EVAL-{year}-{random_id}"


def generate_po_number():
    """Generate unique PO number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"PO-{year}-{random_id}"


def generate_subcontract_number():
    """Generate unique subcontract order number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"SUB-{year}-{random_id}"


def generate_ncr_number():
    """Generate unique NCR number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"NCR-SUP-{year}-{random_id}"


# Supplier Routes
@router.post("/suppliers/", response_model=SupplierResponse)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db)
):
    """Create a new supplier (ASL entry)."""
    supplier_code = generate_supplier_code()
    db_supplier = Supplier(
        **supplier.dict(),
        supplier_code=supplier_code,
        created_by=1
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


@router.get("/suppliers/", response_model=SupplierList)
def list_suppliers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[SupplierStatus] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List suppliers with filtering."""
    query = db.query(Supplier)
    
    if status:
        query = query.filter(Supplier.status == status)
    
    if search:
        query = query.filter(
            or_(
                Supplier.supplier_code.ilike(f"%{search}%"),
                Supplier.supplier_name.ilike(f"%{search}%"),
                Supplier.contact_person.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    suppliers = query.offset(skip).limit(limit).all()
    
    return SupplierList(
        suppliers=suppliers,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/suppliers/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    """Get specific supplier."""
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    return supplier


@router.put("/suppliers/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    supplier_update: SupplierUpdate,
    db: Session = Depends(get_db)
):
    """Update supplier."""
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    update_data = supplier_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(supplier, field, value)
    
    db.commit()
    db.refresh(supplier)
    return supplier


@router.put("/suppliers/{supplier_id}/approve")
def approve_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    """Approve supplier (Manager/Admin only)."""
    


# Supplier Evaluation Routes
@router.post("/supplier-evaluations/", response_model=SupplierEvaluationResponse)
def create_supplier_evaluation(
    evaluation: SupplierEvaluationCreate,
    db: Session = Depends(get_db)
):
    """Create supplier evaluation."""
    evaluation_number = generate_evaluation_number()
    
    # Verify supplier exists
    supplier = db.query(Supplier).filter(Supplier.id == evaluation.supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    db_evaluation = SupplierEvaluation(
        **evaluation.dict(),
        evaluation_number=evaluation_number,
        evaluated_by=1
    )
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation


@router.get("/supplier-evaluations/", response_model=SupplierEvaluationList)
def list_supplier_evaluations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List supplier evaluations with filtering."""
    query = db.query(SupplierEvaluation)
    
    if search:
        query = query.filter(
            or_(
                SupplierEvaluation.evaluation_number.ilike(f"%{search}%"),
                SupplierEvaluation.supplier.has(Supplier.supplier_name.ilike(f"%{search}%"))
            )
        )
    
    total = query.count()
    evaluations = query.offset(skip).limit(limit).all()
    
    return SupplierEvaluationList(
        evaluations=evaluations,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.put("/supplier-evaluations/{evaluation_id}/approve")
def approve_supplier_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db)
):
    """Approve supplier evaluation (Manager/Admin only)."""
    


# Purchase Order Routes
@router.post("/purchase-orders/", response_model=PurchaseOrderResponse)
def create_purchase_order(
    order: PurchaseOrderCreate,
    db: Session = Depends(get_db)
):
    """Create a new purchase order."""
    po_number = generate_po_number()
    
    # Verify supplier exists and is approved
    supplier = db.query(Supplier).filter(Supplier.id == order.supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        ) 
    
    if supplier.status != SupplierStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supplier is not approved for purchasing"
        )
    
    db_order = PurchaseOrder(
        **order.dict(exclude={'items'}),
        po_number=po_number,
        created_by=1
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Add PO items
    for item in order.items:
        db_item = PurchaseOrderItem(
            **item.dict(),
            po_id=db_order.id
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/purchase-orders/", response_model=PurchaseOrderList)
def list_purchase_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List purchase orders with filtering."""
    query = db.query(PurchaseOrder)
    
    if search:
        query = query.filter(
            or_(
                PurchaseOrder.po_number.ilike(f"%{search}%"),
                PurchaseOrder.supplier.has(Supplier.supplier_name.ilike(f"%{search}%"))
            )
        )
    
    total = query.count()
    orders = query.offset(skip).limit(limit).all()
    
    return PurchaseOrderList(
        orders=orders,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/purchase-orders/{po_id}", response_model=PurchaseOrderResponse)
def get_purchase_order(
    po_id: int,
    db: Session = Depends(get_db)
):
    """Get specific purchase order."""
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase order not found"
        )
    return po


# Subcontracting Order Routes
@router.post("/subcontracting-orders/", response_model=SubcontractingOrderResponse)
def create_subcontracting_order(
    order: SubcontractingOrderCreate,
    db: Session = Depends(get_db)
):
    """Create a new subcontracting order."""
    order_number = generate_subcontract_number()
    
    # Verify supplier exists and is approved
    supplier = db.query(Supplier).filter(Supplier.id == order.supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    if supplier.status != SupplierStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supplier is not approved for subcontracting"
        )
    
    db_order = SubcontractingOrder(
        **order.dict(),
        order_number=order_number,
        created_by=1
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/subcontracting-orders/", response_model=SubcontractingOrderList)
def list_subcontracting_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List subcontracting orders with filtering."""
    query = db.query(SubcontractingOrder)
    
    if search:
        query = query.filter(
            or_(
                SubcontractingOrder.order_number.ilike(f"%{search}%"),
                SubcontractingOrder.part_number.ilike(f"%{search}%"),
                SubcontractingOrder.supplier.has(Supplier.supplier_name.ilike(f"%{search}%"))
            )
        )
    
    total = query.count()
    orders = query.offset(skip).limit(limit).all()
    
    return SubcontractingOrderList(
        orders=orders,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Supplier NCR Routes
@router.post("/supplier-ncrs/", response_model=SupplierNCRResponse)
def create_supplier_ncr(
    ncr: SupplierNCRCreate,
    db: Session = Depends(get_db)
):
    """Create supplier NCR."""
    ncr_number = generate_ncr_number()
    
    # Verify supplier exists
    if ncr.supplier_id:
        supplier = db.query(Supplier).filter(Supplier.id == ncr.supplier_id).first()
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found"
            )
    
    # Verify PO exists if provided
    if ncr.po_id:
        po = db.query(PurchaseOrder).filter(PurchaseOrder.id == ncr.po_id).first()
        if not po:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Purchase order not found"
            )
    
    db_ncr = SupplierNCR(
        **ncr.dict(),
        ncr_number=ncr_number,
        created_by=1
    )
    db.add(db_ncr)
    db.commit()
    db.refresh(db_ncr)
    return db_ncr


@router.get("/supplier-ncrs/", response_model=SupplierNCRList)
def list_supplier_ncrs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List supplier NCRs with filtering."""
    query = db.query(SupplierNCR)
    
    if search:
        query = query.filter(
            or_(
                SupplierNCR.ncr_number.ilike(f"%{search}%"),
                SupplierNCR.material_description.ilike(f"%{search}%"),
                SupplierNCR.supplier.has(Supplier.supplier_name.ilike(f"%{search}%"))
            )
        )
    
    total = query.count()
    ncrs = query.offset(skip).limit(limit).all()
    
    return SupplierNCRList(
        ncrs=ncrs,
        total=total,
        page=skip // limit + 1,
        size=limit
    )
