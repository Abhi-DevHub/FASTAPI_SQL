import uuid

def generate_uuid() -> str:
    
    """Generate a unique identifier.
    Returns:
        str: A string representation of a UUID.
    """
    return str(uuid.uuid4())
