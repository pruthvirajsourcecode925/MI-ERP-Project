from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.database.database import get_db
from app.models.stores import (
    RawMaterialInward, MTCVerification, TraceabilityRecord, StockRegister,
    ShelfLifeControl, IdentificationTag, InspectionStatus, MaterialStatus
)
from app.schemas.stores import (
    RawMaterialInwardCreate, RawMaterialInwardUpdate, RawMaterialInwardResponse,
    MTCVerificationCreate, MTCVerificationUpdate, MTCVerificationResponse,
    TraceabilityRecordCreate, TraceabilityRecordUpdate, TraceabilityRecordResponse,
    StockRegisterCreate, StockRegisterUpdate, StockRegisterResponse,
    ShelfLifeControlCreate, ShelfLifeControlUpdate, ShelfLifeControlResponse,
    IdentificationTagCreate, IdentificationTagUpdate, IdentificationTagResponse,
    RawMaterialInwardList, MTCVerificationList, TraceabilityRecordList,
    StockRegisterList, ShelfLifeControlList, IdentificationTagList
)
import uuid
from datetime import datetime

router = APIRouter()


def generate_inward_number():
    """Generate unique inward number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"INW-{year}-{random_id}"


def generate_mtc_number():
    """Generate unique MTC verification number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"MTC-{year}-{random_id}"


def generate_traceability_number():
    """Generate unique traceability record number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"TRC-{year}-{random_id}"


def generate_tag_number():
    """Generate unique identification tag number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"TAG-{year}-{random_id}"


# Raw Material Inward Routes
@router.post("/raw-material-inwards/", response_model=RawMaterialInwardResponse)
def create_raw_material_inward(
    inward: RawMaterialInwardCreate,
    db: Session = Depends(get_db)
):
    """Create a new raw material inward."""
    inward_number = generate_inward_number()
    
    # Verify supplier exists
    from app.models.purchase import Supplier
    supplier = db.query(Supplier).filter(Supplier.id == inward.supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    # Verify PO exists if provided
    if inward.po_id:
        from app.models.purchase import PurchaseOrder
        po = db.query(PurchaseOrder).filter(PurchaseOrder.id == inward.po_id).first()
        if not po:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Purchase order not found"
            )
    
    db_inward = RawMaterialInward(
        **inward.dict(),
        inward_number=inward_number,
        created_by=1
    )
    db.add(db_inward)
    db.commit()
    db.refresh(db_inward)
    return db_inward


@router.get("/raw-material-inwards/", response_model=RawMaterialInwardList)
def list_raw_material_inwards(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    inspection_status: Optional[InspectionStatus] = Query(None),
    material_status: Optional[MaterialStatus] = Query(None),
    db: Session = Depends(get_db)
):
    """List raw material inwards with filtering."""
    query = db.query(RawMaterialInward)
    
    if inspection_status:
        query = query.filter(RawMaterialInward.inspection_status == inspection_status)
    
    if material_status:
        query = query.filter(RawMaterialInward.material_status == material_status)
    
    if search:
        query = query.filter(
            or_(
                RawMaterialInward.inward_number.ilike(f"%{search}%"),
                RawMaterialInward.part_number.ilike(f"%{search}%"),
                RawMaterialInward.drawing_number.ilike(f"%{search}%"),
                RawMaterialInward.heat_number.ilike(f"%{search}%"),
                RawMaterialInward.batch_number.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    inwards = query.offset(skip).limit(limit).all()
    
    return RawMaterialInwardList(
        inwards=inwards,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/raw-material-inwards/{inward_id}", response_model=RawMaterialInwardResponse)
def get_raw_material_inward(
    inward_id: int,
    db: Session = Depends(get_db)
):
    """Get specific raw material inward."""
    inward = db.query(RawMaterialInward).filter(RawMaterialInward.id == inward_id).first()
    if not inward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Raw material inward not found"
        )
    return inward


@router.put("/raw-material-inwards/{inward_id}", response_model=RawMaterialInwardResponse)
def update_raw_material_inward(
    inward_id: int,
    inward_update: RawMaterialInwardUpdate,
    db: Session = Depends(get_db)
):
    """Update raw material inward."""
    inward = db.query(RawMaterialInward).filter(RawMaterialInward.id == inward_id).first()
    if not inward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Raw material inward not found"
        )
    
    update_data = inward_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(inward, field, value)
    
    db.commit()
    db.refresh(inward)
    return inward


@router.put("/raw-material-inwards/{inward_id}/approve")
def approve_raw_material_inward(
    inward_id: int,
    db: Session = Depends(get_db)
):
    """Approve raw material inward (Quality/Manager only)."""
    


# MTC Verification Routes
@router.post("/mtc-verifications/", response_model=MTCVerificationResponse)
def create_mtc_verification(
    verification: MTCVerificationCreate,
    db: Session = Depends(get_db)
):
    """Create a new MTC verification."""
    mtc_number = generate_mtc_number()
    
    # Verify inward exists
    inward = db.query(RawMaterialInward).filter(RawMaterialInward.id == verification.inward_id).first()
    if not inward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Raw material inward not found"
        )
    
    db_verification = MTCVerification(
        **verification.dict(),
        mtc_number=mtc_number,
        verified_by=1
    )
    db.add(db_verification)
    db.commit()
    db.refresh(db_verification)
    return db_verification


