"""
Utility module for Swagger documentation templates.
This module provides reusable Swagger documentation templates for common REST operations.
"""

# Authentication endpoints documentation
AUTH_LOGIN = {
    "tags": ["Authentication"],
    "description": "Login with employee credentials",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "example": "user@example.com"},
                    "password": {"type": "string", "example": "password123"}
                },
                "required": ["email", "password"]
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Login successful",
            "schema": {
                "type": "object",
                "properties": {
                    "access_token": {"type": "string"}
                }
            }
        },
        "400": {"description": "Email and password required"},
        "401": {"description": "Invalid email or password"}
    }
}

# Customer endpoints documentation
CUSTOMER_LIST = {
    "tags": ["Customers"],
    "description": "Get all customers",
    "security": [{"Bearer": []}],
    "responses": {
        "200": {
            "description": "List of customers",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "phone": {"type": "string"},
                        "email": {"type": "string"},
                        "notes": {"type": "string"},
                        "created_datetime": {"type": "string", "format": "date-time"}
                    }
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

CUSTOMER_CREATE = {
    "tags": ["Customers"],
    "description": "Create a new customer",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "John Doe"},
                    "phone": {"type": "string", "example": "555-123-4567"},
                    "email": {"type": "string", "example": "john@example.com"},
                    "notes": {"type": "string", "example": "New residential customer"}
                },
                "required": ["name"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Customer created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "phone": {"type": "string"},
                    "email": {"type": "string"},
                    "notes": {"type": "string"},
                    "created_datetime": {"type": "string", "format": "date-time"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

CUSTOMER_GET = {
    "tags": ["Customers"],
    "description": "Get customer by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "customer_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the customer to retrieve"
        }
    ],
    "responses": {
        "200": {
            "description": "Customer details",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "phone": {"type": "string"},
                    "email": {"type": "string"},
                    "notes": {"type": "string"},
                    "created_datetime": {"type": "string", "format": "date-time"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Customer not found"}
    }
}

CUSTOMER_UPDATE = {
    "tags": ["Customers"],
    "description": "Update customer by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "customer_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the customer to update"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "John Smith"},
                    "phone": {"type": "string", "example": "555-987-6543"},
                    "email": {"type": "string", "example": "john.smith@example.com"},
                    "notes": {"type": "string", "example": "Updated notes"}
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Customer updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "phone": {"type": "string"},
                    "email": {"type": "string"},
                    "notes": {"type": "string"},
                    "created_datetime": {"type": "string", "format": "date-time"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Customer not found"}
    }
}

CUSTOMER_DELETE = {
    "tags": ["Customers"],
    "description": "Delete customer by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "customer_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the customer to delete"
        }
    ],
    "responses": {
        "200": {
            "description": "Customer deleted successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Customer deleted"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Customer not found"}
    }
}

# Employees endpoints documentation
EMPLOYEES_LIST = {
    "tags": ["Employees"],
    "description": "Get all employees",
    "security": [{"Bearer": []}],
    "responses": {
        "200": {
            "description": "List of employees",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "role": {"type": "string", "enum": ["admin", "lead", "employee"]},
                        "created_datetime": {"type": "string", "format": "date-time"}
                    }
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

EMPLOYEES_CREATE = {
    "tags": ["Employees"],
    "description": "Create a new employee",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Jane Smith"},
                    "email": {"type": "string", "example": "jane@example.com"},
                    "password": {"type": "string", "example": "securepassword"},
                    "role": {"type": "string", "enum": ["admin", "lead", "employee"], "example": "employee"}
                },
                "required": ["name", "email", "password", "role"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Employee created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "role": {"type": "string"},
                    "created_datetime": {"type": "string", "format": "date-time"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

# Appointments endpoints documentation
APPOINTMENTS_LIST = {
    "tags": ["Appointments"],
    "description": "Get all appointments",
    "security": [{"Bearer": []}],
    "responses": {
        "200": {
            "description": "List of appointments",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "customer_id": {"type": "integer"},
                        "description": {"type": "string"},
                        "start_time": {"type": "string", "format": "date-time"},
                        "end_time": {"type": "string", "format": "date-time"},
                        "status": {"type": "string", "enum": ["scheduled", "completed", "cancelled"]},
                        "created_datetime": {"type": "string", "format": "date-time"}
                    }
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

# Invoices endpoints documentation
INVOICES_LIST = {
    "tags": ["Invoices"],
    "description": "Get all invoices",
    "security": [{"Bearer": []}],
    "responses": {
        "200": {
            "description": "List of invoices",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "customer_id": {"type": "integer"},
                        "appointment_id": {"type": "integer"},
                        "total_amount": {"type": "number", "format": "float"},
                        "status": {"type": "string", "enum": ["draft", "sent", "paid", "overdue"]},
                        "due_date": {"type": "string", "format": "date"},
                        "created_datetime": {"type": "string", "format": "date-time"}
                    }
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

# Customer Location endpoints documentation
LOCATION_LIST = {
    "tags": ["Locations"],
    "description": "Get all locations for a customer",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "customer_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the customer to retrieve locations for"
        }
    ],
    "responses": {
        "200": {
            "description": "List of locations for the customer",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "customer_id": {"type": "integer"},
                        "address": {"type": "string"},
                        "city": {"type": "string"},
                        "state": {"type": "string"},
                        "zip_code": {"type": "string"},
                        "point_of_contact": {"type": "string"},
                        "property_type": {"type": "string"},
                        "approx_acres": {"type": "number", "format": "float"},
                        "notes": {"type": "string"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"}
                    }
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Customer not found"}
    }
}

LOCATION_CREATE = {
    "tags": ["Locations"],
    "description": "Create a new location for a customer",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "integer", "example": 1},
                    "address": {"type": "string", "example": "123 Main St"},
                    "city": {"type": "string", "example": "Anytown"},
                    "state": {"type": "string", "example": "CA"},
                    "zip_code": {"type": "string", "example": "12345"},
                    "point_of_contact": {"type": "string", "example": "John Smith"},
                    "property_type": {"type": "string", "example": "Residential"},
                    "approx_acres": {"type": "number", "format": "float", "example": 0.5},
                    "notes": {"type": "string", "example": "Front lawn and backyard"}
                },
                "required": ["customer_id", "address"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Location created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "customer_id": {"type": "integer"},
                    "address": {"type": "string"},
                    "city": {"type": "string"},
                    "state": {"type": "string"},
                    "zip_code": {"type": "string"},
                    "point_of_contact": {"type": "string"},
                    "property_type": {"type": "string"},
                    "approx_acres": {"type": "number", "format": "float"},
                    "notes": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Customer not found"}
    }
}

LOCATION_GET = {
    "tags": ["Locations"],
    "description": "Get location by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "location_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the location to retrieve"
        }
    ],
    "responses": {
        "200": {
            "description": "Location details",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "customer_id": {"type": "integer"},
                    "address": {"type": "string"},
                    "city": {"type": "string"},
                    "state": {"type": "string"},
                    "zip_code": {"type": "string"},
                    "point_of_contact": {"type": "string"},
                    "property_type": {"type": "string"},
                    "approx_acres": {"type": "number", "format": "float"},
                    "notes": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Location not found"}
    }
}

LOCATION_UPDATE = {
    "tags": ["Locations"],
    "description": "Update location by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "location_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the location to update"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "address": {"type": "string", "example": "456 Oak St"},
                    "city": {"type": "string", "example": "New City"},
                    "state": {"type": "string", "example": "NY"},
                    "zip_code": {"type": "string", "example": "54321"},
                    "notes": {"type": "string", "example": "Updated notes about the property"}
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Location updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "customer_id": {"type": "integer"},
                    "address": {"type": "string"},
                    "city": {"type": "string"},
                    "state": {"type": "string"},
                    "zip_code": {"type": "string"},
                    "notes": {"type": "string"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Location not found"}
    }
}

LOCATION_DELETE = {
    "tags": ["Locations"],
    "description": "Delete location by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "location_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the location to delete"
        }
    ],
    "responses": {
        "200": {
            "description": "Location deleted successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Location deleted"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Location not found"}
    }
}

# Generic templates for CRUD operations
def get_list_docs(tag_name, entity_name, schema_properties):
    """Generate Swagger docs for listing entities"""
    return {
        "tags": [tag_name],
        "description": f"Get all {entity_name}",
        "security": [{"Bearer": []}],
        "responses": {
            "200": {
                "description": f"List of {entity_name}",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": schema_properties
                    }
                }
            },
            "401": {"description": "Unauthorized"},
            "403": {"description": "Forbidden - Insufficient permissions"}
        }
    }

def get_create_docs(tag_name, entity_name, request_schema, response_schema):
    """Generate Swagger docs for creating entities"""
    return {
        "tags": [tag_name],
        "description": f"Create a new {entity_name}",
        "security": [{"Bearer": []}],
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": request_schema
                }
            }
        ],
        "responses": {
            "201": {
                "description": f"{entity_name} created successfully",
                "schema": {
                    "type": "object",
                    "properties": response_schema
                }
            },
            "400": {"description": "Invalid input"},
            "401": {"description": "Unauthorized"},
            "403": {"description": "Forbidden - Insufficient permissions"}
        }
    }

