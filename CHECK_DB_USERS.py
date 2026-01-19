#!/usr/bin/env python3
"""
Check Database Users
Debug what's in the database
"""

from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User, UserRole

def check_db_users():
    """Check what users exist in database"""
    
    print("🔍 CHECKING DATABASE USERS")
    print("=" * 50)
    
    try:
        db: Session = next(get_db())
        
        # Get all users
        users = db.query(User).all()
        print(f"Total users in database: {len(users)}")
        
        for user in users:
            print(f"\nUser ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Role: {user.role}")
            print(f"Active: {user.is_active}")
            print(f"Email Verified: {user.is_email_verified}")
            print(f"Created: {user.created_at}")
        
        # Check super admin specifically
        super_admins = db.query(User).filter(User.role == UserRole.SUPER_ADMIN).all()
        print(f"\nSuper admins: {len(super_admins)}")
        
        for admin in super_admins:
            print(f"  - {admin.username} ({admin.email})")
        
        db.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_db_users()
