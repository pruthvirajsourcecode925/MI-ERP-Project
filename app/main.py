from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine
from app.models import department, sales, engineering, purchase, stores, production, quality, maintenance, dispatch, document_control
from app.routers import sales, quality, engineering, purchase, production, stores, compliance, audit
from app.database.database import get_db
from app.core.config import settings

# Create database tables
department.Base.metadata.create_all(bind=engine)
sales.CustomerEnquiry.__table__.metadata.create_all(bind=engine)
sales.Quotation.__table__.metadata.create_all(bind=engine)
sales.ContractReview.__table__.metadata.create_all(bind=engine)
sales.CustomerPurchaseOrder.__table__.metadata.create_all(bind=engine)
engineering.Drawing.__table__.metadata.create_all(bind=engine)
engineering.RouteCard.__table__.metadata.create_all(bind=engine)
engineering.ProcessOperation.__table__.metadata.create_all(bind=engine)
engineering.ControlPlan.__table__.metadata.create_all(bind=engine)
engineering.ControlCharacteristic.__table__.metadata.create_all(bind=engine)
engineering.Tooling.__table__.metadata.create_all(bind=engine)
purchase.Supplier.__table__.metadata.create_all(bind=engine)
purchase.SupplierEvaluation.__table__.metadata.create_all(bind=engine)
purchase.PurchaseOrder.__table__.metadata.create_all(bind=engine)
purchase.PurchaseOrderItem.__table__.metadata.create_all(bind=engine)
purchase.SubcontractingOrder.__table__.metadata.create_all(bind=engine)
purchase.SupplierNCR.__table__.metadata.create_all(bind=engine)
stores.RawMaterialInward.__table__.metadata.create_all(bind=engine)
stores.MTCVerification.__table__.metadata.create_all(bind=engine)
stores.TraceabilityRecord.__table__.metadata.create_all(bind=engine)
stores.StockRegister.__table__.metadata.create_all(bind=engine)
stores.ShelfLifeControl.__table__.metadata.create_all(bind=engine)
stores.IdentificationTag.__table__.metadata.create_all(bind=engine)
production.JobCard.__table__.metadata.create_all(bind=engine)
production.JobCardOperation.__table__.metadata.create_all(bind=engine)
production.Machine.__table__.metadata.create_all(bind=engine)
production.ProductionLog.__table__.metadata.create_all(bind=engine)
production.FAITrigger.__table__.metadata.create_all(bind=engine)
production.ReworkRecord.__table__.metadata.create_all(bind=engine)
quality.InspectionReport.__table__.metadata.create_all(bind=engine)
quality.InspectionCharacteristic.__table__.metadata.create_all(bind=engine)
quality.FAIReport.__table__.metadata.create_all(bind=engine)
quality.FAIDimension.__table__.metadata.create_all(bind=engine)
quality.NonConformanceReport.__table__.metadata.create_all(bind=engine)
quality.CAPAReport.__table__.metadata.create_all(bind=engine)
quality.GaugeCalibration.__table__.metadata.create_all(bind=engine)
quality.InternalAudit.__table__.metadata.create_all(bind=engine)
maintenance.Base.metadata.create_all(bind=engine)
dispatch.Base.metadata.create_all(bind=engine)
document_control.Base.metadata.create_all(bind=engine)
compliance.ComplianceClause.__table__.metadata.create_all(bind=engine)
compliance.ComplianceCheck.__table__.metadata.create_all(bind=engine)
compliance.ComplianceAudit.__table__.metadata.create_all(bind=engine)
compliance.CorrectiveAction.__table__.metadata.create_all(bind=engine)
compliance.TrainingRecord.__table__.metadata.create_all(bind=engine)
compliance.SupplierCompliance.__table__.metadata.create_all(bind=engine)
compliance.ComplianceDashboard.__table__.metadata.create_all(bind=engine)
audit.AuditLog.__table__.metadata.create_all(bind=engine)
audit.Report.__table__.metadata.create_all(bind=engine)
audit.ReportExecution.__table__.metadata.create_all(bind=engine)
audit.SystemLog.__table__.metadata.create_all(bind=engine)
audit.ActivityLog.__table__.metadata.create_all(bind=engine)
audit.DataChangeLog.__table__.metadata.create_all(bind=engine)
audit.LoginHistory.__table__.metadata.create_all(bind=engine)
audit.PerformanceLog.__table__.metadata.create_all(bind=engine)









app = FastAPI(
    title="Mauli Industries ERP System",
    description="ERP System for Aerospace and Defense Division",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sales.router, prefix="/api/v1", tags=["Sales & Marketing"])
app.include_router(quality.router, prefix="/quality", tags=["Quality Management"])
app.include_router(engineering.router, prefix="/engineering", tags=["Engineering & Planning"])
app.include_router(purchase.router, prefix="/purchase", tags=["Purchase & Supplier Management"])
app.include_router(production.router, prefix="/production", tags=["Production & Job Cards"])
app.include_router(stores.router, prefix="/stores", tags=["Stores & Inward Management"])
app.include_router(compliance.router, prefix="/compliance", tags=["AS9100D Compliance"])
app.include_router(audit.router, prefix="/audit", tags=["Audit Trail & Reporting"])




@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "message": "Mauli Industries ERP System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