def get_detail_docs(tag_name, entity_name, entity_id_name, schema_properties):
    """Generate Swagger docs for getting entity details"""
    return {
        "tags": [tag_name],
        "description": f"Get {entity_name} by ID",
        "security": [{"Bearer": []}],
        "parameters": [
            {
                "name": entity_id_name,
                "in": "path",
                "required": True,
                "type": "integer",
                "description": f"ID of the {entity_name} to retrieve"
            }
        ],
        "responses": {
            "200": {
                "description": f"{entity_name} details",
                "schema": {
                    "type": "object",
                    "properties": schema_properties
                }
            },
            "401": {"description": "Unauthorized"},
            "403": {"description": "Forbidden - Insufficient permissions"},
            "404": {"description": f"{entity_name} not found"}
        }
    }

def get_update_docs(tag_name, entity_name, entity_id_name, request_schema, response_schema):
    """Generate Swagger docs for updating entities"""
    return {
        "tags": [tag_name],
        "description": f"Update {entity_name} by ID",
        "security": [{"Bearer": []}],
        "parameters": [
            {
                "name": entity_id_name,
                "in": "path",
                "required": True,
                "type": "integer",
                "description": f"ID of the {entity_name} to update"
            },
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": request_schema
                }
            }
        ],
        "responses": {
            "200": {
                "description": f"{entity_name} updated successfully",
                "schema": {
                    "type": "object",
                    "properties": response_schema
                }
            },
            "400": {"description": "Invalid input"},
            "401": {"description": "Unauthorized"},
            "403": {"description": "Forbidden - Insufficient permissions"},
            "404": {"description": f"{entity_name} not found"}
        }
    }

