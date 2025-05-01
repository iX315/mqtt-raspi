import random
import time
from helpers import parse_color, read_cpu_temperature, temperature_to_color

def rainbow_cycle(neo, delay):
    colors = [
        (255, 0, 0),  # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (75, 0, 130),  # Indigo
        (148, 0, 211)  # Violet
    ]
    for color in colors:
        neo.fill_strip(*color)
        neo.update_strip()
        time.sleep(delay)

def solid(neo, color):
    # Parse the color input
    r, g, b = parse_color(color)

    # Fill the strip with the specified color
    neo.fill_strip(r, g, b)
    neo.update_strip()  # Commit changes to the LEDs

def loading_bar(neo, delay, color):
    # Parse the color input
    r, g, b = parse_color(color)

    for i in range(neo.num_leds):
        neo.set_led_color(i, r, g, b)
        neo.update_strip()
        time.sleep(delay)
    neo.clear_strip()
    neo.update_strip()

def firework(neo, delay):
    center = random.randint(0, neo.num_leds - 1)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    # Simulate firework explosion expanding outward
    for radius in range(neo.num_leds):
        neo.fill_strip(0, 0, 0)
        if center - radius >= 0:
            neo.set_led_color(center - radius, *color)
        if center + radius < neo.num_leds:
            neo.set_led_color(center + radius, *color)
        neo.update_strip()
        time.sleep(delay)

def temperature(neo):
    temp = read_cpu_temperature()
    color = temperature_to_color(temp)
    neo.fill_strip(*color)  # Fill the LED strip with the determined color
    neo.update_strip()  # Commit changes to the LEDs
    print(f"Current CPU Temperature: {temp:.2f} °C, LED Color: {color}")
    time.sleep(1)  # Update every second