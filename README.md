# 🎡 Adventure World Theme Park Simulation

A complete Python simulation of a theme park with animated rides, intelligent patrons, queue management, and a stunning modern dark-themed dashboard.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## ✨ Features

### 🎢 Three Types of Animated Rides
- **PirateShip**: Swinging arc animation with smooth back-and-forth motion
- **FerrisWheel**: Rotating wheel with spokes and gondolas
- **SpiderRide**: Fast-rotating arms with multiple carriages

**Each ride includes:**
- ✅ Configurable capacity and duration
- ✅ Bounding box collision detection
- ✅ FIFO queue management
- ✅ 3-state machine: `idle` → `boarding` → `running` → `idle`
- ✅ Visual state indicators (💤 idle, ⏳ boarding, ⚡ running)
- ✅ Real-time capacity tracking

### 👥 Intelligent Patrons
- **4-State Machine**: `roaming` → `queued` → `riding` → `leaving`
- **Smart Behavior**: 
  - Spawn at designated park entrances
  - Frozen for first 5 timesteps (assignment requirement)
  - Random movement with ride-targeting behavior
  - Collision avoidance with ride bounding boxes
  - Automatic queue joining when near rides
  - Exit park after riding

### 🎯 Park Management
- Configurable park dimensions (any width × height)
- Multiple entrances/exits support
- Overlap detection prevents ride placement conflicts
- Real-time statistics tracking
- Terrain boundary enforcement