def get_delete_docs(tag_name, entity_name, entity_id_name):
    """Generate Swagger docs for deleting entities"""
    return {
        "tags": [tag_name],
        "description": f"Delete {entity_name} by ID",
        "security": [{"Bearer": []}],
        "parameters": [
            {
                "name": entity_id_name,
                "in": "path",
                "required": True,
                "type": "integer",
                "description": f"ID of the {entity_name} to delete"
            }
        ],
        "responses": {
            "200": {
                "description": f"{entity_name} deleted successfully",
                "schema": {
                    "type": "object",
                    "properties": {
                        "msg": {"type": "string", "example": f"{entity_name} deleted"}
                    }
                }
            },
            "401": {"description": "Unauthorized"},
            "403": {"description": "Forbidden - Insufficient permissions"},
            "404": {"description": f"{entity_name} not found"}
        }
    }

# Dynamic Documentation Generation
# These variables will be filled programmatically by the add_swagger_docs.py script
# They follow the naming convention: <BLUEPRINT>_<ROUTE>_<METHOD>

# AUTH endpoints
AUTH_LOGIN_POST = AUTH_LOGIN

# EMPLOYEES endpoints
EMPLOYEES_GET = EMPLOYEES_LIST
EMPLOYEES_POST = EMPLOYEES_CREATE

# LOCATIONS endpoints
LOCATIONS_GET = get_list_docs("Locations", "locations", {
    "id": {"type": "integer"},
    "customer_id": {"type": "integer"},
    "address": {"type": "string"},
    "city": {"type": "string"},
    "state": {"type": "string"},
    "zip_code": {"type": "string"},
    "created_datetime": {"type": "string", "format": "date-time"}
})

# APPOINTMENTS endpoints
APPOINTMENTS_GET = APPOINTMENTS_LIST

# INVOICES endpoints
INVOICES_GET = INVOICES_LIST

# Define missing INVOICES_POST Swagger documentation
INVOICES_POST = {
    "tags": ["Invoices"],
    "description": "Create a new invoice",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "integer", "example": 1},
                    "appointment_id": {"type": "integer", "example": 1},
                    "due_date": {"type": "string", "format": "date", "example": "2025-04-21"},
                    "notes": {"type": "string", "example": "Invoice for lawn maintenance services"}
                },
                "required": ["customer_id"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Invoice created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "customer_id": {"type": "integer"},
                    "appointment_id": {"type": "integer"},
                    "total_amount": {"type": "number", "format": "float"},
                    "status": {"type": "string", "enum": ["draft", "sent", "paid", "overdue"]},
                    "due_date": {"type": "string", "format": "date"},
                    "created_datetime": {"type": "string", "format": "date-time"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

# Define missing INVOICES_INVOICE_ID_GET Swagger documentation
INVOICES_INVOICE_ID_GET = {
    "tags": ["Invoices"],
    "description": "Get invoice by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "invoice_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the invoice to retrieve"
        }
    ],
    "responses": {
        "200": {
            "description": "Invoice details",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "customer_id": {"type": "integer"},
                    "appointment_id": {"type": "integer"},
                    "total_amount": {"type": "number", "format": "float"},
                    "status": {"type": "string", "enum": ["draft", "sent", "paid", "overdue"]},
                    "due_date": {"type": "string", "format": "date"},
                    "created_datetime": {"type": "string", "format": "date-time"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "invoice_id": {"type": "integer"},
                                "description": {"type": "string"},
                                "quantity": {"type": "integer"},
                                "unit_price": {"type": "number", "format": "float"},
                                "amount": {"type": "number", "format": "float"}
                            }
                        }
                    }
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Invoice not found"}
    }
}

# Define missing INVOICES_INVOICE_ID_PUT Swagger documentation
INVOICES_INVOICE_ID_PUT = {
    "tags": ["Invoices"],
    "description": "Update invoice by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "invoice_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the invoice to update"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["draft", "sent", "paid", "overdue"]},
                    "due_date": {"type": "string", "format": "date"},
                    "notes": {"type": "string"}
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Invoice updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "customer_id": {"type": "integer"},
                    "appointment_id": {"type": "integer"},
                    "total_amount": {"type": "number", "format": "float"},
                    "status": {"type": "string", "enum": ["draft", "sent", "paid", "overdue"]},
                    "due_date": {"type": "string", "format": "date"},
                    "created_datetime": {"type": "string", "format": "date-time"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Invoice not found"}
    }
}

# Define missing INVOICES_INVOICE_ID_DELETE Swagger documentation
INVOICES_INVOICE_ID_DELETE = {
    "tags": ["Invoices"],
    "description": "Delete invoice by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "invoice_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the invoice to delete"
        }
    ],
    "responses": {
        "200": {
            "description": "Invoice deleted successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Invoice deleted"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Invoice not found"}
    }
}

# Define missing INVOICES_INVOICE_ID_POST Swagger documentation for invoice items
INVOICES_INVOICE_ID_POST = {
    "tags": ["Invoice Items"],
    "description": "Create a new invoice item for an invoice",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "invoice_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the invoice to add an item to"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "example": "Lawn mowing service"},
                    "quantity": {"type": "integer", "example": 1},
                    "unit_price": {"type": "number", "format": "float", "example": 75.00}
                },
                "required": ["description", "quantity", "unit_price"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Invoice item created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "invoice_id": {"type": "integer"},
                    "description": {"type": "string"},
                    "quantity": {"type": "integer"},
                    "unit_price": {"type": "number", "format": "float"},
                    "amount": {"type": "number", "format": "float"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Invoice not found"}
    }
}

# Define missing INVOICES_ITEM_ID_PUT Swagger documentation
INVOICES_ITEM_ID_PUT = {
    "tags": ["Invoice Items"],
    "description": "Update an invoice item",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "item_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the invoice item to update"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "example": "Updated service description"},
                    "quantity": {"type": "integer", "example": 2},
                    "unit_price": {"type": "number", "format": "float", "example": 85.00}
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Invoice item updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "invoice_id": {"type": "integer"},
                    "description": {"type": "string"},
                    "quantity": {"type": "integer"},
                    "unit_price": {"type": "number", "format": "float"},
                    "amount": {"type": "number", "format": "float"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Invoice item not found"}
    }
}

