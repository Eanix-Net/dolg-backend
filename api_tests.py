#!/usr/bin/env python3
# api_tests.py - Comprehensive API tests for LawnMate backend

import requests
import unittest
import os
import json
import random
import string
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Try to load environment variables from .env file
load_dotenv(".env.test")

# Base URL for API tests
BASE_URL = "http://localhost:5000/api"


class LawnMateAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test data and authentication"""
        # Admin login credentials
        cls.admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        cls.admin_password = os.getenv("ADMIN_PASSWORD", "admin")
        
        # Employee login credentials
        cls.employee_email = os.getenv("EMPLOYEE_EMAIL", "employee@example.com")
        cls.employee_password = os.getenv("EMPLOYEE_PASSWORD", "employeepassword")
        
        # Lead login credentials
        cls.lead_email = os.getenv("LEAD_EMAIL", "lead@example.com")
        cls.lead_password = os.getenv("LEAD_PASSWORD", "leadpassword")
        
        # Get auth tokens
        cls.admin_token = cls.get_auth_token(cls.admin_email, cls.admin_password)
        cls.employee_token = cls.get_auth_token(cls.employee_email, cls.employee_password)
        cls.lead_token = cls.get_auth_token(cls.lead_email, cls.lead_password)
        
        # Test data
        cls.test_data = {}
    
    @staticmethod
    def get_auth_token(email, password):
        """Helper method to get authentication token"""
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"Failed to get auth token for {email}: {response.text}")
            return None
    
    @staticmethod
    def generate_random_string(length=8):
        """Generate a random string for test data"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def get_headers(self, token=None):
        """Get request headers with optional auth token"""
        headers = {
            "Content-Type": "application/json"
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    # --- Health Check Test ---
    def test_01_health_check(self):
        """Test the health check endpoint"""
        response = requests.get(f"{BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "healthy")

    # --- Authentication Tests ---
    def test_02_login_success(self):
        """Test successful login"""
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": self.admin_email, "password": self.admin_password}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
    
    def test_03_login_failure(self):
        """Test failed login with wrong credentials"""
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": self.admin_email, "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 401)
    
    # --- Customer API Tests ---
    def test_04_get_customers(self):
        """Test getting all customers"""
        response = requests.get(
            f"{BASE_URL}/customers",
            headers=self.get_headers(self.admin_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    def test_05_create_customer(self):
        """Test creating a new customer"""
        customer_data = {
            "name": f"Test Customer {self.generate_random_string()}",
            "email": f"test.{self.generate_random_string()}@example.com",
            "phone": f"+1{self.generate_random_string(10)}",
            "notes": "Test customer created by automated tests"
        }
        
        response = requests.post(
            f"{BASE_URL}/customers",
            headers=self.get_headers(self.admin_token),
            json=customer_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save customer ID for later tests
        self.test_data["customer_id"] = response.json().get("id")
        self.assertEqual(response.json().get("name"), customer_data["name"])
    
    def test_06_get_customer(self):
        """Test getting a specific customer"""
        customer_id = self.test_data.get("customer_id")
        self.assertIsNotNone(customer_id, "Customer ID not set from previous test")
        
        response = requests.get(
            f"{BASE_URL}/customers/{customer_id}",
            headers=self.get_headers(self.admin_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("id"), customer_id)
    
    def test_07_update_customer(self):
        """Test updating a customer"""
        customer_id = self.test_data.get("customer_id")
        self.assertIsNotNone(customer_id, "Customer ID not set from previous test")
        
        updated_data = {
            "name": f"Updated Customer {self.generate_random_string()}",
            "notes": "Updated by automated tests"
        }
        
        response = requests.put(
            f"{BASE_URL}/customers/{customer_id}",
            headers=self.get_headers(self.admin_token),
            json=updated_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("name"), updated_data["name"])
        self.assertEqual(response.json().get("notes"), updated_data["notes"])
    
    # --- Location API Tests ---
    def test_08_create_location(self):
        """Test creating a location for a customer"""
        customer_id = self.test_data.get("customer_id")
        self.assertIsNotNone(customer_id, "Customer ID not set from previous test")
        
        location_data = {
            "customer_id": customer_id,
            "address": f"{self.generate_random_string()} Main St",
            "city": "Testville",
            "state": "TS",
            "zip_code": "12345",
            "notes": "Test location created by automated tests"
        }
        
        response = requests.post(
            f"{BASE_URL}/locations",
            headers=self.get_headers(self.admin_token),
            json=location_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save location ID for later tests
        self.test_data["location_id"] = response.json().get("id")
    
    def test_09_get_locations(self):
        """Test getting all locations"""
        response = requests.get(
            f"{BASE_URL}/locations",
            headers=self.get_headers(self.admin_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    def test_10_get_location(self):
        """Test getting a specific location"""
        location_id = self.test_data.get("location_id")
        self.assertIsNotNone(location_id, "Location ID not set from previous test")
        
        response = requests.get(
            f"{BASE_URL}/locations/{location_id}",
            headers=self.get_headers(self.admin_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("id"), location_id)
    
    # --- Appointment API Tests ---
    def test_11_create_appointment(self):
        """Test creating an appointment"""
        customer_id = self.test_data.get("customer_id")
        location_id = self.test_data.get("location_id")
        self.assertIsNotNone(customer_id, "Customer ID not set from previous test")
        self.assertIsNotNone(location_id, "Location ID not set from previous test")
        
        # Create appointment for tomorrow
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        appointment_data = {
            "customer_id": customer_id,
            "location_id": location_id,
            "scheduled_start_datetime": f"{tomorrow}T10:00:00",
            "scheduled_end_datetime": f"{tomorrow}T12:00:00",
            "service_type": "Lawn Mowing",
            "status": "scheduled",
            "notes": "Test appointment created by automated tests"
        }
        
        response = requests.post(
            f"{BASE_URL}/appointments",
            headers=self.get_headers(self.admin_token),
            json=appointment_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save appointment ID for later tests
        self.test_data["appointment_id"] = response.json().get("id")
    
    def test_12_get_appointments(self):
        """Test getting all appointments"""
        response = requests.get(
            f"{BASE_URL}/appointments",
            headers=self.get_headers(self.admin_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    def test_13_get_appointment(self):
        """Test getting a specific appointment"""
        appointment_id = self.test_data.get("appointment_id")
        self.assertIsNotNone(appointment_id, "Appointment ID not set from previous test")
        
        response = requests.get(
            f"{BASE_URL}/appointments/{appointment_id}",
            headers=self.get_headers(self.admin_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("id"), appointment_id)
    
    def test_14_update_appointment(self):
        """Test updating an appointment"""
        appointment_id = self.test_data.get("appointment_id")
        self.assertIsNotNone(appointment_id, "Appointment ID not set from previous test")
        
        # Update to the day after tomorrow
        day_after_tomorrow = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        updated_data = {
            "scheduled_start_datetime": f"{day_after_tomorrow}T14:00:00",
            "scheduled_end_datetime": f"{day_after_tomorrow}T16:00:00",
            "notes": "Updated by automated tests"
        }
        
        response = requests.put(
            f"{BASE_URL}/appointments/{appointment_id}",
            headers=self.get_headers(self.admin_token),
            json=updated_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated by automated tests", response.json().get("notes"))
    
    # --- Quote API Tests ---
    def test_15_create_quote(self):
        """Test creating a quote"""
        employee_id = self.test_data.get("employee_id")
        appointment_id = self.test_data.get("appointment_id")
        self.assertIsNotNone(employee_id, "Employee ID not set from previous test")
        self.assertIsNotNone(appointment_id, "Appointment ID not set from previous test")
        
        quote_data = {
            "employee_id": employee_id,
            "appointment_id": appointment_id,
            "service_description": "Full Yard Service",
            "estimate": 150.00,
            "valid_until": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "notes": "Test quote created by automated tests"
        }
        
        response = requests.post(
            f"{BASE_URL}/quotes",
            headers=self.get_headers(self.admin_token),
            json=quote_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save quote ID for later tests
        self.test_data["quote_id"] = response.json().get("id")
    
    def test_16_get_quotes(self):
        """Test getting all quotes"""
        response = requests.get(
            f"{BASE_URL}/quotes",
            headers=self.get_headers(self.admin_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    # --- Invoice API Tests ---
    def test_17_create_invoice(self):
        """Test creating an invoice"""
        appointment_id = self.test_data.get("appointment_id")
        self.assertIsNotNone(appointment_id, "Appointment ID not set from previous test")
        
        # Calculate some example values
        subtotal = 125.00
        tax_rate = 0.07
        total = subtotal * (1 + tax_rate)
        
        invoice_data = {
            "appointment_id": appointment_id,
            "subtotal": subtotal,
            "total": total,
            "tax_rate": tax_rate,
            "status": "draft",
            "due_date": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
            "notes": "Test invoice created by automated tests",
            "customer_name": "Test Customer",
            "invoice_number": f"INV-{datetime.now().strftime('%Y%m%d')}-001"
        }
        
        response = requests.post(
            f"{BASE_URL}/invoices",
            headers=self.get_headers(self.admin_token),
            json=invoice_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save invoice ID for later tests
        self.test_data["invoice_id"] = response.json().get("id")
    
    def test_18_get_invoices(self):
        """Test getting all invoices"""
        response = requests.get(
            f"{BASE_URL}/invoices",
            headers=self.get_headers(self.admin_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    def test_18a_create_invoice_item(self):
        """Test creating an invoice item"""
        invoice_id = self.test_data.get("invoice_id")
        self.assertIsNotNone(invoice_id, "Invoice ID not set from previous test")
        
        # For testing purposes, we'll use service_id=1
        # In a real scenario, you might want to create a service first
        service_id = 1
        
        invoice_item_data = {
            "invoice_id": invoice_id,
            "service_id": service_id,
            "cost": 75.50,
            "description": "Lawn mowing service"
        }
        
        response = requests.post(
            f"{BASE_URL}/invoices/{invoice_id}/items",
            headers=self.get_headers(self.admin_token),
            json=invoice_item_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save invoice item ID for later tests
        self.test_data["invoice_item_id"] = response.json().get("id")
        self.assertEqual(response.json().get("cost"), invoice_item_data["cost"])
    
    def test_18b_get_invoice_items(self):
        """Test getting all items for an invoice"""
        invoice_id = self.test_data.get("invoice_id")
        self.assertIsNotNone(invoice_id, "Invoice ID not set from previous test")
        
        response = requests.get(
            f"{BASE_URL}/invoices/{invoice_id}/items",
            headers=self.get_headers(self.admin_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertTrue(len(response.json()) > 0, "No items found for the invoice")
    
    # --- Equipment API Tests ---
    def test_19_create_equipment(self):
        """Test creating equipment"""
        # Get employee ID for purchased_by field
        employee_id = self.test_data.get("employee_id", 1)  # Default to first employee if not set
        
        # Run the equipment category test first if it hasn't been run yet
        if "equipment_category_id" not in self.test_data:
            self.test_20a_create_equipment_category()
            
        # Use the category ID from our created category
        category_id = self.test_data.get("equipment_category_id", 1)
        
        equipment_data = {
            "name": f"Test Mower {self.generate_random_string()}",
            "purchased_date": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
            "purchased_condition": "New",
            "warranty_expiration_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "manufacturer": "TestMakers Inc.",
            "model": "LawnPro 3000",
            "equipment_category_id": category_id,
            "purchase_price": 599.99,
            "repair_cost_to_date": 0.0,
            "purchased_by": employee_id
        }
        
        response = requests.post(
            f"{BASE_URL}/equipment",
            headers=self.get_headers(self.admin_token),
            json=equipment_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save equipment ID for later tests
        self.test_data["equipment_id"] = response.json().get("id")
    
    def test_20_get_equipment(self):
        """Test getting all equipment"""
        response = requests.get(
            f"{BASE_URL}/equipment",
            headers=self.get_headers(self.admin_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    def test_20a_create_equipment_category(self):
        """Test creating an equipment category"""
        category_data = {
            "name": f"Test Category {self.generate_random_string()}"
        }
        
        response = requests.post(
            f"{BASE_URL}/equipment/categories",
            headers=self.get_headers(self.admin_token),
            json=category_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save category ID for later tests
        self.test_data["equipment_category_id"] = response.json().get("id")
        self.assertEqual(response.json().get("name"), category_data["name"])
    
    def test_20b_get_equipment_categories(self):
        """Test getting all equipment categories"""
        response = requests.get(
            f"{BASE_URL}/equipment/categories",
            headers=self.get_headers(self.admin_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        
        # Verify our created category is in the list
        category_id = self.test_data.get("equipment_category_id")
        if category_id:
            category_found = False
            for category in response.json():
                if category.get("id") == category_id:
                    category_found = True
                    break
            self.assertTrue(category_found, "Created category not found in the list")
    
    # --- Reviews API Tests ---
    def test_21_create_review(self):
        """Test creating a review"""
        customer_id = self.test_data.get("customer_id")
        self.assertIsNotNone(customer_id, "Customer ID not set from previous test")
        
        review_data = {
            "customer_id": customer_id,
            "rating": 4,
            "comments": "Great service, highly recommended!",
            "review_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        response = requests.post(
            f"{BASE_URL}/reviews",
            headers=self.get_headers(self.admin_token),
            json=review_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save review ID for later tests
        self.test_data["review_id"] = response.json().get("id")
    
    def test_22_get_reviews(self):
        """Test getting all reviews"""
        response = requests.get(
            f"{BASE_URL}/reviews",
            headers=self.get_headers(self.admin_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    # --- Timelogs API Tests ---
    def test_23_create_timelog(self):
        """Test creating a timelog"""
        employee_id = 1  # Assuming there's an employee with ID 1
        appointment_id = self.test_data.get("appointment_id")
        self.assertIsNotNone(appointment_id, "Appointment ID not set from previous test")
        
        timelog_data = {
            "employee_id": employee_id,
            "appointment_id": appointment_id,
            "start_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "end_time": (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S"),
            "notes": "Test timelog created by automated tests"
        }
        
        response = requests.post(
            f"{BASE_URL}/timelogs",
            headers=self.get_headers(self.admin_token),
            json=timelog_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save timelog ID for later tests
        self.test_data["timelog_id"] = response.json().get("id")
    
    def test_24_get_timelogs(self):
        """Test getting all timelogs"""
        response = requests.get(
            f"{BASE_URL}/timelogs",
            headers=self.get_headers(self.admin_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    # --- Photos API Tests ---
    def test_25_upload_photo(self):
        """Test uploading a photo (mock)"""
        # Since we can't easily upload a real file in this test, we'll mock it
        # In a real test, you would use requests.post with files parameter
        print("Photo upload test would go here (requires multipart file upload)")

    # --- Employees API Tests ---
    def test_26_get_employees(self):
        """Test getting all employees"""
        response = requests.get(
            f"{BASE_URL}/employees",
            headers=self.get_headers(self.lead_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        
    def test_27_create_employee(self):
        """Test creating a new employee"""
        employee_data = {
            "name": f"Test Employee {self.generate_random_string()}",
            "email": f"employee.{self.generate_random_string()}@example.com",
            "phone": f"+1{self.generate_random_string(10)}",
            "team": "Installation",
            "role": "employee",
            "password": "testpassword123"
        }
        
        response = requests.post(
            f"{BASE_URL}/employees",
            headers=self.get_headers(self.admin_token),
            json=employee_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save employee ID for later tests
        self.test_data["test_employee_id"] = response.json().get("id")
        self.assertEqual(response.json().get("name"), employee_data["name"])
    
    def test_28_get_employee(self):
        """Test getting a specific employee"""
        employee_id = self.test_data.get("test_employee_id")
        self.assertIsNotNone(employee_id, "Employee ID not set from previous test")
        
        response = requests.get(
            f"{BASE_URL}/employees/{employee_id}",
            headers=self.get_headers(self.lead_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("id"), employee_id)
    
    def test_29_update_employee(self):
        """Test updating an employee"""
        employee_id = self.test_data.get("test_employee_id")
        self.assertIsNotNone(employee_id, "Employee ID not set from previous test")
        
        updated_data = {
            "team": "Maintenance",
            "phone": f"+1{self.generate_random_string(10)}"
        }
        
        response = requests.put(
            f"{BASE_URL}/employees/{employee_id}",
            headers=self.get_headers(self.admin_token),
            json=updated_data
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify update
        response = requests.get(
            f"{BASE_URL}/employees/{employee_id}",
            headers=self.get_headers(self.admin_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("team"), updated_data["team"])

    # --- Customer Portal Tests ---
    def test_30_customer_registration(self):
        """Test customer registration"""
        customer_data = {
            "name": f"Portal Customer {self.generate_random_string()}",
            "email": f"portal.{self.generate_random_string()}@example.com",
            "phone": f"+1{self.generate_random_string(10)}",
            "password": "securepassword123"
        }
        
        response = requests.post(
            f"{BASE_URL}/customer_portal/register",
            json=customer_data
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("successfully", response.json().get("msg", ""))
        
        # Save credentials for login test
        self.test_data["portal_customer_email"] = customer_data["email"]
        self.test_data["portal_customer_password"] = customer_data["password"]
    
    def test_31_customer_login(self):
        """Test customer login"""
        login_data = {
            "email": self.test_data.get("portal_customer_email"),
            "password": self.test_data.get("portal_customer_password")
        }
        
        response = requests.post(
            f"{BASE_URL}/customer_portal/login",
            json=login_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        
        # Save customer token for later tests
        self.test_data["customer_token"] = response.json().get("access_token")
    
    def test_32_get_customer_profile(self):
        """Test getting customer profile"""
        customer_token = self.test_data.get("customer_token")
        self.assertIsNotNone(customer_token, "Customer token not set from previous test")
        
        response = requests.get(
            f"{BASE_URL}/customer_portal/profile",
            headers=self.get_headers(customer_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("email"), self.test_data.get("portal_customer_email"))
    
    def test_33_update_customer_profile(self):
        """Test updating customer profile"""
        customer_token = self.test_data.get("customer_token")
        self.assertIsNotNone(customer_token, "Customer token not set from previous test")
        
        updated_data = {
            "name": f"Updated Portal Customer {self.generate_random_string()}",
            "phone": f"+1{self.generate_random_string(10)}"
        }
        
        response = requests.put(
            f"{BASE_URL}/customer_portal/profile",
            headers=self.get_headers(customer_token),
            json=updated_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("name"), updated_data["name"])
    
    # --- Payments API Tests ---
    def test_34_create_payment(self):
        """Test creating a payment for an invoice"""
        invoice_id = self.test_data.get("invoice_id")
        self.assertIsNotNone(invoice_id, "Invoice ID not set from previous test")
        
        payment_data = {
            "invoice_id": invoice_id,
            "amount": 50.00,
            "payment_date": datetime.now().strftime("%Y-%m-%d"),
            "payment_method": "credit_card",
            "reference_number": f"REF-{self.generate_random_string(8)}",
            "notes": "Test payment created by automated tests"
        }
        
        response = requests.post(
            f"{BASE_URL}/payments",
            headers=self.get_headers(self.lead_token),
            json=payment_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save payment ID for later tests
        self.test_data["payment_id"] = response.json().get("id")
    
    def test_35_get_payment(self):
        """Test getting a specific payment"""
        payment_id = self.test_data.get("payment_id")
        self.assertIsNotNone(payment_id, "Payment ID not set from previous test")
        
        response = requests.get(
            f"{BASE_URL}/payments/{payment_id}",
            headers=self.get_headers(self.employee_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("id"), payment_id)
    
    def test_36_get_invoice_payments(self):
        """Test getting all payments for an invoice"""
        invoice_id = self.test_data.get("invoice_id")
        self.assertIsNotNone(invoice_id, "Invoice ID not set from previous test")
        
        response = requests.get(
            f"{BASE_URL}/payments/invoice/{invoice_id}",
            headers=self.get_headers(self.employee_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertTrue(len(response.json()) > 0, "No payments found for invoice")
    
    def test_37_update_payment(self):
        """Test updating a payment"""
        payment_id = self.test_data.get("payment_id")
        self.assertIsNotNone(payment_id, "Payment ID not set from previous test")
        
        updated_data = {
            "amount": 75.00,
            "notes": "Updated payment by automated tests",
            "payment_method": "check"
        }
        
        response = requests.put(
            f"{BASE_URL}/payments/{payment_id}",
            headers=self.get_headers(self.lead_token),
            json=updated_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("amount"), updated_data["amount"])
        self.assertEqual(response.json().get("payment_method"), updated_data["payment_method"])
    
    # --- Integration API Tests ---
    def test_38_register_webhook(self):
        """Test registering a webhook"""
        webhook_data = {
            "webhook_url": f"https://example.com/webhook/{self.generate_random_string()}"
        }
        
        response = requests.post(
            f"{BASE_URL}/integrations/register_webhook",
            headers=self.get_headers(self.admin_token),
            json=webhook_data
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("Webhook registered", response.json().get("msg", ""))
    
    def test_39_test_event(self):
        """Test the webhook test event endpoint"""
        # For this test, we'll use an API key header (normally used by integration partners)
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": os.getenv("API_KEY", "test_api_key")
        }
        
        response = requests.get(
            f"{BASE_URL}/integrations/test_event",
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("event", response.json())
        self.assertIn("data", response.json())
    
    def test_40_receive_webhook(self):
        """Test receiving a webhook event from external system"""
        # For this test, we'll use an API key header (normally used by integration partners)
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": os.getenv("API_KEY", "test_api_key")
        }
        
        webhook_event = {
            "event_type": "external.update",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "appointment_id": self.test_data.get("appointment_id"),
                "status": "completed",
                "notes": "Completed by external system"
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/integrations/webhook",
            headers=headers,
            json=webhook_event
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Webhook event received", response.json().get("msg", ""))

    # --- Testing Access Control ---
    def test_41_employee_access_control(self):
        """Test employee access control for admin-only endpoints"""
        # Attempt to create an employee as a regular employee (should fail)
        employee_data = {
            "name": f"Unauthorized Employee {self.generate_random_string()}",
            "email": f"unauth.{self.generate_random_string()}@example.com",
            "phone": f"+1{self.generate_random_string(10)}",
            "team": "Test",
            "role": "employee",
            "password": "password123"
        }
        
        response = requests.post(
            f"{BASE_URL}/employees",
            headers=self.get_headers(self.employee_token),
            json=employee_data
        )
        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)
    
    def test_42_lead_access_control(self):
        """Test lead access control for admin-only endpoints"""
        # Attempt to delete an employee as a lead (should fail)
        employee_id = self.test_data.get("test_employee_id")
        self.assertIsNotNone(employee_id, "Employee ID not set from previous test")
        
        response = requests.delete(
            f"{BASE_URL}/employees/{employee_id}",
            headers=self.get_headers(self.lead_token)
        )
        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)
    
    # --- Photos Extended Tests ---
    def test_43_get_photos_for_appointment(self):
        """Test getting photos for a specific appointment"""
        appointment_id = self.test_data.get("appointment_id")
        self.assertIsNotNone(appointment_id, "Appointment ID not set from previous test")
        
        response = requests.get(
            f"{BASE_URL}/photos/appointment/{appointment_id}",
            headers=self.get_headers(self.employee_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    # --- Cleanup Tests ---
    def test_90_delete_payment(self):
        """Test deleting a payment"""
        payment_id = self.test_data.get("payment_id")
        if payment_id:
            response = requests.delete(
                f"{BASE_URL}/payments/{payment_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_91_delete_employee(self):
        """Test deleting an employee"""
        employee_id = self.test_data.get("test_employee_id")
        if employee_id:
            response = requests.delete(
                f"{BASE_URL}/employees/{employee_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_92_delete_timelog(self):
        """Test deleting a timelog"""
        timelog_id = self.test_data.get("timelog_id")
        if timelog_id:
            response = requests.delete(
                f"{BASE_URL}/timelogs/{timelog_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_93_delete_review(self):
        """Test deleting a review"""
        review_id = self.test_data.get("review_id")
        if review_id:
            response = requests.delete(
                f"{BASE_URL}/reviews/{review_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_93a_delete_invoice_item(self):
        """Test deleting an invoice item"""
        invoice_item_id = self.test_data.get("invoice_item_id")
        invoice_id = self.test_data.get("invoice_id")
        if invoice_item_id and invoice_id:
            response = requests.delete(
                f"{BASE_URL}/invoices/items/{invoice_item_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_94_delete_invoice(self):
        """Test deleting an invoice"""
        invoice_id = self.test_data.get("invoice_id")
        if invoice_id:
            response = requests.delete(
                f"{BASE_URL}/invoices/{invoice_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_95_delete_quote(self):
        """Test deleting a quote"""
        quote_id = self.test_data.get("quote_id")
        if quote_id:
            response = requests.delete(
                f"{BASE_URL}/quotes/{quote_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_96_delete_appointment(self):
        """Test deleting an appointment"""
        appointment_id = self.test_data.get("appointment_id")
        if appointment_id:
            response = requests.delete(
                f"{BASE_URL}/appointments/{appointment_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_97_delete_equipment(self):
        """Test deleting equipment"""
        equipment_id = self.test_data.get("equipment_id")
        if equipment_id:
            response = requests.delete(
                f"{BASE_URL}/equipment/{equipment_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_97a_delete_equipment_category(self):
        """Test deleting an equipment category"""
        category_id = self.test_data.get("equipment_category_id")
        if category_id:
            response = requests.delete(
                f"{BASE_URL}/equipment/categories/{category_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_98_delete_location(self):
        """Test deleting a location"""
        location_id = self.test_data.get("location_id")
        if location_id:
            response = requests.delete(
                f"{BASE_URL}/locations/{location_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_99_delete_customer(self):
        """Test deleting a customer"""
        customer_id = self.test_data.get("customer_id")
        if customer_id:
            response = requests.delete(
                f"{BASE_URL}/customers/{customer_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main(verbosity=2) 