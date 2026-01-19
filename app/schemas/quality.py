from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from app.models.quality import InspectionType, NCRStatus, CAPAStatus


class InspectionReportBase(BaseModel):
    inspection_type: InspectionType
    part_number: str
    drawing_number: str
    quantity_inspected: int
    quantity_accepted: int
    quantity_rejected: int
    remarks: Optional[str] = None
    status: str = "completed"


class InspectionReportCreate(InspectionReportBase):
    job_card_id: Optional[int] = None
    inward_id: Optional[int] = None


class InspectionReportUpdate(BaseModel):
    inspection_type: Optional[InspectionType] = None
    part_number: Optional[str] = None
    drawing_number: Optional[str] = None
    quantity_inspected: Optional[int] = None
    quantity_accepted: Optional[int] = None
    quantity_rejected: Optional[int] = None
    remarks: Optional[str] = None


class InspectionReportResponse(InspectionReportBase):
    id: int
    report_number: str
    job_card_id: Optional[int] = None
    inward_id: Optional[int] = None
    inspection_date: datetime
    inspector_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class InspectionCharacteristicBase(BaseModel):
    characteristic_number: int
    description: str
    specification: str
    tolerance: Optional[str] = None
    measured_value: Optional[str] = None
    result: str
    gauge_used: Optional[str] = None


class InspectionCharacteristicCreate(InspectionCharacteristicBase):
    inspection_report_id: int


class InspectionCharacteristicResponse(InspectionCharacteristicBase):
    id: int
    inspection_report_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class FAIReportBase(BaseModel):
    part_number: str
    drawing_number: str
    revision: str
    customer: Optional[str] = None
    quantity_produced: int
    serial_numbers: Optional[str] = None
    design_verification: bool = False
    process_validation: bool = False
    production_capability: bool = False
    gage_r_and_r: bool = False
    material_verification: bool = False
    performance_testing: bool = False
    overall_result: str = "pending"
    status: str = "draft"


class FAIReportCreate(FAIReportBase):
    pass


class FAIReportUpdate(BaseModel):
    part_number: Optional[str] = None
    drawing_number: Optional[str] = None
    revision: Optional[str] = None
    customer: Optional[str] = None
    quantity_produced: Optional[int] = None
    serial_numbers: Optional[str] = None
    design_verification: Optional[bool] = None
    process_validation: Optional[bool] = None
    production_capability: Optional[bool] = None
    gage_r_and_r: Optional[bool] = None
    material_verification: Optional[bool] = None
    performance_testing: Optional[bool] = None
    overall_result: Optional[str] = None
    status: Optional[str] = None


class FAIReportResponse(FAIReportBase):
    id: int
    fai_number: str
    fai_date: datetime
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


class FAIDimensionBase(BaseModel):
    dimension_number: int
    description: str
    specification: str
    tolerance: Optional[str] = None
    measurement_1: Optional[Decimal] = None
    measurement_2: Optional[Decimal] = None
    measurement_3: Optional[Decimal] = None
    average: Optional[Decimal] = None
    result: str
    gauge_id: Optional[str] = None


class FAIDimensionCreate(FAIDimensionBase):
    fai_report_id: int


class FAIDimensionResponse(FAIDimensionBase):
    id: int
    fai_report_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class NonConformanceReportBase(BaseModel):
    part_number: str
    drawing_number: str
    quantity_affected: int
    defect_description: str
    defect_type: str
    severity: str  # Major, Minor, Critical
    detection_stage: str  # Incoming, In-process, Final, Customer
    immediate_action: Optional[str] = None
    status: NCRStatus = NCRStatus.OPEN


class NonConformanceReportCreate(NonConformanceReportBase):
    job_card_id: Optional[int] = None
    inward_id: Optional[int] = None


class NonConformanceReportUpdate(BaseModel):
    part_number: Optional[str] = None
    drawing_number: Optional[str] = None
    quantity_affected: Optional[int] = None
    defect_description: Optional[str] = None
    defect_type: Optional[str] = None
    severity: Optional[str] = None
    detection_stage: Optional[str] = None
    immediate_action: Optional[str] = None
    status: Optional[NCRStatus] = None