# Define missing INVOICES_ITEM_ID_DELETE Swagger documentation
INVOICES_ITEM_ID_DELETE = {
    "tags": ["Invoice Items"],
    "description": "Delete an invoice item",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "item_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the invoice item to delete"
        }
    ],
    "responses": {
        "200": {
            "description": "Invoice item deleted successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Invoice item deleted"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Invoice item not found"}
    }
}

# TIMELOGS endpoints
TIMELOGS_GET = get_list_docs("Time Logs", "time logs", {
    "id": {"type": "integer"},
    "employee_id": {"type": "integer"},
    "appointment_id": {"type": "integer"},
    "start_time": {"type": "string", "format": "date-time"},
    "end_time": {"type": "string", "format": "date-time"},
    "description": {"type": "string"},
    "created_datetime": {"type": "string", "format": "date-time"}
})

# QUOTES endpoints documentation
QUOTES_GET = {
    "tags": ["Quotes"],
    "description": "Get all quotes",
    "security": [{"Bearer": []}],
    "responses": {
        "200": {
            "description": "List of quotes",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "appointment_id": {"type": "integer"},
                        "estimate": {"type": "number", "format": "float"},
                        "employee_id": {"type": "integer"},
                        "created_date": {"type": "string", "format": "date-time"}
                    }
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

QUOTES_POST = {
    "tags": ["Quotes"],
    "description": "Create a new quote",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "integer", "example": 1},
                    "estimate": {"type": "number", "format": "float", "example": 250.00},
                    "employee_id": {"type": "integer", "example": 1}
                },
                "required": ["appointment_id", "employee_id"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Quote created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "appointment_id": {"type": "integer"},
                    "estimate": {"type": "number", "format": "float"},
                    "employee_id": {"type": "integer"},
                    "created_date": {"type": "string", "format": "date-time"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

QUOTES_QUOTE_ID_GET = {
    "tags": ["Quotes"],
    "description": "Get quote by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "quote_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the quote to retrieve"
        }
    ],
    "responses": {
        "200": {
            "description": "Quote details",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "appointment_id": {"type": "integer"},
                    "estimate": {"type": "number", "format": "float"},
                    "employee_id": {"type": "integer"},
                    "created_date": {"type": "string", "format": "date-time"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Quote not found"}
    }
}

QUOTES_QUOTE_ID_PUT = {
    "tags": ["Quotes"],
    "description": "Update quote by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "quote_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the quote to update"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "estimate": {"type": "number", "format": "float", "example": 275.50}
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Quote updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "appointment_id": {"type": "integer"},
                    "estimate": {"type": "number", "format": "float"},
                    "employee_id": {"type": "integer"},
                    "created_date": {"type": "string", "format": "date-time"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Quote not found"}
    }
}

QUOTES_QUOTE_ID_DELETE = {
    "tags": ["Quotes"],
    "description": "Delete quote by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "quote_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the quote to delete"
        }
    ],
    "responses": {
        "200": {
            "description": "Quote deleted successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Quote deleted"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Quote not found"}
    }
}

QUOTES_QUOTE_ID_POST = {
    "tags": ["Quote Items"],
    "description": "Create a new quote item",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "quote_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the quote to add an item to"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "service_id": {"type": "integer", "example": 1},
                    "cost": {"type": "number", "format": "float", "example": 150.00}
                },
                "required": ["service_id", "cost"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Quote item created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "quote_id": {"type": "integer"},
                    "service_id": {"type": "integer"},
                    "cost": {"type": "number", "format": "float"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Quote not found"}
    }
}

QUOTES_ITEM_ID_PUT = {
    "tags": ["Quote Items"],
    "description": "Update a quote item",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "item_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the quote item to update"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "cost": {"type": "number", "format": "float", "example": 175.00}
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Quote item updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "quote_id": {"type": "integer"},
                    "service_id": {"type": "integer"},
                    "cost": {"type": "number", "format": "float"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Quote item not found"}
    }
}

QUOTES_ITEM_ID_DELETE = {
    "tags": ["Quote Items"],
    "description": "Delete a quote item",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "item_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the quote item to delete"
        }
    ],
    "responses": {
        "200": {
            "description": "Quote item deleted successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Quote item deleted"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Quote item not found"}
    }
}

# EQUIPMENT endpoints documentation
EQUIPMENT_CATEGORIES_GET = {
    "tags": ["Equipment Categories"],
    "description": "Get all equipment categories",
    "security": [{"Bearer": []}],
    "responses": {
        "200": {
            "description": "List of equipment categories",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"}
                    }
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

EQUIPMENT_CATEGORIES_POST = {
    "tags": ["Equipment Categories"],
    "description": "Create a new equipment category",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Power Tools"}
                },
                "required": ["name"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Category created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

EQUIPMENT_GET = {
    "tags": ["Equipment"],
    "description": "Get all equipment items",
    "security": [{"Bearer": []}],
    "responses": {
        "200": {
            "description": "List of equipment",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "purchased_date": {"type": "string", "format": "date"},
                        "purchased_condition": {"type": "string"},
                        "warranty_expiration_date": {"type": "string", "format": "date"},
                        "manufacturer": {"type": "string"},
                        "model": {"type": "string"},
                        "equipment_category_id": {"type": "integer"},
                        "purchase_price": {"type": "number", "format": "float"},
                        "repair_cost_to_date": {"type": "number", "format": "float"},
                        "purchased_by": {"type": "string"},
                        "fuel_type": {"type": "string"},
                        "oil_type": {"type": "string"},
                        "created_date": {"type": "string", "format": "date-time"}
                    }
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

EQUIPMENT_POST = {
    "tags": ["Equipment"],
    "description": "Create a new equipment item",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Lawn Mower"},
                    "purchased_date": {"type": "string", "format": "date", "example": "2023-01-15"},
                    "purchased_condition": {"type": "string", "example": "New"},
                    "warranty_expiration_date": {"type": "string", "format": "date", "example": "2025-01-15"},
                    "manufacturer": {"type": "string", "example": "Honda"},
                    "model": {"type": "string", "example": "HRX217K6VKA"},
                    "equipment_category_id": {"type": "integer", "example": 1},
                    "purchase_price": {"type": "number", "format": "float", "example": 599.99},
                    "repair_cost_to_date": {"type": "number", "format": "float", "example": 0.00},
                    "purchased_by": {"type": "string", "example": "John Doe"},
                    "fuel_type": {"type": "string", "example": "Gasoline"},
                    "oil_type": {"type": "string", "example": "SAE 10W-30"}
                },
                "required": ["name"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Equipment created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Equipment created"},
                    "equipment_id": {"type": "integer", "example": 1}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

EQUIPMENT_EQ_ID_GET = {
    "tags": ["Equipment"],
    "description": "Get equipment by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "eq_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the equipment to retrieve"
        }
    ],
    "responses": {
        "200": {
            "description": "Equipment details",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "purchased_date": {"type": "string", "format": "date"},
                    "purchased_condition": {"type": "string"},
                    "warranty_expiration_date": {"type": "string", "format": "date"},
                    "manufacturer": {"type": "string"},
                    "model": {"type": "string"},
                    "equipment_category_id": {"type": "integer"},
                    "purchase_price": {"type": "number", "format": "float"},
                    "repair_cost_to_date": {"type": "number", "format": "float"},
                    "purchased_by": {"type": "string"},
                    "fuel_type": {"type": "string"},
                    "oil_type": {"type": "string"},
                    "created_date": {"type": "string", "format": "date-time"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Equipment not found"}
    }
}

EQUIPMENT_EQ_ID_PUT = {
    "tags": ["Equipment"],
    "description": "Update equipment by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "eq_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the equipment to update"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Lawn Mower Pro"},
                    "purchased_date": {"type": "string", "format": "date"},
                    "purchased_condition": {"type": "string"},
                    "warranty_expiration_date": {"type": "string", "format": "date"},
                    "manufacturer": {"type": "string"},
                    "model": {"type": "string"},
                    "equipment_category_id": {"type": "integer"},
                    "purchase_price": {"type": "number", "format": "float"},
                    "repair_cost_to_date": {"type": "number", "format": "float"},
                    "purchased_by": {"type": "string"},
                    "fuel_type": {"type": "string"},
                    "oil_type": {"type": "string"}
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Equipment updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Equipment updated"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Equipment not found"}
    }
}

EQUIPMENT_EQ_ID_DELETE = {
    "tags": ["Equipment"],
    "description": "Delete equipment by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "eq_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the equipment to delete"
        }
    ],
    "responses": {
        "200": {
            "description": "Equipment deleted successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Equipment deleted"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Equipment not found"}
    }
}

EQUIPMENT_EQ_ID_POST = {
    "tags": ["Equipment Assignments"],
    "description": "Create a new equipment assignment or consumable usage record",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "eq_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the equipment"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "team": {"type": "string", "example": "Team A"},
                    "assigned_date": {"type": "string", "format": "date", "example": "2023-05-15"},
                    "consumable_type": {"type": "string", "example": "Fuel"},
                    "amount_used": {"type": "number", "format": "float", "example": 2.5},
                    "cost_per_liter": {"type": "number", "format": "float", "example": 1.5},
                    "date_recorded": {"type": "string", "format": "date", "example": "2023-05-20"}
                }
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Assignment or consumable usage created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Assignment created"},
                    "assignment_id": {"type": "integer"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Equipment not found"}
    }
}

# PAYMENTS endpoints documentation
PAYMENTS_POST = {
    "tags": ["Payments"],
    "description": "Create a new payment for an invoice",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "invoice_id": {"type": "integer", "example": 1},
                    "amount": {"type": "number", "format": "float", "example": 250.00},
                    "payment_date": {"type": "string", "format": "date-time", "example": "2023-04-15T14:30:00"},
                    "payment_method": {"type": "string", "example": "Credit Card"},
                    "reference_number": {"type": "string", "example": "TX123456"},
                    "notes": {"type": "string", "example": "Payment for April services"}
                },
                "required": ["invoice_id", "amount", "payment_date", "payment_method"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Payment created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "invoice_id": {"type": "integer"},
                    "amount": {"type": "number", "format": "float"},
                    "payment_date": {"type": "string", "format": "date-time"},
                    "payment_method": {"type": "string"},
                    "reference_number": {"type": "string"},
                    "notes": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Invoice not found"}
    }
}

PAYMENTS_PAYMENT_ID_GET = {
    "tags": ["Payments"],
    "description": "Get payment by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "payment_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the payment to retrieve"
        }
    ],
    "responses": {
        "200": {
            "description": "Payment details",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "invoice_id": {"type": "integer"},
                    "amount": {"type": "number", "format": "float"},
                    "payment_date": {"type": "string", "format": "date-time"},
                    "payment_method": {"type": "string"},
                    "reference_number": {"type": "string"},
                    "notes": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Payment not found"}
    }
}

