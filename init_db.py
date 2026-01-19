#!/usr/bin/env python3
"""
Initialize database and create super admin
"""

from app.database.database import engine, SessionLocal
from app.models import user, department, sales, engineering, purchase, stores, production, quality, maintenance, dispatch, document_control
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from app.core.config import settings

def init_database():
    """Initialize database tables."""
    print("Creating database tables...")
    user.Base.metadata.create_all(bind=engine)
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
    print("Database tables created successfully!")

def create_super_admin():
    """Create super admin user."""
    db = SessionLocal()
    
    try:
        # Check if super admin exists
        super_admin = db.query(User).filter(User.role == UserRole.SUPER_ADMIN).first()
        
        if not super_admin:
            print("Creating super admin user...")
            # Use direct bcrypt hashing
            import bcrypt
            password = b"admin123"
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
            super_admin = User(
                email=settings.super_admin_email,
                username="admin",
                hashed_password=hashed_password,
                full_name="Super Administrator",
                role=UserRole.SUPER_ADMIN,
                is_active=True
            )
            
            db.add(super_admin)
            db.commit()
            print(f"Super admin created: {settings.super_admin_email}")
            print(f"Username: admin")
            print(f"Password: {settings.super_admin_password}")
        else:
            print("Super admin already exists")
            
    except Exception as e:
        print(f"Error creating super admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
    create_super_admin()
    print("Database initialization complete!")
