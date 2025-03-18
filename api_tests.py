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
        cls.admin_password = os.getenv("ADMIN_PASSWORD", "adminpassword")
        
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
            f"{BASE_URL}/customers/",
            headers=self.get_headers(self.employee_token)
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
            f"{BASE_URL}/customers/",
            headers=self.get_headers(self.lead_token),
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
            headers=self.get_headers(self.employee_token)
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
            headers=self.get_headers(self.lead_token),
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
            f"{BASE_URL}/locations/",
            headers=self.get_headers(self.lead_token),
            json=location_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save location ID for later tests
        self.test_data["location_id"] = response.json().get("id")
    
    def test_09_get_locations(self):
        """Test getting all locations"""
        response = requests.get(
            f"{BASE_URL}/locations/",
            headers=self.get_headers(self.employee_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    def test_10_get_location(self):
        """Test getting a specific location"""
        location_id = self.test_data.get("location_id")
        self.assertIsNotNone(location_id, "Location ID not set from previous test")
        
        response = requests.get(
            f"{BASE_URL}/locations/{location_id}",
            headers=self.get_headers(self.employee_token)
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
            f"{BASE_URL}/appointments/",
            headers=self.get_headers(self.lead_token),
            json=appointment_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save appointment ID for later tests
        self.test_data["appointment_id"] = response.json().get("id")
    
    def test_12_get_appointments(self):
        """Test getting all appointments"""
        response = requests.get(
            f"{BASE_URL}/appointments/",
            headers=self.get_headers(self.employee_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    def test_13_get_appointment(self):
        """Test getting a specific appointment"""
        appointment_id = self.test_data.get("appointment_id")
        self.assertIsNotNone(appointment_id, "Appointment ID not set from previous test")
        
        response = requests.get(
            f"{BASE_URL}/appointments/{appointment_id}",
            headers=self.get_headers(self.employee_token)
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
            headers=self.get_headers(self.lead_token),
            json=updated_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated by automated tests", response.json().get("notes"))
    
    # --- Quote API Tests ---
    def test_15_create_quote(self):
        """Test creating a quote"""
        customer_id = self.test_data.get("customer_id")
        location_id = self.test_data.get("location_id")
        self.assertIsNotNone(customer_id, "Customer ID not set from previous test")
        self.assertIsNotNone(location_id, "Location ID not set from previous test")
        
        quote_data = {
            "customer_id": customer_id,
            "location_id": location_id,
            "service_description": "Full Yard Service",
            "price": 150.00,
            "valid_until": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "notes": "Test quote created by automated tests"
        }
        
        response = requests.post(
            f"{BASE_URL}/quotes/",
            headers=self.get_headers(self.lead_token),
            json=quote_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save quote ID for later tests
        self.test_data["quote_id"] = response.json().get("id")
    
    def test_16_get_quotes(self):
        """Test getting all quotes"""
        response = requests.get(
            f"{BASE_URL}/quotes/",
            headers=self.get_headers(self.lead_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    # --- Invoice API Tests ---
    def test_17_create_invoice(self):
        """Test creating an invoice"""
        customer_id = self.test_data.get("customer_id")
        appointment_id = self.test_data.get("appointment_id")
        self.assertIsNotNone(customer_id, "Customer ID not set from previous test")
        self.assertIsNotNone(appointment_id, "Appointment ID not set from previous test")
        
        invoice_data = {
            "customer_id": customer_id,
            "appointment_id": appointment_id,
            "amount": 125.00,
            "status": "pending",
            "due_date": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
            "description": "Lawn Service",
            "notes": "Test invoice created by automated tests"
        }
        
        response = requests.post(
            f"{BASE_URL}/invoices/",
            headers=self.get_headers(self.lead_token),
            json=invoice_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save invoice ID for later tests
        self.test_data["invoice_id"] = response.json().get("id")
    
    def test_18_get_invoices(self):
        """Test getting all invoices"""
        response = requests.get(
            f"{BASE_URL}/invoices/",
            headers=self.get_headers(self.lead_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    # --- Equipment API Tests ---
    def test_19_create_equipment(self):
        """Test creating equipment"""
        equipment_data = {
            "name": f"Test Mower {self.generate_random_string()}",
            "type": "Lawn Mower",
            "status": "active",
            "purchase_date": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
            "notes": "Test equipment created by automated tests"
        }
        
        response = requests.post(
            f"{BASE_URL}/equipment/",
            headers=self.get_headers(self.admin_token),
            json=equipment_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save equipment ID for later tests
        self.test_data["equipment_id"] = response.json().get("id")
    
    def test_20_get_equipment(self):
        """Test getting all equipment"""
        response = requests.get(
            f"{BASE_URL}/equipment/",
            headers=self.get_headers(self.employee_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
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
            f"{BASE_URL}/reviews/",
            headers=self.get_headers(self.lead_token),
            json=review_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save review ID for later tests
        self.test_data["review_id"] = response.json().get("id")
    
    def test_22_get_reviews(self):
        """Test getting all reviews"""
        response = requests.get(
            f"{BASE_URL}/reviews/",
            headers=self.get_headers(self.employee_token)
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
            f"{BASE_URL}/timelogs/",
            headers=self.get_headers(self.employee_token),
            json=timelog_data
        )
        self.assertEqual(response.status_code, 201)
        
        # Save timelog ID for later tests
        self.test_data["timelog_id"] = response.json().get("id")
    
    def test_24_get_timelogs(self):
        """Test getting all timelogs"""
        response = requests.get(
            f"{BASE_URL}/timelogs/",
            headers=self.get_headers(self.lead_token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    # --- Photos API Tests ---
    def test_25_upload_photo(self):
        """Test uploading a photo (mock)"""
        # Since we can't easily upload a real file in this test, we'll mock it
        # In a real test, you would use requests.post with files parameter
        print("Photo upload test would go here (requires multipart file upload)")
    
    # --- Cleanup Tests ---
    def test_90_delete_timelog(self):
        """Test deleting a timelog"""
        timelog_id = self.test_data.get("timelog_id")
        if timelog_id:
            response = requests.delete(
                f"{BASE_URL}/timelogs/{timelog_id}",
                headers=self.get_headers(self.lead_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_91_delete_review(self):
        """Test deleting a review"""
        review_id = self.test_data.get("review_id")
        if review_id:
            response = requests.delete(
                f"{BASE_URL}/reviews/{review_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_92_delete_invoice(self):
        """Test deleting an invoice"""
        invoice_id = self.test_data.get("invoice_id")
        if invoice_id:
            response = requests.delete(
                f"{BASE_URL}/invoices/{invoice_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_93_delete_quote(self):
        """Test deleting a quote"""
        quote_id = self.test_data.get("quote_id")
        if quote_id:
            response = requests.delete(
                f"{BASE_URL}/quotes/{quote_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_94_delete_appointment(self):
        """Test deleting an appointment"""
        appointment_id = self.test_data.get("appointment_id")
        if appointment_id:
            response = requests.delete(
                f"{BASE_URL}/appointments/{appointment_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_95_delete_equipment(self):
        """Test deleting equipment"""
        equipment_id = self.test_data.get("equipment_id")
        if equipment_id:
            response = requests.delete(
                f"{BASE_URL}/equipment/{equipment_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_96_delete_location(self):
        """Test deleting a location"""
        location_id = self.test_data.get("location_id")
        if location_id:
            response = requests.delete(
                f"{BASE_URL}/locations/{location_id}",
                headers=self.get_headers(self.admin_token)
            )
            self.assertEqual(response.status_code, 200)
    
    def test_97_delete_customer(self):
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