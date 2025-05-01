
import asyncio
import os
from dotenv import load_dotenv
from items import init as init_items
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import DeviceInfo
from paho.mqtt.client import Client, CallbackAPIVersion

load_dotenv()

MQTT_HOST = os.getenv('MQTT_HOST', None)
MQTT_PORT = os.getenv('MQTT_PORT', 1883)
MQTT_USER = os.getenv('MQTT_USER', None)
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', None)
MQTT_CLIENT_ID = os.getenv('MQTT_CLIENT_ID', None)
MQTT_DISCOVEY_PREFIX = os.getenv('MQTT_DISCOVEY_PREFIX', 'homeassistant')
DEVICE_NAME = os.getenv('DEVICE_NAME', 'Raspberry')
DEVICE_IDENTIFIER = os.getenv('DEVICE_IDENTIFIER', 'Rpi')
DEVICE_MANUFACTURER = os.getenv('DEVICE_MANUFACTURER', "Raspberry Pi")
DEVICE_MODEL = os.getenv('DEVICE_MODEL', "Raspberry Pi 5")

async def main():
    mqtt_settings = Settings.MQTT(
        host=MQTT_HOST,
        port=MQTT_PORT,
        username=MQTT_USER,
        password=MQTT_PASSWORD,
        client_id=MQTT_CLIENT_ID,
        discovery=True,
        discovery_prefix=MQTT_DISCOVEY_PREFIX
    )

    device_info = DeviceInfo(
        name=DEVICE_NAME,
        identifiers=DEVICE_IDENTIFIER,
        manufacturer=DEVICE_MANUFACTURER,
        model=DEVICE_MODEL,
    )

    # Initialize the MQTT client
    mqtt_client = Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id='rpi5neo')
    mqtt_client.username_pw_set(mqtt_settings.username, mqtt_settings.password)

    # Connect to the MQTT broker
    mqtt_client.connect(mqtt_settings.host, mqtt_settings.port)

    update_items = init_items(device_info, mqtt_settings)

    # Publish the discovery message
    mqtt_client.loop_start()  # Start the MQTT loop

    while True:
        update_items()

        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
