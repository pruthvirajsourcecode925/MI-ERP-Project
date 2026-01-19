from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.database.database import get_db
from app.models.production import (
    JobCard, JobCardOperation, Machine, ProductionLog, 
    FAITrigger, ReworkRecord, JobStatus, OperationStatus
)
from app.schemas.production import (
    JobCardCreate, JobCardUpdate, JobCardResponse,
    JobCardOperationCreate, JobCardOperationUpdate, JobCardOperationResponse,
    MachineCreate, MachineUpdate, MachineResponse,
    ProductionLogCreate, ProductionLogResponse,
    FAITriggerCreate, FAITriggerUpdate, FAITriggerResponse,
    ReworkRecordCreate, ReworkRecordUpdate, ReworkRecordResponse,
    JobCardList, JobCardOperationList, MachineList,
    ProductionLogList, FAITriggerList, ReworkRecordList
)
import uuid
from datetime import datetime

router = APIRouter()


def generate_job_card_number():
    """Generate unique job card number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"JC-{year}-{random_id}"


def generate_machine_code():
    """Generate unique machine code."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"MC-{year}-{random_id}"


def generate_trigger_number():
    """Generate unique FAI trigger number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"TRG-{year}-{random_id}"


def generate_rework_number():
    """Generate unique rework number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"RW-{year}-{random_id}"


# Job Card Routes
@router.post("/job-cards/", response_model=JobCardResponse)
def create_job_card(
    job_card: JobCardCreate,
    db: Session = Depends(get_db)
):
    """Create a new job card."""
    job_card_number = generate_job_card_number()
    
    # Verify route card exists if provided
    if job_card.route_card_id:
        from app.models.engineering import RouteCard
        route_card = db.query(RouteCard).filter(RouteCard.id == job_card.route_card_id).first()
        if not route_card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Route card not found"
            )
    
    db_job_card = JobCard(
        **job_card.dict(),
        job_card_number=job_card_number,
        created_by=1
    )
    db.add(db_job_card)
    db.commit()
    db.refresh(db_job_card)
    return db_job_card


