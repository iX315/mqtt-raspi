import os
import importlib
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import DeviceInfo

def init(device_info: DeviceInfo, mqtt_settings: Settings.MQTT):
    # Directory containing sensor modules
    sensor_directory = 'items'
    
    # List to hold sensor instances
    sensors = []

    # Iterate through the files in the sensor directory
    for filename in os.listdir(sensor_directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Remove the .py extension
            module = importlib.import_module(f'{sensor_directory}.{module_name}')
            sensor_class = getattr(module, 'Init', None)
            if sensor_class:
                sensors.append(sensor_class(device_info, mqtt_settings))

    def update():
        for sensor in sensors:
            sensor.update()

    return update