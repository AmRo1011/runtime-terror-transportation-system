# Smart City Transportation System 🚦

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.24.0-orange.svg)](https://streamlit.io)
[![NetworkX](https://img.shields.io/badge/NetworkX-2.8.4-blue.svg)](https://networkx.org)

A comprehensive transportation optimization system for smart cities, implementing various algorithms to solve transportation-related problems. This project is part of the CSE112 - Design and Analysis of Algorithms course.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Data Sources](#data-sources)
- [Installation](#installation)
- [Usage](#usage)
- [Algorithms Implemented](#algorithms-implemented)
- [Team](#team)

## Overview

The Smart City Transportation System is a sophisticated platform that leverages various algorithms to optimize urban transportation networks. It provides solutions for multiple transportation challenges, from route planning to traffic management and public transport scheduling.

## Features

### 1. Road Network Optimization
- **Minimum Spanning Tree (MST)** implementation for optimal road network design
- Integration with existing road infrastructure
- Cost-effective road network expansion planning

### 2. Route Planning and Navigation
- **Dijkstra's Algorithm** for shortest path finding
- **A* Algorithm** for optimized path finding
- Emergency vehicle routing with priority paths

### 3. Traffic Management
- Smart traffic signal timing using greedy algorithms
- Dynamic congestion reduction at intersections
- Traffic flow pattern analysis

### 4. Public Transport Optimization
- Bus scheduling optimization using dynamic programming
- Metro line scheduling and resource allocation
- Capacity planning and optimization

### 5. Maintenance Planning
- Budget-aware maintenance scheduling
- Road condition monitoring and prediction
- Cost optimization for maintenance activities

## Project Structure

```
runtime-terror-transportation-system/
├── docs/                    # Documentation and reports
│   ├── presentation/        # Presentation materials
│   │   └── README.md
│   └── report/             # Project reports
│       └── README.md
├── dp_optimization/         # Dynamic programming implementations
│   ├── dp_maintenance.py   # Maintenance scheduling
│   ├── dp_scheduler.py     # Transport scheduling
│   └── README.md
├── greedy_signals/          # Traffic signal optimization
│   └── README.md
├── mst/                     # Minimum Spanning Tree implementation
│   └── README.md
├── shared/                  # Shared resources
│   └── data/               # Data files
│       ├── Current_Bus_Routes.csv
│       ├── Current_Metro_Lines.csv
│       ├── Existing_Roads.csv
│       ├── Facilities.csv
│       ├── Neighborhoods.csv
│       ├── Potential_New_Roads.csv
│       ├── Traffic_Flow_Patterns.csv
│       └── Transportation_Demand.csv
├── shortest_path/           # Path finding algorithms
│   └── README.md
├── testing/                 # Test cases
│   └── test_graph.py
├── __init__.py             # Package initialization
├── app.py                  # Main Streamlit application
├── main.py                 # Entry point
├── setup.py                # Package setup
└── structure.md            # Project structure documentation
```

## Data Sources

The system uses the following data files for optimization:
- `Current_Bus_Routes.csv`: Current bus route information
- `Current_Metro_Lines.csv`: Metro line configurations
- `Existing_Roads.csv`: Current road network data
- `Facilities.csv`: Location and type of facilities
- `Neighborhoods.csv`: Neighborhood boundaries and data
- `Potential_New_Roads.csv`: Proposed new road segments
- `Traffic_Flow_Patterns.csv`: Traffic flow analysis data
- `Transportation_Demand.csv`: Transportation demand patterns


---

## 🛠️ Technologies

- Python 3.10+
- Streamlit (for UI)
- NetworkX (graph processing)
- Matplotlib (visualizations)
- Git & GitHub (version control)

## 🔧 Installation

```bash
git clone https://github.com/AmRo1011/runtime-terror-transportation-system.git
cd runtime-terror-transportation-system
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/amro1011/runtime-terror-transportation-system.git
cd runtime-terror-transportation-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application
```bash
streamlit run app.py
```

### Key Features Usage

1. **Road Network Optimization**
   - Access through the "Suggest new road network" option
   - Input parameters for network optimization
   - View optimized road network suggestions

2. **Route Planning**
   - Select "Find best route between two locations"
   - Input source and destination
   - Choose optimization criteria (shortest distance, time, etc.)

3. **Public Transport Scheduling**
   - Navigate to "Visualize public transport scheduling"
   - Input available resources (buses, trains)
   - Generate optimized schedules

4. **Maintenance Planning**
   - Select "Plan road maintenance"
   - Input budget constraints
   - Generate maintenance schedule

## Algorithms Implemented

### 1. Graph Algorithms
- Dijkstra's Algorithm (in `shortest_path/`)
- A* Algorithm (in `shortest_path/`)
- Minimum Spanning Tree (in `mst/`)
- Breadth-First Search
- Depth-First Search

### 2. Optimization Algorithms
- Dynamic Programming (in `dp_optimization/`)
  - Maintenance scheduling (`dp_maintenance.py`)
  - Transport scheduling (`dp_scheduler.py`)
- Greedy Algorithms (in `greedy_signals/`)
  - Traffic signal optimization

### 3. Testing
- Graph testing (`testing/test_graph.py`)

## Team
👥 Team Runtime Terror
- [Omnia Adel Saber](https://github.com/Omnia-adel1)
- [Mariam Elrafei Mohamed](https://github.com/Mariam-abdelfttah)
- [Shams Abd Elhalim Abo Ghannam](https://github.com/shams8795)
- [Abdelrahman Amr Mohamed](https://github.com/AmRo1011)

##🙏 Acknowledgments
Special thanks to:

Eng. Ahmed M. Yahia – for guidance and feedback

AIU Faculty – for providing a supportive learning environment

Open-source community

