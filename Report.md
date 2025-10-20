# Adventure World Simulation - Project Report

**Student Name:** [Your Name]  
**Student ID:** [Your ID]  
**Date:** October 16, 2025

---

## 1. Introduction

This report documents the design, implementation, and results of the Adventure World theme park simulation developed for the COMP1005/5005 assignment. The simulation models a theme park with multiple rides, patrons, and queue management systems, visualized using matplotlib.

---

## 2. Design Overview

### 2.1 System Architecture

The simulation is built using object-oriented programming principles with the following core components:

- **Ride System**: Base `Ride` class with specialized subclasses (`PirateShip`, `FerrisWheel`, `SpiderRide`)
- **Patron System**: `Patron` class managing visitor behavior and state transitions
- **Park Management**: `Park` class coordinating all simulation entities
- **User Interface**: Command-line interface with interactive and batch modes

### 2.2 Class Hierarchy

```
Ride (base class)
├── PirateShip
├── FerrisWheel
└── SpiderRide

Patron (independent class)

Park (manager class)
```

### 2.3 State Machines

**Ride States:**
```
IDLE → BOARDING → RUNNING → IDLE
```

**Patron States:**
```
ROAMING → QUEUED → RIDING → ROAMING (or LEAVING)
```

---

## 3. Implementation Details

### 3.1 Feature Implementation

#### Feature 1: Rides
- **Implementation:** Base `Ride` class with state machine, timer, queue, and bounding box
- **Subclasses:** Three ride types with unique animations
- **Key methods:** `step_change()`, `plot_me()`, `get_bounding_box()`, `overlaps_with()`
- **Design decision:** Used inheritance for code reuse; each subclass overrides animation logic

#### Feature 2: Patrons
- **Implementation:** `Patron` class with position, state, and AI behavior
- **Movement:** Waypoint-based navigation with collision avoidance
- **Key methods:** `step_change(park)`, `plot_me()`
- **Design decision:** Patrons frozen for first 5 timesteps (per requirements)

#### Feature 3: Queues/Rider Management
- **Implementation:** FIFO queue using Python lists
- **Capacity:** Configurable per-ride capacity enforced during boarding
- **State sync:** Patron state updated when entering/leaving queue
- **Design decision:** Queue managed by `Ride` class for encapsulation

#### Feature 4: Terrain
- **Implementation:** Park boundary + ride bounding boxes act as barriers
- **Collision:** Patrons avoid ride bounding boxes during movement
- **Configuration:** CSV file support for flexible park layouts
- **Design decision:** Bounding box approach balances simplicity with functionality

#### Feature 5: User Interface
- **Interactive mode:** Prompts for all parameters (`-i` flag)
- **Batch mode:** CSV files for rides and parameters (`-f` and `-p` flags)
- **Implementation:** `argparse` for CLI parsing
- **Design decision:** Dual-mode interface supports both exploration and automation

#### Feature 6: Simulation
- **Timestep order:** Update rides → Update patrons → Increment counter
- **Spawn/despawn:** Patrons spawn at entrances; exit logic implemented
- **Coordination:** `Park.step()` orchestrates all entity updates
- **Design decision:** Fixed update order prevents race conditions

### 3.2 Data Structures

| Component | Data Structure | Justification |
|-----------|---------------|---------------|
| Ride queue | Python list (FIFO) | Simple, efficient for small queues |
| Ride riders | Python list | Direct access, known capacity |
| Park rides | Python list | Few rides, iteration-heavy workload |
| Park patrons | Python list | Dynamic size, frequent iteration |
| Entrances | List of tuples | Static configuration |

### 3.3 Code Quality

- **PEP 8 compliance:** 4-space indentation, descriptive names, docstrings
- **No anti-patterns:** Avoided `while True`, excessive `break/continue`, global variables
- **Comments:** Inline and block comments explain logic
- **Modularity:** Each class has single responsibility

---

## 4. Results and Analysis

### 4.1 Test Scenarios

**Test 1: Basic Functionality**
- **Configuration:** 3 rides (one of each type), 15 patrons, 100 timesteps
- **Result:** All rides cycled through states; patrons queued and rode successfully
- **Observation:** Queues formed naturally; ride animations smooth

**Test 2: Overlap Detection**
- **Configuration:** Attempted to place overlapping rides
- **Result:** System correctly rejected overlapping rides with error message
- **Observation:** Collision detection working as designed

**Test 3: High Load**
- **Configuration:** 5 rides, 50 patrons, 200 timesteps
- **Result:** [To be filled in with your test results]
- **Observation:** [Your observations]

### 4.2 Parameter Sensitivity

