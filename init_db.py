#!/usr/bin/env python
# init_db.py
from app import create_app
from models import db, Employee
from werkzeug.security import generate_password_hash
import hashlib


print("Starting...")
app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    
    # Create default employee account
    email = "admin@example.com"
    password = "admin"
    
    # Check if employee already exists
    existing_employee = Employee.query.filter_by(email=email).first()
    if not existing_employee:
        employee = Employee(
            name="Daniel",
            email=email,
            password_hash=generate_password_hash(password),
            role="admin"
        )
        db.session.add(employee)
        db.session.commit()
        print(f"Created employee account for {email}")
    else:
        print("Updating employee account...")
        existing_employee.password_hash = generate_password_hash(password)  
        existing_employee.role = "admin"
        existing_employee.name = "Daniel"
        existing_employee.email = "daniel@eanix.net"
        db.session.add(existing_employee)
        db.session.commit()
        print(f"Updated employee account for {email}")
    
    print("Database tables created successfully!") 