@router.get("/job-cards/", response_model=JobCardList)
def list_job_cards(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[JobStatus] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List job cards with filtering."""
    query = db.query(JobCard)
    
    if status:
        query = query.filter(JobCard.status == status)
    
    if search:
        query = query.filter(
            or_(
                JobCard.job_card_number.ilike(f"%{search}%"),
                JobCard.part_number.ilike(f"%{search}%"),
                JobCard.drawing_number.ilike(f"%{search}%"),
                JobCard.customer_po.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    job_cards = query.offset(skip).limit(limit).all()
    
    return JobCardList(
        job_cards=job_cards,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/job-cards/{job_card_id}", response_model=JobCardResponse)
def get_job_card(
    job_card_id: int,
    db: Session = Depends(get_db)
):
    """Get specific job card."""
    job_card = db.query(JobCard).filter(JobCard.id == job_card_id).first()
    if not job_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job card not found"
        )
    return job_card


@router.put("/job-cards/{job_card_id}", response_model=JobCardResponse)
def update_job_card(
    job_card_id: int,
    job_card_update: JobCardUpdate,
    db: Session = Depends(get_db)
):
    """Update job card."""
    job_card = db.query(JobCard).filter(JobCard.id == job_card_id).first()
    if not job_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job card not found"
        )
    
    update_data = job_card_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job_card, field, value)
    
    db.commit()
    db.refresh(job_card)
    return job_card


@router.put("/job-cards/{job_card_id}/start")
def start_job_card(
    job_card_id: int,
    db: Session = Depends(get_db)
):
    """Start job card production."""
    job_card = db.query(JobCard).filter(JobCard.id == job_card_id).first()
    if not job_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job card not found"
        )
    
    job_card.status = JobStatus.IN_PROGRESS
    job_card.actual_start_date = datetime.utcnow()
    db.commit()
    db.refresh(job_card)
    return {"message": "Job card started successfully"}


@router.put("/job-cards/{job_card_id}/complete")
def complete_job_card(
    job_card_id: int,
    db: Session = Depends(get_db)
):
    """Complete job card production."""
    job_card = db.query(JobCard).filter(JobCard.id == job_card_id).first()
    if not job_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job card not found"
        )
    
    job_card.status = JobStatus.COMPLETED
    job_card.actual_completion_date = datetime.utcnow()
    db.commit()
    db.refresh(job_card)
    return {"message": "Job card completed successfully"}


# Job Card Operation Routes
@router.post("/job-card-operations/", response_model=JobCardOperationResponse)
def create_job_card_operation(
    operation: JobCardOperationCreate,
    db: Session = Depends(get_db)
):
    """Create a new job card operation."""
    db_operation = JobCardOperation(**operation.dict())
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation


@router.get("/job-cards/{job_card_id}/operations", response_model=JobCardOperationList)
def list_job_card_operations(
    job_card_id: int,
    db: Session = Depends(get_db)
):
    """List operations for a specific job card."""
    operations = db.query(JobCardOperation).filter(JobCardOperation.job_card_id == job_card_id).all()
    
    return JobCardOperationList(
        operations=operations,
        total=len(operations),
        page=1,
        size=len(operations)
    )


@router.put("/job-card-operations/{operation_id}/start")
def start_operation(
    operation_id: int,
    db: Session = Depends(get_db)
):
    """Start job card operation."""
    operation = db.query(JobCardOperation).filter(JobCardOperation.id == operation_id).first()
    if not operation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operation not found"
        )
    
    operation.status = OperationStatus.IN_PROGRESS
    operation.start_time = datetime.utcnow()
    db.commit()
    db.refresh(operation)
    return {"message": "Operation started successfully"}


@router.put("/job-card-operations/{operation_id}/complete")
def complete_operation(
    operation_id: int,
    db: Session = Depends(get_db)
):
    """Complete job card operation."""
    operation = db.query(JobCardOperation).filter(JobCardOperation.id == operation_id).first()
    if not operation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operation not found"
        )
    
    operation.status = OperationStatus.COMPLETED
    operation.end_time = datetime.utcnow()
    db.commit()
    db.refresh(operation)
    return {"message": "Operation completed successfully"}


# Machine Routes
@router.post("/machines/", response_model=MachineResponse)
def create_machine(
    machine: MachineCreate,
    db: Session = Depends(get_db)
):
    """Create a new machine."""
    machine_code = generate_machine_code()
    db_machine = Machine(
        **machine.dict(),
        machine_code=machine_code,
        created_by=1
    )
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return db_machine


@router.get("/machines/", response_model=MachineList)
def list_machines(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    machine_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List machines with filtering."""
    query = db.query(Machine)
    
    if machine_type:
        query = query.filter(Machine.machine_type == machine_type)
    
    if search:
        query = query.filter(
            or_(
                Machine.machine_code.ilike(f"%{search}%"),
                Machine.machine_name.ilike(f"%{search}%"),
                Machine.manufacturer.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    machines = query.offset(skip).limit(limit).all()
    
    return MachineList(
        machines=machines,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/machines/{machine_id}", response_model=MachineResponse)
def get_machine(
    machine_id: int,
    db: Session = Depends(get_db)
):
    """Get specific machine."""
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine not found"
        )
    return machine


# Production Log Routes
@router.post("/production-logs/", response_model=ProductionLogResponse)
def create_production_log(
    log: ProductionLogCreate,
    db: Session = Depends(get_db)
):
    """Create a new production log."""
    db_log = ProductionLog(**log.dict(), created_by=1)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


@router.get("/production-logs/", response_model=ProductionLogList)
def list_production_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List production logs with filtering."""
    query = db.query(ProductionLog)
    
    if search:
        query = query.filter(
            or_(
                ProductionLog.shift.ilike(f"%{search}%"),
                ProductionLog.job_card.has(JobCard.job_card_number.ilike(f"%{search}%"))
            )
        )
    
    total = query.count()
    logs = query.offset(skip).limit(limit).all()
    
    return ProductionLogList(
        logs=logs,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# FAI Trigger Routes
@router.post("/fai-triggers/", response_model=FAITriggerResponse)
def create_fai_trigger(
    trigger: FAITriggerCreate,
    db: Session = Depends(get_db)
):
    """Create a new FAI trigger."""
    trigger_number = generate_trigger_number()
    
    # Verify job card exists
    job_card = db.query(JobCard).filter(JobCard.id == trigger.job_card_id).first()
    if not job_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job card not found"
        )
    
    db_trigger = FAITrigger(
        **trigger.dict(),
        trigger_number=trigger_number,
        created_by=1
    )
    db.add(db_trigger)
    db.commit()
    db.refresh(db_trigger)
    return db_trigger


@router.get("/fai-triggers/", response_model=FAITriggerList)
def list_fai_triggers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List FAI triggers with filtering."""
    query = db.query(FAITrigger)
    
    if search:
        query = query.filter(
            or_(
                FAITrigger.trigger_number.ilike(f"%{search}%"),
                FAITrigger.job_card.has(JobCard.job_card_number.ilike(f"%{search}%"))
            )
        )
    
    total = query.count()
    triggers = query.offset(skip).limit(limit).all()
    
    return FAITriggerList(
        triggers=triggers,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Rework Record Routes
@router.post("/rework-records/", response_model=ReworkRecordResponse)
def create_rework_record(
    rework: ReworkRecordCreate,
    db: Session = Depends(get_db)
):
    """Create a new rework record."""
    rework_number = generate_rework_number()
    
    # Verify job card and operation exist
    job_card = db.query(JobCard).filter(JobCard.id == rework.job_card_id).first()
    if not job_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job card not found"
        )
    
    operation = db.query(JobCardOperation).filter(JobCardOperation.id == rework.operation_id).first()
    if not operation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operation not found"
        )
    
    db_rework = ReworkRecord(
        **rework.dict(),
        rework_number=rework_number,
        created_by=1
    )
    db.add(db_rework)
    db.commit()
    db.refresh(db_rework)
    return db_rework


@router.get("/rework-records/", response_model=ReworkRecordList)
def list_rework_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List rework records with filtering."""
    query = db.query(ReworkRecord)
    
    if search:
        query = query.filter(
            or_(
                ReworkRecord.rework_number.ilike(f"%{search}%"),
                ReworkRecord.job_card.has(JobCard.job_card_number.ilike(f"%{search}%"))
            )
        )
    
    total = query.count()
    rework_records = query.offset(skip).limit(limit).all()
    
    return ReworkRecordList(
        rework_records=rework_records,
        total=total,
        page=skip // limit + 1,
        size=limit
    )