### 🌙 Modern Dark-Themed Dashboard
- **4-Panel Layout**: Main park view + Statistics + Rides + Patrons
- **Stunning Visuals**: Dark blue theme (#0a1929) with neon cyan accents
- **Real-Time Updates**: All panels update every timestep
- **Animated Elements**: Pulsing grid, glowing patrons, progress bars
- **Professional Design**: Rounded panels, modern typography, color-coded states

---

## 🚀 Quick Start

**Run the simulation in 30 seconds:**

```powershell
cd e:\Projects\Simulation
python adventureworld.py -f map1.csv -p params1.csv
```

**What you'll see:**
- 🎡 **Adventure World** main park view with 3 animated rides
- 📈 **Statistics** panel with live progress bar and counts
- 🎢 **Rides** panel showing queue lengths and capacity
- 👨‍👩‍👧‍👦 **Patrons** panel with distribution donut chart

---

## 📦 Requirements

### Software
- **Python**: 3.7 or higher
- **matplotlib**: 3.0 or higher
- **numpy**: Any recent version (optional, for advanced features)

### Operating System
- ✅ Windows (PowerShell recommended)
- ✅ macOS (Terminal)
- ✅ Linux (Bash)

---

## 💿 Installation

### 1. Install Python
Download from [python.org](https://www.python.org/downloads/) (version 3.7+)

### 2. Install Dependencies
```powershell
pip install matplotlib numpy
```

### 3. Verify Installation
```powershell
python --version          # Should show 3.7 or higher
python -m pip list        # Should show matplotlib and numpy
```

### 4. Download Files
Ensure you have these files in your project directory:
```
e:\Projects\Simulation\
├── adventureworld.py     # Main simulation (1156 lines)
├── map1.csv              # Sample ride configuration
├── params1.csv           # Sample parameters
├── map2.csv              # Alternative configuration
├── params2.csv           # Alternative parameters
├── showDemo.py           # Reference file (optional)
└── showground.py         # Reference file (optional)
```

---

## 🎮 Usage

### Interactive Mode

Prompts you for all configuration details:

```powershell
python adventureworld.py -i
```

**You'll be asked for:**
1. Park width (e.g., `200`)
2. Park height (e.g., `200`)
3. Entrance coordinates (e.g., `10`, `10`)
4. Number of rides (e.g., `3`)
5. For each ride:
   - Type: `1` (PirateShip), `2` (FerrisWheel), `3` (SpiderRide)
   - Position X, Y
   - Capacity (e.g., `10`)
   - Duration in timesteps (e.g., `20`)
6. Number of patrons (e.g., `15`)
7. Number of timesteps (e.g., `100`)

**Tip**: Press Enter to accept default values shown in brackets.

### Batch Mode

Load configuration from CSV files:

```powershell
python adventureworld.py -f map1.csv -p params1.csv
```

**Advantages:**
- ✅ Repeatable configurations
- ✅ Quick testing of different scenarios
- ✅ No manual input required
- ✅ Easy to share configurations

**Example configurations provided:**
- `map1.csv` + `params1.csv`: 3 rides, 15 patrons, 100 timesteps
- `map2.csv` + `params2.csv`: Alternative setup

---

## 📄 Configuration Files

### params.csv Format

```csv
park_width,park_height,entrances,num_patrons,timesteps
200,200,"10:10",15,100
```

**Fields:**
- `park_width`: Width of park (pixels)
- `park_height`: Height of park (pixels)
- `entrances`: Semicolon-separated coordinates `"x1:y1;x2:y2"`
- `num_patrons`: Total patrons to spawn
- `timesteps`: Simulation duration

### map.csv Format

```csv
ride_type,x,y,capacity,duration
PirateShip,60,100,10,20
FerrisWheel,120,100,12,15
SpiderRide,180,100,8,12
```

**Fields:**
- `ride_type`: `PirateShip`, `FerrisWheel`, or `SpiderRide`
- `x`, `y`: Position in park
- `capacity`: Maximum riders at once
- `duration`: Timesteps per ride cycle

**Example Configurations:**

**Small Park (Quick Test):**
```csv
# params.csv
park_width,park_height,entrances,num_patrons,timesteps
150,150,"10:10",8,50
```

**Large Park (Full Demo):**
```csv
# params.csv
park_width,park_height,entrances,num_patrons,timesteps
300,300,"10:10;290:290",30,200
```

---

## 🏗️ Architecture

### Class Structure

```
Ride (Base Class)
├── PirateShip
├── FerrisWheel
└── SpiderRide

Patron (State Machine)
├── states: roaming, queued, riding, leaving
└── methods: update(), is_in_bounds()

Park (Manager)
├── rides: List[Ride]
├── patrons: List[Patron]
├── entrances: List[Tuple[int, int]]
└── methods: add_ride(), spawn_patron(), step()
```

### Ride State Machine

```
┌──────┐
│ IDLE │ ←──────────────┐
└──┬───┘                │
   │ patrons in queue   │
   ↓                    │
┌──────────┐            │
│ BOARDING │            │
└──┬───────┘            │
   │ full or timeout    │
   ↓                    │
┌─────────┐             │
│ RUNNING │             │
└──┬──────┘             │
   │ duration complete  │
   └────────────────────┘
```

### Patron State Machine

```
┌─────────┐
│ ROAMING │ ←─────────────────┐
└──┬──────┘                   │
   │ near ride               │
   ↓                         │
┌────────┐                   │
│ QUEUED │                   │
└──┬─────┘                   │
   │ ride boards             │
   ↓                         │
┌────────┐                   │
│ RIDING │                   │
└──┬─────┘                   │
   │ ride finishes           │
   ↓                         │
┌─────────┐                  │
│ LEAVING │──────────────────┘
└─────────┘   exit or re-roam
```

### Key Design Patterns

- **Inheritance**: Ride base class with specialized subclasses
- **State Machine**: Both rides and patrons use state-based behavior
- **Observer**: Park tracks and updates all entities
- **Factory**: Ride creation based on string type
- **FIFO Queue**: First-in-first-out patron queuing

---

## 🎨 UI Dashboard

### Panel Layout (4x4 GridSpec)

```
┌─────────────────────────┬───────────┐
│                         │  📈       │
│    🎡 ADVENTURE WORLD   │  STATS    │
│    (Main Park View)     │           │
│                         ├───────────┤
│   • Rides animate       │  🎢       │
│   • Patrons move        │  RIDES    │
│   • Glowing effects     │           │
│   • Entrance markers    ├───────────┤
│                         │  👨‍👩‍👧‍👦    │
│                         │  PATRONS  │
│                         │           │
└─────────────────────────┴───────────┘
```

### Visual Elements

#### 🎡 Adventure World (Main Park View)
- **Title**: Large animated title with subtitle showing timestep
- **Boundary**: Rounded glass-effect border
- **Grid**: Animated pulsing grid lines
- **Entrances**: Star markers with cyan glow and labels
- **Rides**: Animated with state indicators and info cards
- **Patrons**: Colored dots with multi-layer glow effects
  - 🟢 Green = Roaming
  - 🔵 Blue = Queued
  - 🔴 Red = Riding
  - ⚪ Gray = Leaving

#### 📈 Statistics Panel
- **Progress Bar**: Animated bar showing simulation progress
- **Live Counts**:
  - ⏱️ Timestep counter
  - 👥 Total spawned
  - 🎯 Active patrons
  - 🚶 Roaming count
  - ⏳ Queued count
  - 🎢 Riding count
  - 👋 Leaving count

#### 🎢 Rides Panel
- **Per-Ride Cards**:
  - State emoji (💤/⏳/⚡)
  - Ride type name
  - Queue length: `Q:2`
  - Riders: `R:10/10` (current/capacity)
  - Capacity bar visualization

#### 👨‍👩‍👧‍👦 Patrons Panel
- **Donut Chart**: Shows distribution by state
- **Center Text**: Total active patrons
- **Legend**: Color-coded state labels with counts
- **Percentages**: Auto-calculated for each segment

---

## 🎨 Color Scheme

### Dark Theme Palette

| Element | Color | Hex Code | Usage |
|---------|-------|----------|-------|
| **Background** | Deep Navy | `#0a1929` | Main background |
| **Panel BG** | Dark Blue | `#132f4c` | Panel backgrounds |
| **Border** | Blue Gray | `#1e4976` | Panel borders |
| **Accent** | Neon Cyan | `#00d4ff` | Highlights, titles |
| **Text** | Light Blue | `#e3f2fd` | Labels, values |
| **Roaming** | Neon Green | `#00ff88` | Roaming patrons |
| **Queued** | Cyan | `#00d4ff` | Queued patrons |
| **Riding** | Hot Pink | `#ff3366` | Riding patrons |
| **Leaving** | Gray Blue | `#b8c5d6` | Leaving patrons |
| **Idle** | Muted Blue | `#3d5a80` | Idle rides |
| **Boarding** | Orange | `#ffa500` | Boarding rides |
| **Running** | Purple | `#8b5cf6` | Running rides |

### Changing Colors

Edit the `colors` dictionary in `adventureworld.py` (around line 714):

```python
colors = {
    'accent': '#00d4ff',      # Change accent color here
    'bg_dark': '#0a1929',     # Change background here
    'roaming': '#00ff88',     # Change patron colors here
    # ... etc
}
```

---

## 🔧 Customization

### Change Animation Speed

Edit line ~1110 in `adventureworld.py`:

```python
plt.pause(0.05)  # Change to 0.01 (faster) or 0.1 (slower)
```

### Change Figure Size

Edit line ~733 in `adventureworld.py`:

```python
fig = plt.figure(figsize=(18, 11))  # Change to (20, 12) for bigger
```

### Add New Ride Type

1. Create a new class inheriting from `Ride`:
```python
class RollerCoaster(Ride):
    def plot_me(self, ax):
        # Your animation code here
        pass
```

2. Update the ride type mapping in `main()`:
```python
ride_type_map = {
    'PirateShip': PirateShip,
    'FerrisWheel': FerrisWheel,
    'SpiderRide': SpiderRide,
    'RollerCoaster': RollerCoaster  # Add here
}
```

3. Add to CSV:
```csv
RollerCoaster,150,100,15,25
```

### Adjust Patron Behavior

Edit `Patron` class (lines 195-277):
- Change freeze duration: `self.frozen_time = 5` (line ~202)
- Adjust speed: Modify `dx`, `dy` calculations (line ~232-242)
- Change targeting: Edit ride detection logic (line ~246-253)

---

## 🐛 Troubleshooting

### Issue: "matplotlib not found"
**Solution:**
```powershell
pip install matplotlib
```

### Issue: "numpy not found"
**Solution:**
```powershell
pip install numpy
```

### Issue: "File not found: map1.csv"
**Solution:** Use interactive mode instead:
```powershell
python adventureworld.py -i
```

### Issue: Emoji showing as boxes (□)
**Effect:** Cosmetic only, doesn't affect functionality  
**Note:** This is a font rendering issue on some systems. The simulation works perfectly.

### Issue: Animation is too slow
**Solution:** Reduce timesteps or increase pause time:
```python
# In adventureworld.py, line ~1110
plt.pause(0.01)  # Smaller = faster
```

### Issue: Window is too small
**Solution:** Increase figure size:
```python
# In adventureworld.py, line ~733
fig = plt.figure(figsize=(20, 12))  # Bigger numbers = bigger window
```

### Issue: "Ride overlaps with existing ride"
**Solution:** 
- Use interactive mode and spread rides farther apart
- Edit CSV file with larger spacing between x,y coordinates
- Reduce ride sizes in the class definitions

### Issue: Patrons not moving
**Check:**
- Are you past timestep 5? (Patrons frozen for first 5 steps)
- Is park size large enough? (Minimum 100x100 recommended)
- Are entrances inside park boundaries?

### Issue: No patrons spawning
**Check:**
- `num_patrons` > 0 in params.csv
- Entrance coordinates are valid
- No errors in console output

---

## 📝 Assignment Requirements

### ✅ Core Requirements Met

| Requirement | Implementation | Location in Code |
|------------|----------------|------------------|
| **3 Ride Types** | PirateShip, FerrisWheel, SpiderRide | Lines 85-193 |
| **Object Movement** | Swinging, rotating animations | `plot_me()` methods |
| **Patron States** | 4-state machine with transitions | Lines 195-277 |
| **Queue Management** | FIFO queues per ride | `Ride.queue` (line 93) |
| **Interactive Mode** | Full CLI with prompts | Lines 614-703 |
| **Batch Mode** | CSV file parsing | Lines 568-613 |
| **Collision Detection** | Bounding box overlap checks | Lines 358-375 |
| **Visualization** | 4-panel matplotlib dashboard | Lines 705-1119 |
| **Documentation** | Comprehensive README | This file |

### Design Decisions

1. **State Machines**: Used for both rides and patrons to manage complex behavior transitions
2. **Inheritance**: Ride base class allows easy extension to new ride types
3. **GridSpec Layout**: Responsive 4-panel dashboard provides comprehensive view
4. **Dark Theme**: Modern aesthetic improves visibility and reduces eye strain
5. **Real-Time Updates**: All statistics calculated and displayed every timestep
6. **Neon Accents**: High-contrast colors ensure clarity of different states
7. **Glow Effects**: Multi-layer rendering provides depth and visual interest

### Performance Considerations

- **Efficient Rendering**: Only redraw what changes each frame
- **Optimized Collections**: Use lists for O(1) append operations
- **Minimal Calculations**: Cache frequently used values
- **Appropriate Pause**: 50ms delay balances smoothness with CPU usage

---

## 📊 Console Output

### Batch Mode Example

```
=== Adventure World Simulation - Batch Mode ===

Map file: map1.csv
Params file: params1.csv

=== Starting Simulation ===
Park: 200x200
Rides: 3
Patrons: 15
Timesteps: 100

Progress: [████████░░░░░░░░░░░░] 40.0%

⏱️  Timestep 10/100 | Patrons: 15 | Riding: 8 | Queued: 3
⏱️  Timestep 20/100 | Patrons: 14 | Riding: 12 | Queued: 1
⏱️  Timestep 30/100 | Patrons: 14 | Riding: 10 | Queued: 2
⏱️  Timestep 40/100 | Patrons: 13 | Riding: 11 | Queued: 1
⏱️  Timestep 50/100 | Patrons: 13 | Riding: 9 | Queued: 2

✅ === Simulation Complete ===
📊 Final Statistics:
   Total timesteps: 100
   Patrons spawned: 15
   Patrons remaining: 10
   Rides operated: 3
```

---

## 🎯 Testing

### Quick Test (30 seconds)
```powershell
python adventureworld.py -f map1.csv -p params1.csv
```

### Interactive Test (2 minutes)
```powershell
python adventureworld.py -i
# Use small values: 150x150 park, 3 rides, 10 patrons, 50 timesteps
```

### Stress Test (5 minutes)
```powershell
# Edit params1.csv:
# 300,300,"10:10;290:10;10:290",50,500
python adventureworld.py -f map1.csv -p params1.csv
```

---

## 📚 Code Structure Reference

### Main Components
- **Lines 1-84**: Imports and constants
- **Lines 85-193**: Ride classes (PirateShip, FerrisWheel, SpiderRide)
- **Lines 195-277**: Patron class with state machine
- **Lines 279-566**: Park class (simulation engine)
- **Lines 568-703**: Interactive and batch modes
- **Lines 705-1119**: Visualization with 4-panel dashboard
- **Lines 1121-1156**: Main entry point and CLI

### Key Functions
- `Park.step()`: Main simulation loop (line 479)
- `Patron.update()`: Patron behavior logic (line 219)
- `Ride.update()`: Ride state transitions (line 130)
- `run_simulation()`: Visualization engine (line 705)

---

## 🤝 Contributing

This is an assignment project, but improvements are welcome:
- Add new ride types
- Enhance patron AI
- Improve visualization effects
- Optimize performance
- Add more statistics

---

## 📄 License

MIT License - Free to use for educational purposes

---

## 🎓 Credits

**Author**: FOP Assignment Student  
**Course**: Foundations of Programming  
**Date**: October 2025  
**Version**: 2.0 (Dark Theme Edition)

---

## 🔗 Quick Command Reference

```powershell
# Run with default configuration
python adventureworld.py -f map1.csv -p params1.csv

# Run interactive mode
python adventureworld.py -i

# Install dependencies
pip install matplotlib numpy

# Check Python version
python --version

# Check installed packages
python -m pip list
```

---

**🎉 Enjoy the simulation!**

For questions or issues, review the [Troubleshooting](#-troubleshooting) section or check the inline code comments in `adventureworld.py`.
