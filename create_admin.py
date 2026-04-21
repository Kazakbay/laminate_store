#!/usr/bin/env python3
"""
Script to create an admin user for the laminate store.
Run this script to create the first admin user.
"""

import os
import sys
from sqlalchemy.orm import Session
from database import SessionLocal, User
from auth_utils import get_password_hash

def create_admin_user():
    """Create an admin user."""
    db = SessionLocal()
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.is_admin == True).first()
        if existing_admin:
            print(f"Admin user already exists: {existing_admin.username}")
            return
        
        # Create admin user
        username = input("Enter admin username: ")
        email = input("Enter admin email: ")
        password = input("Enter admin password: ")
        
        # Check if username or email already exists
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            print("Username or email already exists!")
            return
        
        # Create new admin user
        try:
            hashed_password = get_password_hash(password)
        except Exception as hash_error:
            print(f"Password hashing error: {hash_error}")
            print("Using simple hash for now...")
            hashed_password = f"simple_hash_{password}"
        
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
        
        print(f"Admin user created successfully: {admin_user.username}")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
