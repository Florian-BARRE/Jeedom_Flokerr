# Jeedom_ws
The Flokerr-Jeedom Server integrates Flokerr with Jeedom for smart home automation. It synchronizes data in real-time, manages devices, and updates Jeedom via WS and HTTP, streamlining smart home control.

# Flokerr-Jeedom Integration Server Overview
The Flokerr-Jeedom Integration Server is a specialized Python server application crafted to bridge the gap between Flokerr services and Jeedom, a prominent home automation system. This server focuses on real-time data synchronization, enabling dynamic subscription to Flokerr topics, and efficiently managing device information. It facilitates seamless integration by channeling data through WebSocket (WS) and HTTP protocols, ensuring that Jeedom users can effortlessly update and control their smart home devices based on the latest data from Flokerr.

## Key Features
* Real-time Topic Subscription:
Dynamically subscribes to a predefined list of topics within the Flokerr ecosystem.
Automatically updates and records the values of these topics in a structured text file, ensuring that the information remains current and accessible.

* Seamless Jeedom Integration:
Directly feeds the synchronized data into Jeedom, allowing for the real-time update of objects and scenarios within the Jeedom interface.
Utilizes a straightforward JSON state file (states.json) to map out the current status of subscribed topics, making it easy for Jeedom to parse and act upon this data.

* Device Management:
Manages a comprehensive list of devices through a simple text file (devices.txt), where users can specify device names to be monitored.
Provides essential connection information for each device, including ping status, name, UUID, version, and more, facilitating easier management and integration within the Flokerr ecosystem.

* Configuration and Security:
Leverages a JSON configuration file for flexible server setup, allowing users to tailor the server's operation to their specific needs.
Ensures the security of sensitive information through a dedicated secrets.json file, separating critical credentials from the main configuration settings.

## How It Works
* Initialization:
The server initializes by parsing the configuration settings, setting up its connection to Flokerr, and preparing the environment for topic subscription and device management.

* Topic Management:
Subscribes to topics as specified in topics.txt, dynamically updating the states.json file with the latest data from these subscriptions.
This process allows Jeedom to directly access and utilize up-to-date information for device control and automation tasks.

* Device Information Handling:
Reads the list of devices from devices.txt, fetching and storing relevant connection details for each.
These details are made available to both the server and Jeedom, ensuring that devices can be efficiently managed and monitored.

* Real-time Data Exchange:
Utilizes WebSocket connections for real-time data exchange, ensuring that the server and Jeedom stay synchronized with the current state of devices and topics within the Flokerr network.

## Getting Started
* Requirements:
Ensure Python 3.x is installed, along with all dependencies listed in requirements.txt.
* Configuration:
Adjust configuration.json to match your Flokerr server and network settings.
Modify secrets.json for secure operation, ensuring all sensitive information is correctly handled.
Or, use dokcer-compose file to set all environnement variables.
* Running the Server:
Execute main.py to start the server. It will begin listening for connections and start the process of topic subscription and device management based on the configurations provided.

## Conclusion
The Flokerr-Jeedom Integration Server is engineered to provide a robust and flexible solution for integrating Flokerr's real-time data and device management capabilities with Jeedom's home automation platform. Its design emphasizes security, ease of use, and dynamic data handling, making it an invaluable tool for homeowners and system integrators looking to enhance their smart home setups.