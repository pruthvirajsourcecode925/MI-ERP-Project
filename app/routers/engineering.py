from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.database.database import get_db
from app.models.engineering import (
    Drawing, RouteCard, ProcessOperation, ControlPlan, 
    ControlCharacteristic, Tooling, DrawingStatus
)
from app.schemas.engineering import (
    DrawingCreate, DrawingUpdate, DrawingResponse,
    RouteCardCreate, RouteCardUpdate, RouteCardResponse,
    ProcessOperationCreate, ProcessOperationUpdate, ProcessOperationResponse,
    ControlPlanCreate, ControlPlanUpdate, ControlPlanResponse,
    ControlCharacteristicCreate, ControlCharacteristicResponse,
    ToolingCreate, ToolingUpdate, ToolingResponse,
    DrawingList, RouteCardList, ProcessOperationList,
    ControlPlanList, ToolingList
)
import uuid
from datetime import datetime

router = APIRouter()


def generate_drawing_number():
    """Generate unique drawing number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"DWG-{year}-{random_id}"


def generate_route_card_number():
    """Generate unique route card number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"RC-{year}-{random_id}"


def generate_plan_number():
    """Generate unique control plan number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"CP-{year}-{random_id}"


def generate_tool_number():
    """Generate unique tool number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"TL-{year}-{random_id}"


# Drawing Routes
@router.post("/drawings/", response_model=DrawingResponse)
def create_drawing(
    drawing: DrawingCreate,
    db: Session = Depends(get_db)
):
    """Create a new drawing."""
    drawing_number = generate_drawing_number()
    db_drawing = Drawing(
        **drawing.dict(),
        drawing_number=drawing_number,
        created_by=1
    )
    db.add(db_drawing)
    db.commit()
    db.refresh(db_drawing)
    return db_drawing


@router.get("/drawings/", response_model=DrawingList)
def list_drawings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[DrawingStatus] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List drawings with filtering."""
    query = db.query(Drawing)
    
    if status:
        query = query.filter(Drawing.status == status)
    
    if search:
        query = query.filter(
            or_(
                Drawing.drawing_number.ilike(f"%{search}%"),
                Drawing.title.ilike(f"%{search}%"),
                Drawing.customer.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    drawings = query.offset(skip).limit(limit).all()
    
    return DrawingList(
        drawings=drawings,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/drawings/{drawing_id}", response_model=DrawingResponse)
def get_drawing(
    drawing_id: int,
    db: Session = Depends(get_db)
):
    """Get specific drawing."""
    drawing = db.query(Drawing).filter(Drawing.id == drawing_id).first()
    if not drawing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drawing not found"
        )
    return drawing


@router.put("/drawings/{drawing_id}", response_model=DrawingResponse)
def update_drawing(
    drawing_id: int,
    drawing_update: DrawingUpdate,
    db: Session = Depends(get_db)
):
    """Update drawing."""
    drawing = db.query(Drawing).filter(Drawing.id == drawing_id).first()
    if not drawing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drawing not found"
        )
    
    update_data = drawing_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(drawing, field, value)
    
    db.commit()
    db.refresh(drawing)
    return drawing


@router.put("/drawings/{drawing_id}/approve")
def approve_drawing(
    drawing_id: int,
    db: Session = Depends(get_db)
):
    """Approve drawing (Manager/Admin only)."""
    


# Route Card Routes
@router.post("/route-cards/", response_model=RouteCardResponse)
def create_route_card(
    route_card: RouteCardCreate,
    db: Session = Depends(get_db)
):
    """Create a new route card."""
    route_card_number = generate_route_card_number()
    
    # Verify drawing exists
    drawing = db.query(Drawing).filter(Drawing.id == route_card.drawing_id).first()
    if not drawing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drawing not found"
        )
    
    db_route_card = RouteCard(
        **route_card.dict(),
        route_card_number=route_card_number,
        created_by=1
    )
    db.add(db_route_card)
    db.commit()
    db.refresh(db_route_card)
    return db_route_card


@router.get("/route-cards/", response_model=RouteCardList)
def list_route_cards(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List route cards with filtering."""
    query = db.query(RouteCard)
    
    if search:
        query = query.filter(
            or_(
                RouteCard.route_card_number.ilike(f"%{search}%"),
                RouteCard.part_number.ilike(f"%{search}%"),
                RouteCard.drawing.has(Drawing.drawing_number.ilike(f"%{search}%"))
            )
        )
    
    total = query.count()
    route_cards = query.offset(skip).limit(limit).all()
    
    return RouteCardList(
        route_cards=route_cards,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/route-cards/{route_card_id}", response_model=RouteCardResponse)
def get_route_card(
    route_card_id: int,
    db: Session = Depends(get_db)
):
    """Get specific route card."""
    route_card = db.query(RouteCard).filter(RouteCard.id == route_card_id).first()
    if not route_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route card not found"
        )
    return route_card


