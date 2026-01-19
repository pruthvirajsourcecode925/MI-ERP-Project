#!/usr/bin/env python3
"""
Reset Super Admin Password
Reset password for existing super admin
"""

from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def reset_super_admin_password():
    """Reset password for existing super admin"""
    
    print("🔧 RESET SUPER ADMIN PASSWORD")
    print("=" * 50)
    
    try:
        db: Session = next(get_db())
        
        # Find the super admin
        super_admin = db.query(User).filter(User.role == UserRole.SUPER_ADMIN).first()
        
        if super_admin:
            print(f"✅ Found super admin:")
            print(f"   Username: {super_admin.username}")
            print(f"   Email: {super_admin.email}")
            print(f"   User ID: {super_admin.id}")
            
            # Reset password to "admin123"
            new_password = "admin123"
            hashed_password = get_password_hash(new_password)
            
            super_admin.hashed_password = hashed_password
            db.commit()
            
            print(f"\n✅ Password reset successfully!")
            print(f"   New Password: {new_password}")
            print(f"   Username: {super_admin.username}")
            
            # Test login
            print(f"\n🔑 TESTING LOGIN")
            import requests
            
            login_data = {
                "username": super_admin.username,
                "password": new_password
            }
            
            response = requests.post("http://localhost:8000/auth/login", json=login_data)
            print(f"   Login Status: {response.status_code}")
            
            if response.status_code == 200:
                token_data = response.json()
                token = token_data.get('access_token')
                print("✅ Login successful!")
                print(f"   Token: {token[:30]}...")
                
                # Test /me endpoint
                print(f"\n👤 TESTING /me ENDPOINT")
                headers = {"Authorization": f"Bearer {token}"}
                me_response = requests.get("http://localhost:8000/auth/me", headers=headers)
                print(f"   /me Status: {me_response.status_code}")
                
                if me_response.status_code == 200:
                    user_data = me_response.json()
                    print("✅ /me endpoint working!")
                    print(f"   User: {user_data.get('username')}")
                    print(f"   Role: {user_data.get('role')}")
                    
                    print(f"\n🎉 SUPER ADMIN READY!")
                    print("=" * 50)
                    print(f"✅ Login Details:")
                    print(f"   Username: {super_admin.username}")
                    print(f"   Password: {new_password}")
                    print(f"   Role: {user_data.get('role')}")
                    
                    print(f"\n🔐 FOR SWAGGER UI:")
                    print(f"   1. Open: http://localhost:8000/docs")
                    print(f"   2. Click 🔓 'Authorize' button")
                    print(f"   3. Enter: Bearer {token}")
                    print(f"   4. Click 'Authorize'")
                    print(f"   5. Test any protected endpoint")
                    
                    return True
                else:
                    print(f"❌ /me failed: {me_response.text}")
            else:
                print(f"❌ Login failed: {response.text}")
        else:
            print("❌ No super admin found in database")
        
        db.close()
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    reset_super_admin_password()
