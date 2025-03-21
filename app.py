# app.py
from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from flask_migrate import Migrate
from flask_cors import CORS
from blueprints.auth import auth_bp
from blueprints.employees import employees_bp
from blueprints.customers import customers_bp
from blueprints.locations import locations_bp
from blueprints.appointments import appointments_bp
from blueprints.invoices import invoices_bp
from blueprints.quotes import quotes_bp
from blueprints.equipment import equipment_bp
from blueprints.reviews import reviews_bp
from blueprints.photos import photos_bp
from blueprints.timelogs import timelogs_bp
from blueprints.customer_portal import customer_portal_bp
from blueprints.integrations import integrations_bp
from blueprints.payments import payments_bp
from flask import jsonify
import os
from dotenv import load_dotenv
import sys 
from flasgger import Swagger

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure CORS - with security improvements
    CORS(app, 
        resources={r"/*": {"origins": "*"}},
        send_wildcard=True,
        allow_headers="*",
        expose_headers="*",
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        max_age=86400,
        allow_private_network=False,
        supports_credentials=False
    )
    
    # Disable debug mode for Werkzeug
    app.debug = False
    
    DB_USER = os.getenv('POSTGRES_USER')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    DB_HOST = os.getenv('POSTGRES_HOST')
    DB_PORT = os.getenv('POSTGRES_PORT')
    DB_NAME = os.getenv('POSTGRES_DB')

    # Configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', "vpkhHIuKR7IvvZIZ23EqJYYyW5aR0wKgPg8zTdeJkqnVhbk7XCp/fRut")
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/api/auth/refresh'
    app.config['JWT_COOKIE_SECURE'] = True

    print(app.config['JWT_SECRET_KEY'])
    
    # Configure Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/api/apispec.json",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/api/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs"
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Field Service Management API",
            "description": "API Documentation for Field Service Management System",
            "version": "1.0.0",
            "contact": {
                "email": "admin@example.com"
            }
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ]
    }
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    
    # Initialize Swagger after all blueprints are registered
    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(employees_bp, url_prefix='/api/employees')
    app.register_blueprint(customers_bp, url_prefix='/api/customers')
    app.register_blueprint(locations_bp, url_prefix='/api/locations')
    app.register_blueprint(appointments_bp, url_prefix='/api/appointments')
    app.register_blueprint(invoices_bp, url_prefix='/api/invoices')
    app.register_blueprint(quotes_bp, url_prefix='/api/quotes')
    app.register_blueprint(equipment_bp, url_prefix='/api/equipment')
    app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
    app.register_blueprint(photos_bp, url_prefix='/api/photos')
    app.register_blueprint(timelogs_bp, url_prefix='/api/timelogs')
    app.register_blueprint(customer_portal_bp, url_prefix='/api/customer_portal')
    app.register_blueprint(integrations_bp, url_prefix='/api/integrations')
    app.register_blueprint(payments_bp, url_prefix='/api/payments')
    #app.register_blueprint(docs_bp, url_prefix='/api/docs')
    
    # Initialize Swagger after all blueprints have been registered
    swg = Swagger(app, config=swagger_config, template=swagger_template)
    
    # CORS preflight options for all routes
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With,X-Auth-Token')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        # Set Referrer-Policy to a permissive value instead of strict-origin-when-cross-origin
        response.headers.add('Referrer-Policy', 'unsafe-url')
        # Add Vary: Cookie header to prevent session cookie disclosure
        response.headers.add('Vary', 'Cookie')
        return response
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """
        Health Check Endpoint
        ---
        responses:
          200:
            description: Server is healthy
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: healthy
        """
        return jsonify({"status": "healthy"}), 200
    
    # Create database tables (for development; use migrations in production)
    with app.app_context():
        db.create_all()
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