PAYMENTS_INVOICE_ID_GET = {
    "tags": ["Payments"],
    "description": "Get all payments for an invoice",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "invoice_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the invoice to retrieve payments for"
        }
    ],
    "responses": {
        "200": {
            "description": "List of payments for the invoice",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "invoice_id": {"type": "integer"},
                        "amount": {"type": "number", "format": "float"},
                        "payment_date": {"type": "string", "format": "date-time"},
                        "payment_method": {"type": "string"},
                        "reference_number": {"type": "string"},
                        "notes": {"type": "string"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"}
                    }
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Invoice not found"}
    }
}

PAYMENTS_PAYMENT_ID_PUT = {
    "tags": ["Payments"],
    "description": "Update payment by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "payment_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the payment to update"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "format": "float", "example": 275.50},
                    "payment_date": {"type": "string", "format": "date-time", "example": "2023-04-16T10:00:00"},
                    "payment_method": {"type": "string", "example": "Bank Transfer"},
                    "reference_number": {"type": "string", "example": "BT987654"},
                    "notes": {"type": "string", "example": "Updated payment information"}
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Payment updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "invoice_id": {"type": "integer"},
                    "amount": {"type": "number", "format": "float"},
                    "payment_date": {"type": "string", "format": "date-time"},
                    "payment_method": {"type": "string"},
                    "reference_number": {"type": "string"},
                    "notes": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Payment not found"}
    }
}