# Process Operation Routes
@router.post("/process-operations/", response_model=ProcessOperationResponse)
def create_process_operation(
    operation: ProcessOperationCreate,
    db: Session = Depends(get_db)
):
    """Create a new process operation."""
    db_operation = ProcessOperation(**operation.dict())
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation


@router.get("/route-cards/{route_card_id}/operations", response_model=ProcessOperationList)
def list_route_card_operations(
    route_card_id: int,
    db: Session = Depends(get_db)
):
    """List operations for a specific route card."""
    operations = db.query(ProcessOperation).filter(ProcessOperation.route_card_id == route_card_id).all()
    
    return ProcessOperationList(
        operations=operations,
        total=len(operations),
        page=1,
        size=len(operations)
    )


# Control Plan Routes
@router.post("/control-plans/", response_model=ControlPlanResponse)
def create_control_plan(
    plan: ControlPlanCreate,
    db: Session = Depends(get_db)
):
    """Create a new control plan."""
    plan_number = generate_plan_number()
    db_plan = ControlPlan(
        **plan.dict(),
        plan_number=plan_number,
        created_by=1
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


@router.get("/control-plans/", response_model=ControlPlanList)
def list_control_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List control plans with filtering."""
    query = db.query(ControlPlan)
    
    if search:
        query = query.filter(
            or_(
                ControlPlan.plan_number.ilike(f"%{search}%"),
                ControlPlan.part_number.ilike(f"%{search}%"),
                ControlPlan.drawing_revision.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    plans = query.offset(skip).limit(limit).all()
    
    return ControlPlanList(
        control_plans=plans,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/control-plans/{plan_id}/characteristics", response_model=List[ControlCharacteristicResponse])
def list_control_plan_characteristics(
    plan_id: int,
    db: Session = Depends(get_db)
):
    """List characteristics for a specific control plan."""
    characteristics = db.query(ControlCharacteristic).filter(ControlCharacteristic.control_plan_id == plan_id).all()
    return characteristics


# Tooling Routes
@router.post("/tooling/", response_model=ToolingResponse)
def create_tooling(
    tool: ToolingCreate,
    db: Session = Depends(get_db)
):
    """Create new tooling."""
    tool_number = generate_tool_number()
    db_tool = Tooling(
        **tool.dict(),
        tool_number=tool_number,
        created_by=1
    )
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool


@router.get("/tooling/", response_model=ToolingList)
def list_tooling(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    tool_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List tooling with filtering."""
    query = db.query(Tooling)
    
    if tool_type:
        query = query.filter(Tooling.tool_type == tool_type)
    
    if search:
        query = query.filter(
            or_(
                Tooling.tool_number.ilike(f"%{search}%"),
                Tooling.tool_description.ilike(f"%{search}%"),
                Tooling.part_number.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    tooling_items = query.offset(skip).limit(limit).all()
    
    return ToolingList(
        tooling=tooling_items,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/tooling/{tool_id}", response_model=ToolingResponse)
def get_tooling(
    tool_id: int,
    db: Session = Depends(get_db)
):
    """Get specific tooling."""
    tool = db.query(Tooling).filter(Tooling.id == tool_id).first()
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tooling not found"
        )
    return tool
