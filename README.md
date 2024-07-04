# ASI-InSPACe-CANSAT-2022-Team-Astropeep

<img src="/Ground Station/Cansat-GUI-Final/Logos/Cansat_logo.jpg" width="400" alt="CANSAT Design">

This repository contains the project documentation and code for our team's (Team Astropeep) CanSat developed for the CanSat-India 2022 competition organized by Astronautical Society of India [(ASI)](https://www.asindia.org/), Indian National Space Promotion and Authorization Centre [(IN–SPACe)](https://www.inspace.gov.in) and Indian Space Research Organization [(ISRO)](https://www.isro.gov.in/). A CanSat is a miniature version of a real satellite, designed to fit within a small volume. Despite its miniature size, it mimics many of the functionalities and challenges of actual satellites. It is designed to perform specific scientific and engineering tasks, typically in a controlled flight environment such as a rocket launch or high-altitude balloon release. CanSats are used primarily in educational settings, particularly in STEM (Science, Technology, Engineering, and Mathematics) education programs, to teach students about satellite technology, space missions, data collection, and analysis.

## Introduction

This project details the development of our CanSat for the annual CanSat competition. Our goal was to design and build a functioning satellite within the constraints provided by the competition guidelines.

## Features

- Compact size (fits within a standard soda can)
- Integration of various sensors (e.g., temperature, pressure)
- Communication systems for data transmission
- Parachute deployment system
- Mechanical Gyro Control
- Data logging capabilities

## Components

The CanSat consists of the following main components:

- **Microcontroller**: Controls the operation and data collection.
- **Sensors**: Measure various environmental parameters (e.g., temperature, pressure).
- **Communication System**: Transmits data to the ground station.
- **Power System**: Provides necessary power to all components.
- **Mechanical Structure**: Holds all components securely and includes the parachute deployment system.
- **Mechanical Gyro Control**: Controls the orientation of CanSat during Descent.

## Technical Details

- **Microcontroller**: We used ESP-32 for processing and data handling.
- **Sensors**: Included BMP-280, DHT11 and MPU6050 to gather environmental data during flight.
- **Communication**: XBEE-Pro-S2C was employed for transmitting data to the ground station with 2.4 GHz of operating frequency.
- **Power**: Two Li-Ion battery (9V and 1200 mAh) was used to power the CanSat throughout its mission.

## Flight Software

The `Flight Software Files/` directory contains the source code used in the CanSat. It includes:

- **Main Control Code**: Handles sensor readings, data transmission, and overall control.
- **Sensor Calibration Scripts**: Scripts used for calibrating sensors pre-flight.
- **Data Logging Code**: Code snippets responsible for logging data during the flight.

## Ground Station

The `Ground Station/` directory contains the source code used in developing the ground station and GUI of CanSat. It includes:

- **GUI Scripts**: Handles sensor readings, data transmission, and overall control.
- **Communication Scripts**: Scripts used for calibrating sensors pre-flight.
- **Data Logging Code**: Code snippets responsible for logging data during the flight.

## 

## Usage

To replicate our CanSat project or use parts of our code, follow these steps:

1. Clone this repository:
    ```bash
       git clone https://github.com/Neural-Ninja/ASI-InSPACe-CANSAT-2022-Team-Astropeep.git
       cd ASI-InSPACe-CANSAT-2022-Team-Astropeep
2. Navigate to the `CANSAT Design Files/` directory for acessing the design CAD files.
     ```bash
        cd CANSAT Design Files
3. Navigate to the `CANSAT Presentation Files/` and `CANSAT Report Files/` for better conceptual understanding of our CANSAT model and its working. 
     ```bash
        cd CANSAT Presentation Files
        cd CANSAT Report Files
4. Navigate to the `Flight Software Files/` for accessing the Flight Software source codes.
    ```bash
        cd Flight Software Files
5. Navigate to the `Ground Station/` for accessing the Ground Station source codes
    ```bash
        cd Ground Station
## Contributing

Contributions to improve the code, documentation, or any other aspect of the project are welcome. Feel free to fork this repository, make your changes, and submit a pull request.

## License

This project is licensed under the [MIT License](License) - see the LICENSE file for details.