PAYMENTS_PAYMENT_ID_DELETE = {
    "tags": ["Payments"],
    "description": "Delete payment by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "payment_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the payment to delete"
        }
    ],
    "responses": {
        "200": {
            "description": "Payment deleted successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Payment deleted"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Payment not found"}
    }
}

# REVIEWS endpoints documentation
REVIEWS_GET = {
    "tags": ["Reviews"],
    "description": "Get all customer reviews",
    "security": [{"Bearer": []}],
    "responses": {
        "200": {
            "description": "List of reviews",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "customer_id": {"type": "integer"},
                        "location_id": {"type": "integer"},
                        "appointment_id": {"type": "integer"},
                        "rating": {"type": "integer", "minimum": 1, "maximum": 5},
                        "comment": {"type": "string"},
                        "datetime": {"type": "string", "format": "date-time"}
                    }
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

REVIEWS_POST = {
    "tags": ["Reviews"],
    "description": "Create a new customer review",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "integer", "example": 1},
                    "location_id": {"type": "integer", "example": 2},
                    "appointment_id": {"type": "integer", "example": 3},
                    "rating": {"type": "integer", "minimum": 1, "maximum": 5, "example": 5},
                    "comment": {"type": "string", "example": "Excellent service, very professional team!"}
                },
                "required": ["customer_id", "rating"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Review created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "customer_id": {"type": "integer"},
                    "location_id": {"type": "integer"},
                    "appointment_id": {"type": "integer"},
                    "rating": {"type": "integer"},
                    "comment": {"type": "string"},
                    "datetime": {"type": "string", "format": "date-time"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

REVIEWS_REVIEW_ID_PUT = {
    "tags": ["Reviews"],
    "description": "Update review by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "review_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the review to update"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "rating": {"type": "integer", "minimum": 1, "maximum": 5, "example": 4},
                    "comment": {"type": "string", "example": "Updated comment for the service"}
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Review updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "customer_id": {"type": "integer"},
                    "location_id": {"type": "integer"},
                    "appointment_id": {"type": "integer"},
                    "rating": {"type": "integer"},
                    "comment": {"type": "string"},
                    "datetime": {"type": "string", "format": "date-time"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Review not found"}
    }
}

REVIEWS_REVIEW_ID_DELETE = {
    "tags": ["Reviews"],
    "description": "Delete review by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "review_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the review to delete"
        }
    ],
    "responses": {
        "200": {
            "description": "Review deleted successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Review deleted"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Review not found"}
    }
}

# PHOTOS endpoints documentation
PHOTOS_GET = {
    "tags": ["Photos"],
    "description": "Get all photos",
    "security": [{"Bearer": []}],
    "responses": {
        "200": {
            "description": "List of photos",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "appointment_id": {"type": "integer"},
                        "file_path": {"type": "string"},
                        "uploaded_by": {"type": "integer"},
                        "approved_by": {"type": "integer"},
                        "show_to_customer": {"type": "boolean"},
                        "show_on_website": {"type": "boolean"},
                        "datetime": {"type": "string", "format": "date-time"}
                    }
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

PHOTOS_POST = {
    "tags": ["Photos"],
    "description": "Upload a new photo",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "integer", "example": 1},
                    "file_path": {"type": "string", "example": "/uploads/photos/job123.jpg"},
                    "uploaded_by": {"type": "integer", "example": 2},
                    "approved_by": {"type": "integer", "example": 3},
                    "show_to_customer": {"type": "boolean", "example": True},
                    "show_on_website": {"type": "boolean", "example": False}
                },
                "required": ["appointment_id", "file_path", "uploaded_by"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Photo uploaded successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "appointment_id": {"type": "integer"},
                    "file_path": {"type": "string"},
                    "uploaded_by": {"type": "integer"},
                    "approved_by": {"type": "integer"},
                    "show_to_customer": {"type": "boolean"},
                    "show_on_website": {"type": "boolean"},
                    "datetime": {"type": "string", "format": "date-time"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

PHOTOS_PHOTO_ID_PUT = {
    "tags": ["Photos"],
    "description": "Update photo by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "photo_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the photo to update"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "approved_by": {"type": "integer", "example": 1},
                    "show_to_customer": {"type": "boolean", "example": True},
                    "show_on_website": {"type": "boolean", "example": True}
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Photo updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "appointment_id": {"type": "integer"},
                    "file_path": {"type": "string"},
                    "uploaded_by": {"type": "integer"},
                    "approved_by": {"type": "integer"},
                    "show_to_customer": {"type": "boolean"},
                    "show_on_website": {"type": "boolean"},
                    "datetime": {"type": "string", "format": "date-time"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Photo not found"}
    }
}

PHOTOS_PHOTO_ID_DELETE = {
    "tags": ["Photos"],
    "description": "Delete photo by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "photo_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the photo to delete"
        }
    ],
    "responses": {
        "200": {
            "description": "Photo deleted successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Photo deleted"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Photo not found"}
    }
}

# TIMELOGS endpoints additional documentation
TIMELOGS_POST = {
    "tags": ["Time Logs"],
    "description": "Create a new time log",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "integer", "example": 1},
                    "employee_id": {"type": "integer", "example": 2},
                    "time_in": {"type": "string", "format": "date-time", "example": "2023-04-15T08:30:00"}
                },
                "required": ["appointment_id", "employee_id", "time_in"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Time log created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "appointment_id": {"type": "integer"},
                    "employee_id": {"type": "integer"},
                    "time_in": {"type": "string", "format": "date-time"},
                    "time_out": {"type": "string", "format": "date-time"},
                    "total_time": {"type": "number", "format": "float"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

TIMELOGS_LOG_ID_PUT = {
    "tags": ["Time Logs"],
    "description": "Update time log by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "log_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the time log to update"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "time_out": {"type": "string", "format": "date-time", "example": "2023-04-15T17:30:00"}
                },
                "required": ["time_out"]
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Time log updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "appointment_id": {"type": "integer"},
                    "employee_id": {"type": "integer"},
                    "time_in": {"type": "string", "format": "date-time"},
                    "time_out": {"type": "string", "format": "date-time"},
                    "total_time": {"type": "number", "format": "float"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Time log not found"}
    }
}

TIMELOGS_LOG_ID_DELETE = {
    "tags": ["Time Logs"],
    "description": "Delete time log by ID",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "log_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the time log to delete"
        }
    ],
    "responses": {
        "200": {
            "description": "Time log deleted successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Time log deleted"}
                }
            }
        },
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"},
        "404": {"description": "Time log not found"}
    }
}

