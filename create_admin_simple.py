#!/usr/bin/env python3
"""
Simple script to create an admin user without bcrypt dependency issues.
"""

import os
import sys
import hashlib
from sqlalchemy.orm import Session
from database import SessionLocal, User, Base, engine

def simple_hash_password(password: str) -> str:
    """Simple password hashing using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_admin_user_simple():
    """Create an admin user with simple password hashing."""
    print("Creating admin user...")
    
    # Create tables first
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.is_admin == True).first()
        if existing_admin:
            print(f"Admin user already exists: {existing_admin.username}")
            return
        
        # Create admin user with predefined credentials
        username = "admin"
        email = "admin@laminate-store.com"
        password = "admin123"
        
        # Check if username or email already exists
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            print("Username or email already exists!")
            return
        
        # Create new admin user with simple hash
        hashed_password = simple_hash_password(password)
        admin_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=True,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"Admin user created successfully!")
        print(f"Username: {admin_user.username}")
        print(f"Email: {admin_user.email}")
        print(f"Password: {password}")
        print(f"Admin status: {admin_user.is_admin}")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user_simple()