@router.get("/mtc-verifications/", response_model=MTCVerificationList)
def list_mtc_verifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List MTC verifications with filtering."""
    query = db.query(MTCVerification)
    
    if search:
        query = query.filter(
            or_(
                MTCVerification.mtc_number.ilike(f"%{search}%"),
                MTCVerification.inward.has(RawMaterialInward.inward_number.ilike(f"%{search}%"))
            )
        )
    
    total = query.count()
    verifications = query.offset(skip).limit(limit).all()
    
    return MTCVerificationList(
        verifications=verifications,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Traceability Record Routes
@router.post("/traceability-records/", response_model=TraceabilityRecordResponse)
def create_traceability_record(
    record: TraceabilityRecordCreate,
    db: Session = Depends(get_db)
):
    """Create a new traceability record."""
    record_number = generate_traceability_number()
    
    db_record = TraceabilityRecord(
        **record.dict(),
        record_number=record_number,
        created_by=1
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@router.get("/traceability-records/", response_model=TraceabilityRecordList)
def list_traceability_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List traceability records with filtering."""
    query = db.query(TraceabilityRecord)
    
    if search:
        query = query.filter(
            or_(
                TraceabilityRecord.record_number.ilike(f"%{search}%"),
                TraceabilityRecord.part_number.ilike(f"%{search}%"),
                TraceabilityRecord.heat_number.ilike(f"%{search}%"),
                TraceabilityRecord.batch_number.ilike(f"%{search}%"),
                TraceabilityRecord.customer_po.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    records = query.offset(skip).limit(limit).all()
    
    return TraceabilityRecordList(
        records=records,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Stock Register Routes
@router.post("/stock-registers/", response_model=StockRegisterResponse)
def create_stock_register(
    stock: StockRegisterCreate,
    db: Session = Depends(get_db)
):
    """Create a new stock register entry."""
    db_stock = StockRegister(**stock.dict(), created_by=1)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


@router.get("/stock-registers/", response_model=StockRegisterList)
def list_stock_registers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List stock registers with filtering."""
    query = db.query(StockRegister)
    
    if search:
        query = query.filter(
            or_(
                StockRegister.material_code.ilike(f"%{search}%"),
                StockRegister.material_description.ilike(f"%{search}%"),
                StockRegister.heat_number.ilike(f"%{search}%"),
                StockRegister.batch_number.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    stocks = query.offset(skip).limit(limit).all()
    
    return StockRegisterList(
        stock_registers=stocks,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Shelf Life Control Routes
@router.post("/shelf-life-controls/", response_model=ShelfLifeControlResponse)
def create_shelf_life_control(
    control: ShelfLifeControlCreate,
    db: Session = Depends(get_db)
):
    """Create a new shelf life control entry."""
    db_control = ShelfLifeControl(**control.dict(), created_by=1)
    db.add(db_control)
    db.commit()
    db.refresh(db_control)
    return db_control


@router.get("/shelf-life-controls/", response_model=ShelfLifeControlList)
def list_shelf_life_controls(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List shelf life controls with filtering."""
    query = db.query(ShelfLifeControl)
    
    if search:
        query = query.filter(
            or_(
                ShelfLifeControl.material_code.ilike(f"%{search}%"),
                ShelfLifeControl.batch_number.ilike(f"%{search}%"),
                ShelfLifeControl.material_description.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    controls = query.offset(skip).limit(limit).all()
    
    return ShelfLifeControlList(
        shelf_life_controls=controls,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Identification Tag Routes
@router.post("/identification-tags/", response_model=IdentificationTagResponse)
def create_identification_tag(
    tag: IdentificationTagCreate,
    db: Session = Depends(get_db)
):
    """Create a new identification tag."""
    tag_number = generate_tag_number()
    
    db_tag = IdentificationTag(
        **tag.dict(),
        tag_number=tag_number,
        created_by=1
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@router.get("/identification-tags/", response_model=IdentificationTagList)
def list_identification_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List identification tags with filtering."""
    query = db.query(IdentificationTag)
    
    if search:
        query = query.filter(
            or_(
                IdentificationTag.tag_number.ilike(f"%{search}%"),
                IdentificationTag.part_number.ilike(f"%{search}%"),
                IdentificationTag.heat_number.ilike(f"%{search}%"),
                IdentificationTag.batch_number.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    tags = query.offset(skip).limit(limit).all()
    
    return IdentificationTagList(
        identification_tags=tags,
        total=total,
        page=skip // limit + 1,
        size=limit
    )