# INTEGRATIONS endpoints documentation
INTEGRATIONS_REGISTER_WEBHOOK_POST = {
    "tags": ["Integrations"],
    "description": "Register a new webhook endpoint",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "webhook_url": {"type": "string", "example": "https://example.com/webhook-receiver"},
                    "events": {
                        "type": "array",
                        "items": {"type": "string", "enum": ["appointment.created", "appointment.updated", "invoice.paid"]},
                        "example": ["appointment.created", "invoice.paid"]
                    }
                },
                "required": ["webhook_url"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Webhook registered successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Webhook registered"},
                    "webhook_url": {"type": "string"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden - Insufficient permissions"}
    }
}

INTEGRATIONS_WEBHOOK_POST = {
    "tags": ["Integrations"],
    "description": "Receive a webhook event from external systems",
    "parameters": [
        {
            "name": "X-API-Key",
            "in": "header",
            "description": "API key for webhook authentication",
            "required": True,
            "type": "string"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "event": {"type": "string", "example": "customer.updated"},
                    "data": {
                        "type": "object",
                        "example": {
                            "customer_id": 123,
                            "name": "Updated Customer Name",
                            "email": "customer@example.com"
                        }
                    }
                },
                "required": ["event", "data"]
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Webhook event received successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Webhook event received"}
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized - Invalid API key"}
    }
}

INTEGRATIONS_TEST_EVENT_GET = {
    "tags": ["Integrations"],
    "description": "Test integration event generation",
    "parameters": [
        {
            "name": "X-API-Key",
            "in": "header",
            "description": "API key for authentication",
            "required": True,
            "type": "string"
        }
    ],
    "responses": {
        "200": {
            "description": "Sample event data returned",
            "schema": {
                "type": "object",
                "properties": {
                    "event": {"type": "string", "example": "appointment.created"},
                    "data": {
                        "type": "object",
                        "example": {
                            "appointment_id": 123,
                            "customer_location_id": 45,
                            "arrival_datetime": "2025-04-01T10:00:00",
                            "departure_datetime": "2025-04-01T12:00:00"
                        }
                    }
                }
            }
        },
        "401": {"description": "Unauthorized - Invalid API key"}
    }
}

# CUSTOMER PORTAL endpoints documentation
CUSTOMER_PORTAL_REGISTER_POST = {
    "tags": ["Customer Portal"],
    "description": "Register a new customer account",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Jane Smith"},
                    "email": {"type": "string", "example": "jane@example.com"},
                    "password": {"type": "string", "example": "securepassword123"},
                    "phone": {"type": "string", "example": "555-123-4567"}
                },
                "required": ["name", "email", "password"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Customer account created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Customer registered successfully"},
                    "customer_id": {"type": "integer"}
                }
            }
        },
        "400": {"description": "Invalid input or email already registered"},
        "422": {"description": "Validation error - invalid email format"}
    }
}

CUSTOMER_PORTAL_LOGIN_POST = {
    "tags": ["Customer Portal"],
    "description": "Login to customer portal",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "example": "jane@example.com"},
                    "password": {"type": "string", "example": "securepassword123"}
                },
                "required": ["email", "password"]
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Login successful",
            "schema": {
                "type": "object",
                "properties": {
                    "access_token": {"type": "string"},
                    "customer": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                            "email": {"type": "string"}
                        }
                    }
                }
            }
        },
        "400": {"description": "Email and password required"},
        "401": {"description": "Invalid email or password"}
    }
}