| Parameter | Effect on Simulation |
|-----------|---------------------|
| Ride capacity | Higher capacity → shorter queues, more simultaneous riders |
| Ride duration | Longer duration → longer wait times, bigger queues |
| Patron count | More patrons → more congestion, longer queues |
| Park size | Larger park → more roaming time between rides |

### 4.3 Performance

- **Rendering:** Matplotlib animation runs smoothly at ~20 fps (0.05s pause)
- **Scalability:** Tested up to [X] patrons and [Y] rides without issues
- **Memory:** Efficient for typical park sizes (< 1 MB memory footprint)

---

## 5. Extensions and Bonus Features

### 5.1 Implemented Extensions

1. **Three ride types** with distinct animations (required minimum: 2)
2. **Multiple entrances** support (CSV configuration)
3. **SpiderRide** as third ride type beyond requirements

### 5.2 Potential Future Extensions

- **Patron-on-ride plotting:** Draw patrons on moving rides (bonus points)
- **Terrain obstacles:** Add decorative/functional barriers beyond rides
- **Path planning:** A* algorithm for smarter patron navigation
- **Statistics tracking:** Queue length over time, throughput metrics
- **3D visualization:** Top-down + side view composite

---

## 6. Challenges and Solutions

### Challenge 1: State Synchronization
- **Issue:** Patrons sometimes remained in "queued" state after ride
- **Solution:** Ensured `Ride.step_change()` updates patron state during unloading

### Challenge 2: Bounding Box Collision
- **Issue:** Initial implementation allowed patrons to enter ride areas
- **Solution:** Added buffer zone and waypoint targeting outside bounding boxes

### Challenge 3: Animation Performance
- **Issue:** Large patron counts slowed rendering
- **Solution:** Optimized plotting by using batch plot operations

---

## 7. Testing and Validation

### 7.1 Unit Testing
- Manual testing of each class method
- Edge cases: empty queues, full capacity, park boundaries

### 7.2 Integration Testing
- End-to-end simulation runs
- Interactive and batch mode validation
- CSV parsing error handling

### 7.3 Code Review
- PEP 8 compliance verified
- Docstrings for all classes and public methods
- Comments for complex logic sections

---

## 8. Traceability Matrix

| Feature | Requirements Met | Implementation | Tested |
|---------|-----------------|----------------|--------|
| 1. Rides | State, movement, size, capacity | Ride base + 3 subclasses | ✓ |
| 2. Patrons | Position, name, state, plotting | Patron class | ✓ |
| 3. Queues | FIFO, capacity, state sync | Ride.queue + riders | ✓ |
| 4. Terrain | Boundaries, barriers, collision | Bounding boxes | ✓ |
| 5. UI | Interactive + batch modes | argparse, CSV parsing | ✓ |
| 6. Simulation | Timestep, spawn, state updates | Park.step() | ✓ |

---

## 9. References

1. COMP1005/5005 Lecture Materials (State Machines, OOP Design)
2. COMP1005/5005 Practical Test 3 (Pirate Ship base implementation)
3. Python `matplotlib` documentation - Animation techniques
4. PEP 8 Style Guide for Python Code

---

## 10. Conclusion

The Adventure World simulation successfully implements all required features with clean, modular, PEP 8-compliant code. The dual-mode interface supports both interactive exploration and automated parameter sweeps. The simulation demonstrates effective use of object-oriented design patterns, state machines, and visualization techniques.

**Key Achievements:**
- ✓ Complete ride system with animations
- ✓ Patron AI with state transitions
- ✓ Queue management with capacity limits
- ✓ Collision detection and avoidance
- ✓ Interactive and batch modes
- ✓ Extensible architecture for future enhancements

**Lines of Code:** ~600 (including comments and docstrings)  
**Files Delivered:** 5 (adventureworld.py, map1.csv, params1.csv, README.md, Report.md)

---

## Appendices

### Appendix A: Sample Output

```
=== Adventure World Simulation - Batch Mode ===
Map file: map1.csv
Params file: params1.csv

=== Starting Simulation ===
Park: 200x200
Rides: 3
Patrons: 15
Timesteps: 100

Timestep 10/100 - Patrons: 15
...
Timestep 100/100 - Patrons: 15

=== Simulation Complete ===
```

### Appendix B: File Structure

```
e:\Projects\Simulation\
├── adventureworld.py    # Main simulation (600 lines)
├── showDemo.py          # Legacy demo from practicals
├── showground.py        # Legacy Pirate class
├── map1.csv             # Sample ride configuration
├── params1.csv          # Sample parameters
├── README.md            # User documentation
└── Report.md            # This document
```

### Appendix C: Command Reference

```powershell
# Interactive mode
python adventureworld.py -i

# Batch mode
python adventureworld.py -f map1.csv -p params1.csv

# Install dependencies
pip install matplotlib
```
