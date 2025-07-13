import os
import sys
import importlib
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import DeviceInfo

def init(device_info: DeviceInfo, mqtt_settings: Settings.MQTT):
    # Define the absolute path to your plugins directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    plugins_physical_path = os.path.join(project_root, 'plugins') 

    loaded_plugins = []
    print(f'Scanning for plugins in: {plugins_physical_path}')

    for filename in os.listdir(plugins_physical_path):
        if filename.endswith('.py') and filename != '__init__.py':
            # This will be the name you refer to the module as once loaded
            module_alias_name = filename[:-3] 
            file_full_path = os.path.join(plugins_physical_path, filename)

            print(f"Attempting to load module from file: {file_full_path} as '{module_alias_name}'")

            try:
                spec = importlib.util.spec_from_file_location(module_alias_name, file_full_path)
                if spec is None:
                    print(f"Warning: Could not get module spec for {file_full_path}")
                    continue

                plugin_module = importlib.util.module_from_spec(spec)
                # Crucial: Add the module to sys.modules under its alias name
                sys.modules[module_alias_name] = plugin_module 

                spec.loader.exec_module(plugin_module) # Execute the code within the .py file

                plugin_class = getattr(plugin_module, 'Init', None)
                if plugin_class:
                    print(f"Initializing plugin -> [{module_alias_name}]")
                    loaded_plugins.append(plugin_class(device_info, mqtt_settings))
                else:
                    print(f"Warning: Plugin cannot be loaded {module_alias_name} ({file_full_path})")

            except Exception as e:
                print(f"Error loading or executing plugin {module_alias_name} from {file_full_path}: {e}")

    def update():
        for plugin in loaded_plugins:
            try:
                plugin.update()
            except:
                print(f"The plugin {plugin} has no update function.")

    return update