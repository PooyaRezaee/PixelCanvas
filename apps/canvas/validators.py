from django.core.exceptions import ValidationError

def validate_x_coordinates(x: int):
    if not (0 <= x <= 99):
        raise ValidationError("X coordinate must be between 0 and 99")
    
def validate_y_coordinates(y: int):
    if not (0 <= y <= 99):
        raise ValidationError("Y coordinate must be between 0 and 99")
