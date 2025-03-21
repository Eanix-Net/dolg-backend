"""
Script to add Swagger documentation to all blueprint files.
Run this script to update all blueprint files with Swagger documentation.
"""
import os
import re

IMPORT_STATEMENT = 'from flasgger import swag_from\nfrom utils.swagger_docs import (\n'
IMPORT_CLOSING = ')\n'

def get_route_name(line):
    """Extract the route name from a Flask route decorator."""
    match = re.search(r"@\w+_bp\.route\('([\w/<>:]+)'", line)
    if match:
        route = match.group(1)
        # Handle parameters in routes
        if '<' in route:
            param_match = re.search(r'<[\w:]+:([\w_]+)>', route)
            if param_match:
                param_name = param_match.group(1)
                return f"_{param_name}"
        
        # Handle root route
        if route == '/':
            return ""
        
        # Handle other routes
        route = route.replace('/', '_').strip('_')
        return f"_{route}"
    return ""

def get_entity_from_filename(filename):
    """Extract the entity name from the blueprint filename."""
    # Remove .py extension
    entity = filename.replace('.py', '')
    # Convert to uppercase for first letter
    entity = entity.capitalize()
    # Handle special cases
    if entity.endswith('s'):
        # Remove trailing 's' for singular form
        entity = entity[:-1]
    
    # Special handling for specific entities
    name_mapping = {
        'Auth': 'Authentication',
        'Locations': 'Location',
        'Timelogs': 'TimeLog',
        'Customer_portal': 'CustomerPortal',
        'Integrations': 'Integration',
        'Payments': 'Payment'
    }
    
    return name_mapping.get(entity, entity)

def snake_to_camel(snake_str):
    """Convert snake_case to CamelCase."""
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)

def add_swagger_to_file(file_path):
    """Add Swagger documentation to a blueprint file."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Check if Swagger is already imported
    if any('from flasgger import swag_from' in line for line in lines):
        print(f"Swagger already imported in {file_path}")
        return
    
    # Find blueprint declaration and extract name
    bp_name = None
    for i, line in enumerate(lines):
        if '_bp = Blueprint(' in line:
            match = re.search(r'(\w+)_bp = Blueprint', line)
            if match:
                bp_name = match.group(1)
                break
    
    if not bp_name:
        print(f"Could not find blueprint declaration in {file_path}")
        return
    
    # Get filename without path and extension
    filename = os.path.basename(file_path)
    entity_name = get_entity_from_filename(filename)
    
    # Find all route declarations
    route_declarations = []
    swagger_imports = []
    
    for i, line in enumerate(lines):
        if f'@{bp_name}_bp.route' in line:
            method_match = re.search(r"methods=\['([A-Z]+)'", line)
            method = method_match.group(1) if method_match else 'GET'
            
            # Get the next line which should be function decorator or definition
            next_line = lines[i+1] if i+1 < len(lines) else ""
            
            # If the next line is a decorator, we need to look further
            j = i + 1
            while j < len(lines) and '@' in lines[j]:
                j += 1
            
            # Now we should have the function definition
            if j < len(lines):
                func_match = re.search(r'def (\w+)\(', lines[j])
                if func_match:
                    func_name = func_match.group(1)
                    route_suffix = get_route_name(line)
                    
                    # Create Swagger variable name
                    swagger_var = f"{bp_name.upper()}{route_suffix.upper()}_{method}"
                    swagger_imports.append(swagger_var)
                    
                    # Add swag_from decorator after the route and auth decorators
                    route_declarations.append((j, func_name, swagger_var))
    
    # Prepare import statement
    imports_wrapped = [f"    {imp}" for imp in swagger_imports]
    import_statement = IMPORT_STATEMENT + ',\n'.join(imports_wrapped) + IMPORT_CLOSING
    
    # Find where to insert import
    import_pos = 0
    for i, line in enumerate(lines):
        if line.startswith('from') or line.startswith('import'):
            import_pos = i + 1
        elif line.strip() and not line.startswith('#'):
            break
    
    # Insert import statement
    lines.insert(import_pos, import_statement)
    
    # Add swag_from decorators
    # We need to process from bottom to top to keep line numbers correct
    for func_pos, func_name, swagger_var in sorted(route_declarations, reverse=True):
        lines.insert(func_pos, f"@swag_from({swagger_var})\n")
    
    # Write the updated file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print(f"Added Swagger documentation to {file_path}")

def generate_swagger_docs_file():
    """Generate a swagger_docs.py file with documentation templates for all endpoints."""
    # Implementation to be filled in
    pass

def main():
    """Main entry point for the script."""
    # Process all blueprint files
    blueprints_dir = os.path.join('backend', 'blueprints')
    if not os.path.exists(blueprints_dir):
        blueprints_dir = 'blueprints'  # Try relative path
    
    for filename in os.listdir(blueprints_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            file_path = os.path.join(blueprints_dir, filename)
            add_swagger_to_file(file_path)
    
    # Generate swagger_docs.py file
    generate_swagger_docs_file()

if __name__ == '__main__':
    main() 