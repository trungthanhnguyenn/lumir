# Define form
def form_check(form_data):
    # Check if form_data is a dictionary
    if not isinstance(form_data, dict):
        return False
    
    # Check if form_data has the required fields
    required_fields = ['name', 'email', 'phone', 'message']
    for field in required_fields:
        if field not in form_data:
            return False
    return True
