from .department import Department
from .sales import CustomerEnquiry, Quotation, ContractReview, CustomerPurchaseOrder
from .engineering import Drawing, RouteCard, ProcessOperation, ControlPlan, ControlCharacteristic, Tooling
from .purchase import Supplier, SupplierEvaluation, PurchaseOrder, PurchaseOrderItem, SubcontractingOrder, SupplierNCR
from .stores import RawMaterialInward, MTCVerification, TraceabilityRecord, StockRegister, ShelfLifeControl, IdentificationTag
from .production import JobCard, JobCardOperation, Machine, ProductionLog, FAITrigger, ReworkRecord
from .quality import InspectionReport, InspectionCharacteristic, FAIReport, FAIDimension, NonConformanceReport, CAPAReport, GaugeCalibration, InternalAudit
from .maintenance import Equipment, MaintenancePlan, MaintenanceSchedule, MaintenanceRecord, BreakdownRecord, SparePart
from .dispatch import FinalChecklist, CertificateOfConformance, PackingList, Invoice, DeliveryChallan, DispatchRecord
from .document_control import MasterDocumentList, DocumentRevision, DocumentChangeRequest, RecordRetentionMatrix, ObsoleteDocumentControl, DocumentAccessLog, ControlledDocument
from .permissions import Permission, RolePermission, UserPermission, PermissionAudit
from .compliance import ComplianceClause, ComplianceCheck, ComplianceAudit, CorrectiveAction, TrainingRecord, SupplierCompliance, ComplianceDashboard
from .audit import AuditLog, Report, ReportExecution, SystemLog, ActivityLog, DataChangeLog, LoginHistory, PerformanceLog