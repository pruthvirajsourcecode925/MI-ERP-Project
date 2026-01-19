#!/usr/bin/env python3
"""
Initialize database tables without authentication
"""

from app.database.database import engine
from app.models import department, sales, engineering, purchase, stores, production, quality, maintenance, dispatch, document_control, permissions, compliance, audit

def init_database():
    """Initialize database tables."""
    print("Creating database tables...")
    
    # Create all tables
    department.Base.metadata.create_all(bind=engine)
    sales.Base.metadata.create_all(bind=engine)
    engineering.Base.metadata.create_all(bind=engine)
    purchase.Base.metadata.create_all(bind=engine)
    stores.Base.metadata.create_all(bind=engine)
    production.Base.metadata.create_all(bind=engine)
    quality.Base.metadata.create_all(bind=engine)
    maintenance.Base.metadata.create_all(bind=engine)
    dispatch.Base.metadata.create_all(bind=engine)
    document_control.Base.metadata.create_all(bind=engine)
    permissions.Base.metadata.create_all(bind=engine)
    compliance.Base.metadata.create_all(bind=engine)
    audit.Base.metadata.create_all(bind=engine)
    
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()
    print("Database initialization complete!")
