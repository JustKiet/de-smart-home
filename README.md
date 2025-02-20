# 🏙️🤖 DeSmartHome: A Decentralized Multi-Agent Smart Home System

## 🤔 What is DeSmartHome?

**DeSmartHome** is an innovative approach to smart home automation, leveraging a **decentralized multi-agent system** where each room is operated by an independent yet interconnected agent. 

By distributing intelligence across local AI-powered agents, DeSmartHome enhances reliability, privacy, and responsiveness without relying on a central controller.

**DeSmartHome** also applies blockchain technology to ensure data integrity, secure communication, and decentralized control, preventing unauthorized access and enhancing trust among agents.

**DeSmartHome** aims to ensure seamless automation, real-time decision-making, and adaptability to dynamic household environments, creating an intelligent and self-sufficient smart home ecosystem.

## Why DeSmartHome?

**DeSmartHome** aims to resolve the current problems of Vietnamese Smarthome Market:

- **Basic Connectivity**: While the global smart home market is targeting Smart Connectivity, implementing state-of-the-art AI solutions to improve user experiences, Vietnamese Smarthomes Companies are still far behind, only offering basic IoT control and connectivity while lacking intelligent automation, contextual awareness, and adaptive learning. Most systems rely on predefined rules rather than AI-driven decision-making, leading to rigid and less personalized user experiences.
- **Security Challenges**: Many Vietnamese smart home solutions rely on cloud-based infrastructure, making them vulnerable to cyber threats, data breaches, and service outages. Additionally, weak encryption standards and a lack of regular security updates expose users to potential hacking risks. A more secure, decentralized approach is needed to protect user data and ensure system reliability. 
- **Narrow Smart Ecosystem**: Vietnamese smart home companies focus primarily on IoT devices like lighting, security, and appliances, with little integration into broader aspects of daily life such as user productivity, health, or financial management.

**DeSmartHome** addresses key challenges in the Vietnamese smart home market by introducing a decentralized multi-agent system that enhances security, expands compatibility, and enables AI-driven automation. It also integrates blockchain technology for decentralized data storage and secure transactions, ensuring privacy, transparency, and trust. This approach creates a more intelligent, adaptable, and secure smart home environment, moving Vietnam closer to global standards while offering a fully integrated and user-centric smart living experience.                                                                                                                                                                                                                                                  

## Project Structure

```
de-smart-home/
├── .gitignore
├── README.md
├── backend
│   ├── ai_modules # Contains AI/ML/DL modules
│   │   ├── __init__.py
│   │   ├── agents # Agents Core
│   │   │   ├── __init__.py
│   │   │   ├── ...
│   │   ├── speech
│   │   │   └── __init__.py
│   │   └── vision
│   │       └── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── routes # Contains route handlers that define API endpoints. 
│   │       ├── __init__.py
│   │       ├── ...
│   ├── clients # Contains client scripts.
│   │   ├── __init__.py
│   │   ├── device_control_client.py
│   │   ├── ptt_client.py
│   │   └── realtime_client.py
│   ├── config.py
│   ├── database # Contains database access objects (DAO)
│   │   └── __init__.py
│   ├── devices # Contains device classes definitions and interfaces
│   │   ├── __init__.py
│   │   ├── ac_device.py
│   │   ├── interfaces
│   │   │   ├── __init__.py
│   │   │   ├── common
│   │   │   │   ├── __init__.py
│   │   │   │   ├── control_power.py
│   │   │   │   └── device_status.py
│   │   │   ├── control_ac.py
│   │   │   ├── control_camera.py
│   │   │   ├── control_door.py
│   │   │   ├── control_light.py
│   │   │   ├── control_microphone.py
│   │   │   ├── control_sensor.py
│   │   │   ├── control_speaker.py
│   │   │   └── sensors
│   │   │       └── __init__.py
│   │   ├── light_device.py
│   │   ├── microphone_device.py
│   │   └── speaker_device.py
│   ├── gateways # Contains the core logic for controlling devices and advanced processing
│   │   ├── __init__.py
│   │   ├── ac_gateway.py
│   │   ├── audio_gateway.py
│   │   ├── camera_gateway.py
│   │   ├── door_gateway.py
│   │   ├── interfaces
│   │   │   ├── __init__.py
│   │   │   ├── common
│   │   │   │   ├── __init__.py
│   │   │   │   └── control_gateway.py
│   │   │   ├── manage_ac.py
│   │   │   └── manage_speaker.py
│   │   └── light_gateway.py
│   ├── handlers
│   │   ├── __init__.py
│   │   └── event_handler.py
│   ├── main.py
│   └── utils
│       ├── __init__.py
│       └── tool_wrapper.py
├── frontend
│   └── README.md
├── playground.ipynb
├── requirements.txt
└── setup.py
```

## Setting up the project

First, clone the project and install the dependencies:
```
pip install -r requirements.txt
```
==WIP==
