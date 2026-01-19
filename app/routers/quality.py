from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.database.database import get_db
from app.models.quality import (
    InspectionReport, InspectionCharacteristic, FAIReport, FAIDimension,
    NonConformanceReport, CAPAReport, GaugeCalibration, InternalAudit,
    InspectionType, NCRStatus, CAPAStatus
)
from app.schemas.quality import (
    InspectionReportCreate, InspectionReportUpdate, InspectionReportResponse,
    InspectionCharacteristicCreate, InspectionCharacteristicResponse,
    FAIReportCreate, FAIReportUpdate, FAIReportResponse,
    FAIDimensionCreate, FAIDimensionResponse,
    NonConformanceReportCreate, NonConformanceReportUpdate, NonConformanceReportResponse,
    CAPAReportCreate, CAPAReportUpdate, CAPAReportResponse,
    GaugeCalibrationCreate, GaugeCalibrationUpdate, GaugeCalibrationResponse,
    InternalAuditCreate, InternalAuditUpdate, InternalAuditResponse,
    InspectionReportList, FAIReportList, NonConformanceReportList,
    CAPAReportList, GaugeCalibrationList, InternalAuditList
)
import uuid
from datetime import datetime

router = APIRouter()


def generate_report_number(prefix: str):
    """Generate unique report number."""
    year = datetime.now().strftime("%Y")
    random_id = str(uuid.uuid4())[:8].upper()
    return f"{prefix}-{year}-{random_id}"


# Inspection Report Routes
@router.post("/inspections/", response_model=InspectionReportResponse)
def create_inspection_report(
    inspection: InspectionReportCreate,
    db: Session = Depends(get_db)
):
    """Create an inspection report."""
    report_number = generate_report_number("INR")
    db_inspection = InspectionReport(
        **inspection.dict(),
        report_number=report_number,
        inspector_id=1
    )
    db.add(db_inspection)
    db.commit()
    db.refresh(db_inspection)
    return db_inspection


