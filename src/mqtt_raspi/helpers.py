def parse_color(color):
    """Parse a color from hex or RGB format."""
    if type(color) is str and color.startswith('#'):
        # Hex color format
        color = color.lstrip('#')
        if len(color) == 6:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
        else:
            raise ValueError("Hex color must be 6 characters long.")
    elif type(color) is dict:
        r, g, b = int(color['r'] | 0), int(color['g'] | 0), int(color['b'] | 0)
    elif type(color) is list:
        r, g, b = map(int, color.split(','))
    else:
        raise ValueError("Color must be in the format 'r,g,b', '#hex' or [r,g,b].")

    return r, g, b

def apply_brightness(color, brightness):
    # Ensure brightness is clamped between 0 and 255
    brightness = max(0, min(255, brightness))

    # Calculate the scaling factor
    scale = brightness / 255.0

    # Apply the brightness scaling to each color component
    r, g, b = map(int, [color[0] * scale, color[1] * scale, color[2] * scale])

    return r, g, b

def read_cpu_temperature():
    """Read the CPU temperature from the Raspberry Pi."""
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp_milli_celsius = int(f.read().strip())
    return temp_milli_celsius / 1000.0  # Convert to Celsius

def temperature_to_color(temp):
    """Map temperature to LED color."""
    if temp < 40:
        return (0, 0, 255)  # Blue for cool temperatures
    elif 40 <= temp < 60:
        return (0, 255, 0)  # Green for moderate temperatures
    elif 60 <= temp < 80:
        return (255, 255, 0)  # Yellow for warm temperatures
    else:
        return (255, 0, 0)  # Red for hot temperatures