CUSTOMER_PORTAL_PROFILE_GET = {
    "tags": ["Customer Portal"],
    "description": "Get customer profile information",
    "security": [{"Bearer": []}],
    "responses": {
        "200": {
            "description": "Customer profile details",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "phone": {"type": "string"},
                    "notes": {"type": "string"},
                    "created_datetime": {"type": "string", "format": "date-time"},
                    "locations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "address": {"type": "string"},
                                "city": {"type": "string"},
                                "state": {"type": "string"},
                                "zip_code": {"type": "string"}
                            }
                        }
                    }
                }
            }
        },
        "401": {"description": "Unauthorized - Invalid or expired token"}
    }
}

CUSTOMER_PORTAL_PROFILE_PUT = {
    "tags": ["Customer Portal"],
    "description": "Update customer profile",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Jane D. Smith"},
                    "phone": {"type": "string", "example": "555-987-6543"},
                    "password": {"type": "string", "example": "newSecurePassword123"}
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Profile updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Profile updated successfully"},
                    "customer": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "phone": {"type": "string"}
                        }
                    }
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized - Invalid or expired token"}
    }
}

CUSTOMER_PORTAL_APPOINTMENTS_GET = {
    "tags": ["Customer Portal"],
    "description": "Get customer appointments",
    "security": [{"Bearer": []}],
    "responses": {
        "200": {
            "description": "List of customer appointments",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "location_id": {"type": "integer"},
                        "address": {"type": "string"},
                        "description": {"type": "string"},
                        "start_time": {"type": "string", "format": "date-time"},
                        "end_time": {"type": "string", "format": "date-time"},
                        "status": {"type": "string", "enum": ["scheduled", "completed", "cancelled"]},
                        "notes": {"type": "string"}
                    }
                }
            }
        },
        "401": {"description": "Unauthorized - Invalid or expired token"}
    }
}

CUSTOMER_PORTAL_INVOICES_GET = {
    "tags": ["Customer Portal"],
    "description": "Get customer invoices",
    "security": [{"Bearer": []}],
    "responses": {
        "200": {
            "description": "List of customer invoices",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "appointment_id": {"type": "integer"},
                        "appointment_date": {"type": "string", "format": "date-time"},
                        "location_address": {"type": "string"},
                        "total_amount": {"type": "number", "format": "float"},
                        "amount_paid": {"type": "number", "format": "float"},
                        "balance": {"type": "number", "format": "float"},
                        "status": {"type": "string", "enum": ["draft", "sent", "paid", "overdue"]},
                        "due_date": {"type": "string", "format": "date"},
                        "created_datetime": {"type": "string", "format": "date-time"},
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "description": {"type": "string"},
                                    "quantity": {"type": "integer"},
                                    "unit_price": {"type": "number", "format": "float"},
                                    "amount": {"type": "number", "format": "float"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "401": {"description": "Unauthorized - Invalid or expired token"}
    }
}

CUSTOMER_PORTAL_PHOTOS_GET = {
    "tags": ["Customer Portal"],
    "description": "Get photos visible to customer",
    "security": [{"Bearer": []}],
    "responses": {
        "200": {
            "description": "List of photos visible to customer",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "appointment_id": {"type": "integer"},
                        "file_path": {"type": "string"},
                        "description": {"type": "string"},
                        "datetime": {"type": "string", "format": "date-time"},
                        "location": {"type": "string"}
                    }
                }
            }
        },
        "401": {"description": "Unauthorized - Invalid or expired token"}
    }
}

CUSTOMER_PORTAL_REVIEWS_POST = {
    "tags": ["Customer Portal"],
    "description": "Submit a review for a completed service",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "integer", "example": 1},
                    "rating": {"type": "integer", "minimum": 1, "maximum": 5, "example": 5},
                    "comment": {"type": "string", "example": "The service was excellent, very satisfied with the work!"}
                },
                "required": ["appointment_id", "rating"]
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Review submitted successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "msg": {"type": "string", "example": "Review submitted successfully"},
                    "review_id": {"type": "integer"}
                }
            }
        },
        "400": {"description": "Invalid input or already reviewed"},
        "401": {"description": "Unauthorized - Invalid or expired token"},
        "404": {"description": "Appointment not found or doesn't belong to customer"}
    }
}

CUSTOMER_PORTAL_INVOICE_ID_GET = {
    "tags": ["Customer Portal"],
    "description": "Get payment details for an invoice",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "invoice_id",
            "in": "path",
            "required": True,
            "type": "integer",
            "description": "ID of the invoice to retrieve payment details for"
        }
    ],
    "responses": {
        "200": {
            "description": "Payment details for the invoice",
            "schema": {
                "type": "object",
                "properties": {
                    "invoice_id": {"type": "integer"},
                    "total_amount": {"type": "number", "format": "float"},
                    "balance": {"type": "number", "format": "float"},
                    "payment_url": {"type": "string"},
                    "invoice_details": {
                        "type": "object",
                        "properties": {
                            "due_date": {"type": "string", "format": "date"},
                            "status": {"type": "string"},
                            "items": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "description": {"type": "string"},
                                        "quantity": {"type": "integer"},
                                        "unit_price": {"type": "number", "format": "float"},
                                        "amount": {"type": "number", "format": "float"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "401": {"description": "Unauthorized - Invalid or expired token"},
        "403": {"description": "Forbidden - Invoice doesn't belong to customer"},
        "404": {"description": "Invoice not found"}
    } }