@router.get("/inspections/", response_model=InspectionReportList)
def list_inspection_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    inspection_type: Optional[InspectionType] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List inspection reports with filtering."""
    query = db.query(InspectionReport)
    
    if inspection_type:
        query = query.filter(InspectionReport.inspection_type == inspection_type)
    
    if search:
        query = query.filter(
            or_(
                InspectionReport.report_number.ilike(f"%{search}%"),
                InspectionReport.part_number.ilike(f"%{search}%"),
                InspectionReport.drawing_number.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    inspections = query.offset(skip).limit(limit).all()
    
    return InspectionReportList(
        inspections=inspections,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/inspections/{inspection_id}", response_model=InspectionReportResponse)
def get_inspection_report(
    inspection_id: int,
    db: Session = Depends(get_db)
):
    """Get specific inspection report."""
    inspection = db.query(InspectionReport).filter(InspectionReport.id == inspection_id).first()
    if not inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspection report not found"
        )
    return inspection


# FAI Report Routes (AS9102 - Most Critical)
@router.post("/fai-reports/", response_model=FAIReportResponse)
def create_fai_report(
    fai: FAIReportCreate,
    db: Session = Depends(get_db)
):
    """Create FAI report (AS9102 - Most Critical)."""
    fai_number = generate_report_number("FAI")
    db_fai = FAIReport(
        **fai.dict(),
        fai_number=fai_number,
        created_by=1
    )
    db.add(db_fai)
    db.commit()
    db.refresh(db_fai)
    return db_fai


@router.get("/fai-reports/", response_model=FAIReportList)
def list_fai_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List FAI reports with filtering."""
    query = db.query(FAIReport)
    
    if status:
        query = query.filter(FAIReport.status == status)
    
    if search:
        query = query.filter(
            or_(
                FAIReport.fai_number.ilike(f"%{search}%"),
                FAIReport.part_number.ilike(f"%{search}%"),
                FAIReport.drawing_number.ilike(f"%{search}%"),
                FAIReport.customer.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    fai_reports = query.offset(skip).limit(limit).all()
    
    return FAIReportList(
        fai_reports=fai_reports,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/fai-reports/{fai_id}", response_model=FAIReportResponse)
def get_fai_report(
    fai_id: int,
    db: Session = Depends(get_db)
):
    """Get specific FAI report."""
    fai = db.query(FAIReport).filter(FAIReport.id == fai_id).first()
    if not fai:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAI report not found"
        )
    return fai


@router.put("/fai-reports/{fai_id}/approve")
def approve_fai_report(
    fai_id: int,
    db: Session = Depends(get_db)
):
    """Approve FAI report (Manager/Admin only)."""
    


# FAI Dimension Routes
@router.post("/fai-dimensions/", response_model=FAIDimensionResponse)
def create_fai_dimension(
    dimension: FAIDimensionCreate,
    db: Session = Depends(get_db)
):
    """Create FAI dimension measurement."""
    db_dimension = FAIDimension(**dimension.dict())
    db.add(db_dimension)
    db.commit()
    db.refresh(db_dimension)
    return db_dimension


@router.get("/fai-reports/{fai_id}/dimensions", response_model=List[FAIDimensionResponse])
def list_fai_dimensions(
    fai_id: int,
    db: Session = Depends(get_db)
):
    """List dimensions for a specific FAI report."""
    dimensions = db.query(FAIDimension).filter(FAIDimension.fai_report_id == fai_id).all()
    return dimensions


# NCR Routes
@router.post("/ncrs/", response_model=NonConformanceReportResponse)
def create_ncr(
    ncr: NonConformanceReportCreate,
    db: Session = Depends(get_db)
):
    """Create Non-Conformance Report."""
    ncr_number = generate_report_number("NCR")
    db_ncr = NonConformanceReport(
        **ncr.dict(),
        ncr_number=ncr_number,
        created_by=1
    )
    db.add(db_ncr)
    db.commit()
    db.refresh(db_ncr)
    return db_ncr


@router.get("/ncrs/", response_model=NonConformanceReportList)
def list_ncrs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[NCRStatus] = Query(None),
    severity: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List NCRs with filtering."""
    query = db.query(NonConformanceReport)
    
    if status:
        query = query.filter(NonConformanceReport.status == status)
    
    if severity:
        query = query.filter(NonConformanceReport.severity == severity)
    
    if search:
        query = query.filter(
            or_(
                NonConformanceReport.ncr_number.ilike(f"%{search}%"),
                NonConformanceReport.part_number.ilike(f"%{search}%"),
                NonConformanceReport.drawing_number.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    ncrs = query.offset(skip).limit(limit).all()
    
    return NonConformanceReportList(
        ncrs=ncrs,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/ncrs/{ncr_id}", response_model=NonConformanceReportResponse)
def get_ncr(
    ncr_id: int,
    db: Session = Depends(get_db)
):
    """Get specific NCR."""
    ncr = db.query(NonConformanceReport).filter(NonConformanceReport.id == ncr_id).first()
    if not ncr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NCR not found"
        )
    return ncr


# CAPA Routes
@router.post("/capas/", response_model=CAPAReportResponse)
def create_capa(
    capa: CAPAReportCreate,
    db: Session = Depends(get_db)
):
    """Create CAPA report."""
    capa_number = generate_report_number("CAPA")
    db_capa = CAPAReport(
        **capa.dict(),
        capa_number=capa_number,
        created_by=1
    )
    db.add(db_capa)
    db.commit()
    db.refresh(db_capa)
    return db_capa


@router.get("/capas/", response_model=CAPAReportList)
def list_capas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[CAPAStatus] = Query(None),
    source: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List CAPA reports with filtering."""
    query = db.query(CAPAReport)
    
    if status:
        query = query.filter(CAPAReport.status == status)
    
    if source:
        query = query.filter(CAPAReport.source == source)
    
    if search:
        query = query.filter(
            or_(
                CAPAReport.capa_number.ilike(f"%{search}%"),
                CAPAReport.problem_description.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    capas = query.offset(skip).limit(limit).all()
    
    return CAPAReportList(
        capas=capas,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/capas/{capa_id}", response_model=CAPAReportResponse)
def get_capa(
    capa_id: int,
    db: Session = Depends(get_db)
):
    """Get specific CAPA report."""
    capa = db.query(CAPAReport).filter(CAPAReport.id == capa_id).first()
    if not capa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CAPA report not found"
        )
    return capa


# Gauge Calibration Routes
@router.post("/gauge-calibrations/", response_model=GaugeCalibrationResponse)
def create_gauge_calibration(
    gauge: GaugeCalibrationCreate,
    db: Session = Depends(get_db)
):
    """Create gauge calibration record."""
    db_gauge = GaugeCalibration(
        **gauge.dict(),
        created_by=1
    )
    db.add(db_gauge)
    db.commit()
    db.refresh(db_gauge)
    return db_gauge


@router.get("/gauge-calibrations/", response_model=GaugeCalibrationList)
def list_gauge_calibrations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List gauge calibrations with filtering."""
    query = db.query(GaugeCalibration)
    
    if search:
        query = query.filter(
            or_(
                GaugeCalibration.gauge_id.ilike(f"%{search}%"),
                GaugeCalibration.gauge_description.ilike(f"%{search}%"),
                GaugeCalibration.gauge_type.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    gauges = query.offset(skip).limit(limit).all()
    
    return GaugeCalibrationList(
        gauges=gauges,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Internal Audit Routes
@router.post("/internal-audits/", response_model=InternalAuditResponse)
def create_internal_audit(
    audit: InternalAuditCreate,
    db: Session = Depends(get_db)
):
    """Create internal audit record."""
    audit_number = generate_report_number("AUD")
    db_audit = InternalAudit(
        **audit.dict(),
        audit_number=audit_number,
        lead_auditor=1
    )
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    return db_audit


@router.get("/internal-audits/", response_model=InternalAuditList)
def list_internal_audits(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List internal audits with filtering."""
    query = db.query(InternalAudit)
    
    if search:
        query = query.filter(
            or_(
                InternalAudit.audit_number.ilike(f"%{search}%"),
                InternalAudit.audit_type.ilike(f"%{search}%"),
                InternalAudit.scope.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    audits = query.offset(skip).limit(limit).all()
    
    return InternalAuditList(
        audits=audits,
        total=total,
        page=skip // limit + 1,
        size=limit
    )
