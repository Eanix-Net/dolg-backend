# models.py
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

# ---------- Phase 1 Models ----------
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    team = db.Column(db.String(128))
    role = db.Column(db.String(64))  # e.g., 'admin', 'lead', 'employee'
    
    def set_password(self, password):
        """Set the password hash from a plaintext password"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Check if the provided password matches the stored hash"""
        return check_password_hash(self.password_hash, password)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20)) 
    email = db.Column(db.String(128), unique=True, nullable=False) 
    password_hash = db.Column(db.String(128))  # For future customer login support   
    notes = db.Column(db.Text) 
    created_datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)   
    locations = db.relationship('CustomerLocation', backref='customer', lazy=True)

class CustomerLocation(db.Model):  
    __tablename__ = 'customer_locations'
    id = db.Column(db.Integer, primary_key=True)  
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)  
    address = db.Column(db.String(256))  
    point_of_contact = db.Column(db.String(128)) 
    property_type = db.Column(db.String(64))  # Business or Residential 
    approx_acres = db.Column(db.Float)  
    notes = db.Column(db.Text)

# ---------- Unlimited Services (self-hosted) ----------
class Service(db.Model): 
    __tablename__ = 'services' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text) 
    invoice_items = db.relationship('InvoiceItem', backref='service', lazy=True) 
    quote_items = db.relationship('QuoteItem', backref='service', lazy=True)

# ---------- Phase 2 Models (Scheduling/Appointments) ----------
class Appointment(db.Model):  
    __tablename__ = 'appointments' 
    id = db.Column(db.Integer, primary_key=True)
    customer_location_id = db.Column(db.Integer, db.ForeignKey('customer_locations.id'), nullable=False)
    arrival_datetime = db.Column(db.DateTime, nullable=False)
    departure_datetime = db.Column(db.DateTime, nullable=False)
    team = db.Column(db.String(128))
    location = db.relationship('CustomerLocation', backref='appointments')

class RecurringAppointment(db.Model):
    __tablename__ = 'recurring_appointments'
    id = db.Column(db.Integer, primary_key=True)
    customer_location_id = db.Column(db.Integer, db.ForeignKey('customer_locations.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    schedule = db.Column(db.String(128), nullable=False)  # e.g., "Every 3 weeks" or "First Monday of the month"
    team = db.Column(db.String(128))
    location = db.relationship('CustomerLocation', backref='recurring_appointments')

# ---------- Phase 3 Models (Invoicing & Quotes) ----------
class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, nullable=False)
    paid = db.Column(db.String(16), nullable=False, default='unpaid')  # Options: 'paid', 'unpaid', 'declined'
    attempt = db.Column(db.Integer, nullable=False, default=1)
    due_date = db.Column(db.Date, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    items = db.relationship('InvoiceItem', backref='invoice', lazy=True)

class InvoiceItem(db.Model):
    __tablename__ = 'invoice_items'
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    cost = db.Column(db.Float, nullable=False)

class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    estimate = db.Column(db.Float, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    items = db.relationship('QuoteItem', backref='quote', lazy=True)

class QuoteItem(db.Model):
    __tablename__ = 'quote_items'
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    cost = db.Column(db.Float, nullable=False)

# ---------- Phase 4 Models (Equipment, Reviews, Photos, Time Tracking) ----------
# Equipment Management
class EquipmentCategory(db.Model):
    __tablename__ = 'equipment_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    purchased_date = db.Column(db.Date)
    purchased_condition = db.Column(db.String(32))  # 'New' or 'Used'
    warranty_expiration_date = db.Column(db.Date)
    manufacturer = db.Column(db.String(128))
    model = db.Column(db.String(128))
    equipment_category_id = db.Column(db.Integer, db.ForeignKey('equipment_categories.id'))
    purchase_price = db.Column(db.Float)
    repair_cost_to_date = db.Column(db.Float, default=0.0)
    purchased_by = db.Column(db.String(128))
    fuel_type = db.Column(db.String(32))  # e.g., Gas, Diesel, Electric
    oil_type = db.Column(db.String(32))   # or None
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    category = db.relationship('EquipmentCategory', backref='equipment', lazy=True)
    assignments = db.relationship('EquipmentAssignment', backref='equipment', lazy=True)
    consumables = db.relationship('ConsumableUsage', backref='equipment', lazy=True)

class EquipmentAssignment(db.Model):
    __tablename__ = 'equipment_assignments'
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    team = db.Column(db.String(128))
    assigned_date = db.Column(db.Date, default=datetime.date.today)

class ConsumableUsage(db.Model):
    __tablename__ = 'consumable_usage'
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    consumable_type = db.Column(db.String(64))  # e.g., Gas, Oil, Diesel
    amount_used = db.Column(db.Float)           # in liters
    cost_per_liter = db.Column(db.Float)
    date_recorded = db.Column(db.Date, default=datetime.date.today)

# Customer Reviews
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('customer_locations.id'), nullable=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Before/After Photos
class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    file_path = db.Column(db.String(256), nullable=False)
    uploaded_by = db.Column(db.String(128))
    approved_by = db.Column(db.String(128))
    show_to_customer = db.Column(db.Boolean, default=False)
    show_on_website = db.Column(db.Boolean, default=False)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Job Time Tracking
class TimeLog(db.Model):
    __tablename__ = 'timelogs'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    time_in = db.Column(db.DateTime, nullable=False)
    time_out = db.Column(db.DateTime, nullable=True)
    total_time = db.Column(db.Float)  # e.g., total hours