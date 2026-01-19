#!/usr/bin/env python3
"""
Deep Debug Sales Module
Find exact root cause of 500 errors
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_sales_imports():
    """Debug sales module imports"""
    
    print("🔍 DEBUGGING SALES IMPORTS")
    print("=" * 60)
    
    try:
        print("Testing app.models.sales import...")
        from app.models import sales
        print("✅ app.models.sales imported successfully")
        
        print("Testing CustomerEnquiry model...")
        from app.models.sales import CustomerEnquiry
        print("✅ CustomerEnquiry model imported successfully")
        
        print("Testing Quotation model...")
        from app.models.sales import Quotation
        print("✅ Quotation model imported successfully")
        
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        print(f"   Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def debug_sales_router():
    """Debug sales router imports"""
    
    print("\n🔍 DEBUGGING SALES ROUTER")
    print("=" * 60)
    
    try:
        print("Testing app.routers.sales import...")
        from app.routers import sales
        print("✅ app.routers.sales imported successfully")
        
        print("Testing router object...")
        router = sales.router
        print(f"✅ Router object: {router}")
        print(f"   Router type: {type(router)}")
        
    except Exception as e:
        print(f"❌ Router import error: {str(e)}")
        print(f"   Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def debug_sales_schemas():
    """Debug sales schemas"""
    
    print("\n🔍 DEBUGGING SALES SCHEMAS")
    print("=" * 60)
    
    try:
        print("Testing app.schemas.sales import...")
        from app.schemas import sales
        print("✅ app.schemas.sales imported successfully")
        
        print("Testing CustomerEnquiryCreate schema...")
        from app.schemas.sales import CustomerEnquiryCreate
        print("✅ CustomerEnquiryCreate schema imported successfully")
        
    except Exception as e:
        print(f"❌ Schema import error: {str(e)}")
        print(f"   Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def debug_database_connection():
    """Debug database connection for sales"""
    
    print("\n🔍 DEBUGGING DATABASE CONNECTION")
    print("=" * 60)
    
    try:
        from app.database.database import get_db, engine
        print("✅ Database imports successful")
        
        print("Testing database engine...")
        print(f"   Engine: {engine}")
        print(f"   Engine URL: {engine.url}")
        
        print("Testing database session...")
        db = next(get_db())
        print("✅ Database session created")
        
        print("Testing simple query...")
        from app.models.sales import CustomerEnquiry
        result = db.query(CustomerEnquiry).count()
        print(f"✅ Query successful: {result} enquiries found")
        
        db.close()
        print("✅ Database session closed")
        
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        print(f"   Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def debug_sales_endpoint():
    """Debug sales endpoint directly"""
    
    print("\n🔍 DEBUGGING SALES ENDPOINT")
    print("=" * 60)
    
    try:
        from app.routers.sales import router
        from app.models.sales import CustomerEnquiry
        from app.schemas.sales import CustomerEnquiryCreate
        from app.database.database import get_db
        
        print("Testing endpoint function directly...")
        
        # Create mock request data
        mock_enquiry = CustomerEnquiryCreate(
            customer_name="Debug Test",
            part_number="DBG-001",
            drawing_number="DWG-DBG-001",
            quantity=1,
            status="new"
        )
        
        print(f"   Mock enquiry: {mock_enquiry}")
        print("✅ Mock data created successfully")
        
    except Exception as e:
        print(f"❌ Endpoint debug error: {str(e)}")
        print(f"   Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def check_main_app_imports():
    """Check main app imports"""
    
    print("\n🔍 CHECKING MAIN APP IMPORTS")
    print("=" * 60)
    
    try:
        print("Testing main app imports...")
        from app.main import app
        print("✅ Main app imported successfully")
        
        # Check if sales router is included
        routes = [route.path for route in app.routes]
        print(f"   Available routes: {routes}")
        
        sales_routes = [route for route in routes if 'sales' in route]
        print(f"   Sales routes: {sales_routes}")
        
    except Exception as e:
        print(f"❌ Main app error: {str(e)}")
        print(f"   Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main_debug():
    """Run all debug tests"""
    
    print("🔍 COMPREHENSIVE SALES MODULE DEBUG")
    print("=" * 80)
    print("Finding exact root cause of 500 errors...")
    print("=" * 80)
    
    results = []
    
    # Test each component
    results.append(debug_sales_imports())
    results.append(debug_sales_schemas())
    results.append(debug_sales_router())
    results.append(debug_database_connection())
    results.append(debug_sales_endpoint())
    results.append(check_main_app_imports())
    
    # Summary
    print("\n📊 DEBUG SUMMARY")
    print("=" * 80)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All components working - issue may be runtime")
    else:
        print("❌ Some components failing - found root cause")
    
    print("\n🎯 NEXT STEPS:")
    if passed == total:
        print("1. Check server logs for runtime errors")
        print("2. Test with actual HTTP requests")
        print("3. Check for circular dependencies")
    else:
        print("1. Fix failed components first")
        print("2. Re-test sales module")
        print("3. Verify all imports work")
    
    print("=" * 80)

if __name__ == "__main__":
    main_debug()