class NonConformanceReportResponse(NonConformanceReportBase):
    id: int
    ncr_number: str
    job_card_id: Optional[int] = None
    inward_id: Optional[int] = None
    occurrence_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


class CAPAReportBase(BaseModel):
    source: str  # NCR, Audit, Customer Complaint, etc.
    problem_description: str
    root_cause_analysis: Optional[str] = None
    analysis_method: Optional[str] = None  # 5 Why, Fishbone, etc.
    correction_action: Optional[str] = None
    corrective_action: Optional[str] = None
    preventive_action: Optional[str] = None
    target_date: date
    completion_date: Optional[date] = None
    effectiveness_verification: Optional[str] = None
    status: CAPAStatus = CAPAStatus.PENDING


class CAPAReportCreate(CAPAReportBase):
    ncr_id: Optional[int] = None
    responsible_person: int


class CAPAReportUpdate(BaseModel):
    source: Optional[str] = None
    problem_description: Optional[str] = None
    root_cause_analysis: Optional[str] = None
    analysis_method: Optional[str] = None
    correction_action: Optional[str] = None
    corrective_action: Optional[str] = None
    preventive_action: Optional[str] = None
    target_date: Optional[date] = None
    completion_date: Optional[date] = None
    effectiveness_verification: Optional[str] = None
    status: Optional[CAPAStatus] = None


class CAPAReportResponse(CAPAReportBase):
    id: int
    capa_number: str
    ncr_id: Optional[int] = None
    responsible_person: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


class GaugeCalibrationBase(BaseModel):
    gauge_id: str
    gauge_description: str
    gauge_type: str
    range: Optional[str] = None
    accuracy: Optional[str] = None
    location: str
    last_calibration_date: date
    next_calibration_date: date
    calibration_agency: Optional[str] = None
    calibration_certificate: Optional[str] = None
    status: str = "active"


class GaugeCalibrationCreate(GaugeCalibrationBase):
    pass


class GaugeCalibrationUpdate(BaseModel):
    gauge_id: Optional[str] = None
    gauge_description: Optional[str] = None
    gauge_type: Optional[str] = None
    range: Optional[str] = None
    accuracy: Optional[str] = None
    location: Optional[str] = None
    last_calibration_date: Optional[date] = None
    next_calibration_date: Optional[date] = None
    calibration_agency: Optional[str] = None
    calibration_certificate: Optional[str] = None
    status: Optional[str] = None


class GaugeCalibrationResponse(GaugeCalibrationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    
    class Config:
        from_attributes = True


class InternalAuditBase(BaseModel):
    audit_date: date
    audit_type: str  # Process, Product, System
    scope: str
    audit_team: Optional[str] = None
    findings: Optional[str] = None
    non_conformities: Optional[str] = None
    observations: Optional[str] = None
    conclusion: Optional[str] = None
    status: str = "planned"


class InternalAuditCreate(InternalAuditBase):
    lead_auditor: int


class InternalAuditUpdate(BaseModel):
    audit_date: Optional[date] = None
    audit_type: Optional[str] = None
    scope: Optional[str] = None
    audit_team: Optional[str] = None
    findings: Optional[str] = None
    non_conformities: Optional[str] = None
    observations: Optional[str] = None
    conclusion: Optional[str] = None
    status: Optional[str] = None


class InternalAuditResponse(InternalAuditBase):
    id: int
    audit_number: str
    lead_auditor: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# List response schemas
class InspectionReportList(BaseModel):
    inspections: List[InspectionReportResponse]
    total: int
    page: int
    size: int


class FAIReportList(BaseModel):
    fai_reports: List[FAIReportResponse]
    total: int
    page: int
    size: int


class NonConformanceReportList(BaseModel):
    ncrs: List[NonConformanceReportResponse]
    total: int
    page: int
    size: int


class CAPAReportList(BaseModel):
    capas: List[CAPAReportResponse]
    total: int
    page: int
    size: int


class GaugeCalibrationList(BaseModel):
    gauges: List[GaugeCalibrationResponse]
    total: int
    page: int
    size: int


class InternalAuditList(BaseModel):
    audits: List[InternalAuditResponse]
    total: int
    page: int
    size: int
