#!/usr/bin/env python3
"""
adventureworld.py - Theme park simulation with rides, patrons, and queues.

Student Name: [Your Name]
Student ID: [Your ID]

Usage:
    Interactive mode: python adventureworld.py -i
    Batch mode:       python adventureworld.py -f map.csv -p params.csv
"""

import argparse
import csv
import math
import random
import matplotlib.pyplot as plt  # type: ignore
import matplotlib.patches as patches  # type: ignore
from matplotlib.gridspec import GridSpec  # type: ignore
from matplotlib.patches import FancyBboxPatch  # type: ignore
import numpy as np


# ============================================================================
# RIDE CLASSES
# ============================================================================

class Ride:
    """
    Base class for all rides in the theme park.
    
    Attributes:
        ride_id: Unique identifier for the ride
        x, y: Center position of the ride
        width, height: Bounding box dimensions
        capacity: Maximum number of riders at once
        duration: Number of timesteps the ride runs
        state: Current state (idle, boarding, running)
        queue: List of patrons waiting
        riders: List of patrons currently riding
        timer: Countdown timer for ride operation
    """
    
    def __init__(self, ride_id, x, y, width, height, capacity, duration):
        self.ride_id = ride_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.capacity = capacity
        self.duration = duration
        self.state = "idle"  # idle, boarding, running
        self.queue = []
        self.riders = []
        self.timer = 0
        
    def get_bounding_box(self):
        """Return (x_min, y_min, x_max, y_max) for collision detection."""
        half_w = self.width / 2
        half_h = self.height / 2
        return (self.x - half_w, self.y - half_h, 
                self.x + half_w, self.y + half_h)
    
    def overlaps_with(self, other_ride):
        """Check if this ride's bounding box overlaps with another ride."""
        x1_min, y1_min, x1_max, y1_max = self.get_bounding_box()
        x2_min, y2_min, x2_max, y2_max = other_ride.get_bounding_box()
        
        # No overlap if one box is to the side of the other
        if x1_max < x2_min or x2_max < x1_min:
            return False
        if y1_max < y2_min or y2_max < y1_min:
            return False
        return True
    
    def add_to_queue(self, patron):
        """Add a patron to the queue."""
        if patron not in self.queue:
            self.queue.append(patron)
            patron.state = "queued"
            patron.target_ride_id = self.ride_id
            
    def step_change(self):
        """
        Update ride state on each timestep.
        State machine: idle -> boarding -> running -> idle
        """
        if self.state == "idle":
            # Check if there are patrons in queue
            if len(self.queue) > 0:
                self.state = "boarding"
                self.timer = 2  # Boarding takes 2 timesteps
                
        elif self.state == "boarding":
            self.timer -= 1
            if self.timer <= 0:
                # Move patrons from queue to riders
                num_to_board = min(self.capacity, len(self.queue))
                for _ in range(num_to_board):
                    patron = self.queue.pop(0)
                    self.riders.append(patron)
                    patron.state = "riding"
                    patron.ride_timer = self.duration
                
                # Start the ride
                self.state = "running"
                self.timer = self.duration
                
        elif self.state == "running":
            self.timer -= 1
            # Update rider timers
            for rider in self.riders:
                rider.ride_timer -= 1
                
            if self.timer <= 0:
                # Unload riders
                for rider in self.riders:
                    rider.state = "roaming"
                    rider.target_ride_id = None
                    rider.ride_timer = 0
                self.riders = []
                self.state = "idle"
    
    def plot_me(self, ax):
        """Plot the ride and its queue (to be overridden by subclasses)."""
        # Draw bounding box with state-based coloring
        x_min, y_min, x_max, y_max = self.get_bounding_box()
        
        # State colors for dark theme
        state_colors = {
            'idle': '#1a3a52',     # Dark blue
            'boarding': '#ff8c00', # Orange
            'running': '#8b5cf6'   # Purple
        }
        fill_color = state_colors.get(self.state, '#1a3a52')
        border_color = {
            'idle': '#3d5a80',
            'boarding': '#ffa500',
            'running': '#a78bfa'
        }.get(self.state, '#3d5a80')
        
        rect = FancyBboxPatch((x_min, y_min), self.width, self.height,
                              boxstyle="round,pad=1.5",
                              linewidth=2.5, edgecolor=border_color, 
                              facecolor=fill_color, alpha=0.5)
        ax.add_patch(rect)
        
        # Add glow effect when running
        if self.state == 'running':
            glow = FancyBboxPatch((x_min - 1, y_min - 1), 
                                  self.width + 2, self.height + 2,
                                  boxstyle="round,pad=1.5",
                                  linewidth=1, edgecolor=border_color, 
                                  facecolor='none', alpha=0.3)
            ax.add_patch(glow)
        
        # Label the ride with ID
        ax.text(self.x, y_max + 3, f"RIDE {self.ride_id}", 
                ha='center', va='bottom', fontsize=9.5,
                fontweight='bold', color='#00d4ff')
        
        # Plot queue positions with enhanced style
        if len(self.queue) > 0:
            queue_x = x_min - 10
            for i, patron in enumerate(self.queue):
                # Queue line connector
                if i == 0:
                    ax.plot([queue_x + 3, x_min], 
                           [y_min + i * 2.5, y_min], 
                           '--', color='#00d4ff', alpha=0.3, linewidth=1)
                
                # Patron in queue with glow
                ax.plot(queue_x, y_min + i * 2.5, 'o',
                       color='#00d4ff', markersize=8,
                       alpha=0.3, zorder=2)
                ax.plot(queue_x, y_min + i * 2.5, 'o',
                       color='#00d4ff', markersize=5,
                       markeredgecolor='#0a1929', 
                       markeredgewidth=1, zorder=3)


class PirateShip(Ride):
    """
    Pirate ship ride that swings back and forth in an arc.
    """
    
    def __init__(self, ride_id, x, y, capacity=10, duration=20):
        super().__init__(ride_id, x, y, width=20, height=30, 
                         capacity=capacity, duration=duration)
        self.angle = 0  # Current swing angle
        self.direction = 1  # 1 for right, -1 for left
        self.max_angle = 60  # Maximum swing angle in degrees
        
    def step_change(self):
        """Update ride state and animate the swing."""
        super().step_change()
        
        # Animate swing when running
        if self.state == "running":
            self.angle += 3 * self.direction
            if abs(self.angle) >= self.max_angle:
                self.direction *= -1
    
    def plot_me(self, ax):
        """Plot the pirate ship with swinging animation."""
        super().plot_me(ax)
        
        # Draw the ship as a line that rotates with enhanced styling
        length = 15
        angle_rad = math.radians(self.angle)
        end_x = self.x + length * math.sin(angle_rad)
        end_y = self.y - length * math.cos(angle_rad)
        
        # Draw pivot point
        ax.plot(self.x, self.y, 'o', color='#34495e', markersize=8,
               markeredgecolor='white', markeredgewidth=1.5, zorder=5)
        
        # Draw swing arm
        ax.plot([self.x, end_x], [self.y, end_y], '-',
               color='#e74c3c', linewidth=4, zorder=4)
        
        # Draw ship at the end
        ax.plot(end_x, end_y, 's', color='#c0392b', markersize=12,
               markeredgecolor='white', markeredgewidth=1.5, zorder=5)


class FerrisWheel(Ride):
    """
    Ferris wheel ride that rotates continuously.
    """
    
    def __init__(self, ride_id, x, y, capacity=12, duration=30):
        super().__init__(ride_id, x, y, width=25, height=25, 
                         capacity=capacity, duration=duration)
        self.angle = 0  # Current rotation angle
        self.radius = 12
        
    def step_change(self):
        """Update ride state and rotate the wheel."""
        super().step_change()
        
        # Rotate when running
        if self.state == "running":
            self.angle += 5  # Degrees per timestep
            if self.angle >= 360:
                self.angle -= 360
    
    def plot_me(self, ax):
        """Plot the ferris wheel with rotation."""
        super().plot_me(ax)
        
        # Draw the wheel as a circle with enhanced styling
        circle = patches.Circle((self.x, self.y), self.radius, 
                                fill=False, edgecolor='#3498db', 
                                linewidth=3, zorder=4)
        ax.add_patch(circle)
        
        # Draw center hub
        ax.plot(self.x, self.y, 'o', color='#2c3e50', markersize=10,
               markeredgecolor='white', markeredgewidth=1.5, zorder=5)
        
        # Draw spokes with cars
        num_spokes = 6
        for i in range(num_spokes):
            spoke_angle = math.radians(self.angle + i * (360 / num_spokes))
            end_x = self.x + self.radius * math.cos(spoke_angle)
            end_y = self.y + self.radius * math.sin(spoke_angle)
            
            # Spoke line
            ax.plot([self.x, end_x], [self.y, end_y], '-',
                   color='#95a5a6', linewidth=1.5, zorder=3)
            
            # Car at the end
            ax.plot(end_x, end_y, 's', color='#3498db', markersize=8,
                   markeredgecolor='white', markeredgewidth=1, zorder=5)


class SpiderRide(Ride):
    """
    Spider/Hurricane ride with rotating arms.
    """
    
    def __init__(self, ride_id, x, y, capacity=8, duration=25):
        super().__init__(ride_id, x, y, width=30, height=30, 
                         capacity=capacity, duration=duration)
        self.angle = 0
        self.num_arms = 4
        self.arm_length = 14
        
    def step_change(self):
        """Update ride state and rotate arms."""
        super().step_change()
        
        if self.state == "running":
            self.angle += 8  # Fast rotation
            if self.angle >= 360:
                self.angle -= 360
    
    def plot_me(self, ax):
        """Plot the spider ride with rotating arms."""
        super().plot_me(ax)
        
        # Draw center hub
        ax.plot(self.x, self.y, 'o', color='#27ae60', markersize=12,
               markeredgecolor='white', markeredgewidth=2, zorder=5)
        
        # Draw rotating arms with enhanced styling
        for i in range(self.num_arms):
            arm_angle = math.radians(self.angle + i * (360 / self.num_arms))
            end_x = self.x + self.arm_length * math.cos(arm_angle)
            end_y = self.y + self.arm_length * math.sin(arm_angle)
            
            # Arm line
            ax.plot([self.x, end_x], [self.y, end_y], '-',
                   color='#16a085', linewidth=3, zorder=4)
            
            # Car at end
            ax.plot(end_x, end_y, 'o', color='#2ecc71', markersize=10,
                   markeredgecolor='white', markeredgewidth=1.5, zorder=5)


# ============================================================================
# PATRON CLASS
# ============================================================================

class Patron:
    """
    Represents a patron in the theme park.
    
    States: roaming, queued, riding, leaving
    """
    
    def __init__(self, patron_id, x, y, speed=2.0):
        self.patron_id = patron_id
        self.x = x
        self.y = y
        self.speed = speed
        self.state = "roaming"  # roaming, queued, riding, leaving
        self.target_ride_id = None
        self.target_x = None
        self.target_y = None
        self.ride_timer = 0
        self.rides_taken = 0
        self.frozen_timer = 5  # Don't move for first 5 timesteps
        
    def step_change(self, park):
        """
        Update patron position and state based on current state.
        """
        # Don't move for first 5 timesteps
        if self.frozen_timer > 0:
            self.frozen_timer -= 1
            return
            
        if self.state == "roaming":
            # Choose a target if we don't have one
            if self.target_x is None or self.target_y is None:
                # Randomly decide: go to a ride or wander
                if random.random() < 0.7 and len(park.rides) > 0:
                    # Pick a random ride to go to
                    ride = random.choice(park.rides)
                    self.target_ride_id = ride.ride_id
                    # Target a position outside the ride's bounding box
                    x_min, y_min, x_max, y_max = ride.get_bounding_box()
                    self.target_x = x_min - 5
                    self.target_y = (y_min + y_max) / 2
                else:
                    # Wander to random position
                    self.target_x = random.uniform(10, park.width - 10)
                    self.target_y = random.uniform(10, park.height - 10)
            
            # Move towards target
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist < self.speed:
                self.x = self.target_x
                self.y = self.target_y
                
                # Check if we reached a ride
                if self.target_ride_id is not None:
                    ride = park.get_ride_by_id(self.target_ride_id)
                    if ride is not None:
                        ride.add_to_queue(self)
                
                # Clear target
                self.target_x = None
                self.target_y = None
                self.target_ride_id = None
            else:
                # Move towards target
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed
            
            # Keep within park bounds
            self.x = max(5, min(park.width - 5, self.x))
            self.y = max(5, min(park.height - 5, self.y))
            
        elif self.state == "queued":
            # Waiting in queue, position managed by ride
            pass
            
        elif self.state == "riding":
            # On the ride, position managed by ride
            pass
            
        elif self.state == "leaving":
            # Move towards nearest exit
            if len(park.entrances) > 0:
                exit_x, exit_y = park.entrances[0]
                dx = exit_x - self.x
                dy = exit_y - self.y
                dist = math.sqrt(dx**2 + dy**2)
                
                if dist < self.speed:
                    park.remove_patron(self)
                else:
                    self.x += (dx / dist) * self.speed
                    self.y += (dy / dist) * self.speed
    
    def plot_me(self, ax):
        """Plot the patron as a colored dot based on state."""
        if self.state == "roaming":
            ax.plot(self.x, self.y, 'go', markersize=4)
        elif self.state == "queued":
            ax.plot(self.x, self.y, 'bo', markersize=4)
        elif self.state == "riding":
            # Optionally plot on ride (bonus feature)
            ax.plot(self.x, self.y, 'ro', markersize=4)
        elif self.state == "leaving":
            ax.plot(self.x, self.y, 'ko', markersize=4)


# ============================================================================
# PARK CLASS
# ============================================================================

class Park:
    """
    Manages the entire theme park simulation.
    """
    
    def __init__(self, width, height, entrances=None):
        self.width = width
        self.height = height
        self.rides = []
        self.patrons = []
        self.entrances = entrances if entrances else [(10, 10)]
        self.timestep = 0
        self.patrons_spawned = 0
        
    def add_ride(self, ride):
        """
        Add a ride to the park, checking for overlaps.
        Returns True if successful, False if overlap detected.
        """
        for existing_ride in self.rides:
            if ride.overlaps_with(existing_ride):
                print(f"Error: Ride {ride.ride_id} overlaps with "
                      f"Ride {existing_ride.ride_id}")
                return False
        self.rides.append(ride)
        return True
    
    def spawn_patron(self):
        """Spawn a new patron at a random entrance."""
        entrance_x, entrance_y = random.choice(self.entrances)
        patron = Patron(self.patrons_spawned, entrance_x, entrance_y)
        self.patrons.append(patron)
        self.patrons_spawned += 1
        
    def remove_patron(self, patron):
        """Remove a patron from the park."""
        if patron in self.patrons:
            self.patrons.remove(patron)
    
    def get_ride_by_id(self, ride_id):
        """Find a ride by its ID."""
        for ride in self.rides:
            if ride.ride_id == ride_id:
                return ride
        return None
    
    def step(self):
        """
        Execute one timestep of the simulation.
        Order: spawn, update rides, update patrons, timestep increment.
        """
        # Update all rides
        for ride in self.rides:
            ride.step_change()
        
        # Update all patrons
        patrons_copy = self.patrons.copy()  # Avoid modification during iteration
        for patron in patrons_copy:
            patron.step_change(self)
        
        self.timestep += 1
    
    def plot(self, ax):
        """Plot the entire park state."""
        ax.clear()
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')
        ax.set_title(f"Adventure World - Timestep {self.timestep}")
        
        # Draw park boundary
        boundary = patches.Rectangle((0, 0), self.width, self.height,
                                     linewidth=2, edgecolor='black', 
                                     facecolor='lightgreen', alpha=0.2)
        ax.add_patch(boundary)
        
        # Draw entrances
        for entrance_x, entrance_y in self.entrances:
            ax.plot(entrance_x, entrance_y, 'r*', markersize=15, 
                   label='Entrance' if entrance_x == self.entrances[0][0] else '')
        
        # Plot all rides
        for ride in self.rides:
            ride.plot_me(ax)
        
        # Plot all patrons
        for patron in self.patrons:
            patron.plot_me(ax)
        
        # Add legend
        ax.legend(loc='upper right', fontsize=8)
    
    def get_statistics(self):
        """Calculate current statistics for the dashboard."""
        stats = {
            'timestep': self.timestep,
            'total_patrons': len(self.patrons),
            'roaming': sum(1 for p in self.patrons if p.state == 'roaming'),
            'queued': sum(1 for p in self.patrons if p.state == 'queued'),
            'riding': sum(1 for p in self.patrons if p.state == 'riding'),
            'leaving': sum(1 for p in self.patrons if p.state == 'leaving'),
            'total_spawned': self.patrons_spawned,
            'rides': []
        }
        
        for ride in self.rides:
            ride_stats = {
                'id': ride.ride_id,
                'type': ride.__class__.__name__,
                'state': ride.state,
                'queue_length': len(ride.queue),
                'riders': len(ride.riders),
                'capacity': ride.capacity
            }
            stats['rides'].append(ride_stats)
        
        return stats


# ============================================================================
# INTERACTIVE MODE
# ============================================================================

def interactive_mode():
    """
    Run the simulation in interactive mode, prompting user for parameters.
    """
    print("=== Adventure World Simulation - Interactive Mode ===\n")
    
    # Get park parameters
    width = int(input("Enter park width (e.g., 200): ") or 200)
    height = int(input("Enter park height (e.g., 200): ") or 200)
    
    # Get entrance
    entrance_x = int(input("Enter entrance X position (e.g., 10): ") or 10)
    entrance_y = int(input("Enter entrance Y position (e.g., 10): ") or 10)
    
    park = Park(width, height, [(entrance_x, entrance_y)])
    
    # Add rides
    num_rides = int(input("Enter number of rides (e.g., 3): ") or 3)
    for i in range(num_rides):
        print(f"\n--- Ride {i+1} ---")
        print("Ride types: 1=PirateShip, 2=FerrisWheel, 3=SpiderRide")
        ride_type = int(input("Enter ride type (1-3): ") or 1)
        
        x = int(input(f"  X position (e.g., {50 + i*70}): ") or (50 + i*70))
        y = int(input(f"  Y position (e.g., 100): ") or 100)
        capacity = int(input("  Capacity (e.g., 10): ") or 10)
        duration = int(input("  Duration in timesteps (e.g., 20): ") or 20)
        
        if ride_type == 1:
            ride = PirateShip(i+1, x, y, capacity, duration)
        elif ride_type == 2:
            ride = FerrisWheel(i+1, x, y, capacity, duration)
        else:
            ride = SpiderRide(i+1, x, y, capacity, duration)
        
        if not park.add_ride(ride):
            print("Ride overlaps with existing ride. Skipping.")
    
    # Get patron parameters
    num_patrons = int(input("\nEnter number of patrons (e.g., 15): ") or 15)
    for _ in range(num_patrons):
        park.spawn_patron()
    
    # Get simulation parameters
    num_timesteps = int(input("Enter number of timesteps (e.g., 100): ") or 100)
    
    # Run simulation
    run_simulation(park, num_timesteps)


# ============================================================================
# BATCH MODE
# ============================================================================

def batch_mode(map_file, params_file):
    """
    Run the simulation in batch mode using CSV files.
    
    map_file format (rides.csv):
        ride_type,x,y,width,height,capacity,duration
        PirateShip,50,100,20,30,10,20
        FerrisWheel,120,100,25,25,12,30
    
    params_file format (params.csv):
        park_width,park_height,entrances,num_patrons,timesteps
        200,200,"10:10;190:190",15,100
    """
    print(f"=== Adventure World Simulation - Batch Mode ===\n")
    print(f"Map file: {map_file}")
    print(f"Params file: {params_file}\n")
    
    # Read parameters
    park_width = 200
    park_height = 200
    entrances = [(10, 10)]
    num_patrons = 15
    num_timesteps = 100
    
    try:
        with open(params_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header
            row = next(reader)
            park_width = int(row[0])
            park_height = int(row[1])
            
            # Parse entrances (format: "x1:y1;x2:y2")
            entrance_str = row[2].strip('"')
            entrances = []
            for entrance in entrance_str.split(';'):
                x, y = entrance.split(':')
                entrances.append((int(x), int(y)))
            
            num_patrons = int(row[3])
            num_timesteps = int(row[4])
    except FileNotFoundError:
        print(f"Warning: {params_file} not found. Using defaults.")
    except Exception as e:
        print(f"Warning: Error reading {params_file}: {e}. Using defaults.")
    
    park = Park(park_width, park_height, entrances)
    
    # Read rides
    ride_id = 1
    try:
        with open(map_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header
            for row in reader:
                ride_type = row[0]
                x = int(row[1])
                y = int(row[2])
                capacity = int(row[5])
                duration = int(row[6])
                
                if ride_type == "PirateShip":
                    ride = PirateShip(ride_id, x, y, capacity, duration)
                elif ride_type == "FerrisWheel":
                    ride = FerrisWheel(ride_id, x, y, capacity, duration)
                elif ride_type == "SpiderRide":
                    ride = SpiderRide(ride_id, x, y, capacity, duration)
                else:
                    print(f"Unknown ride type: {ride_type}")
                    continue
                
                if park.add_ride(ride):
                    ride_id += 1
    except FileNotFoundError:
        print(f"Error: {map_file} not found.")
        return
    except Exception as e:
        print(f"Error reading {map_file}: {e}")
        return
    
    # Spawn patrons
    for _ in range(num_patrons):
        park.spawn_patron()
    
    # Run simulation
    run_simulation(park, num_timesteps)


# ============================================================================
# SIMULATION RUNNER
# ============================================================================

def run_simulation(park, num_timesteps):
    """
    Run the simulation with a modern dashboard layout.
    """
    print(f"\n=== Starting Simulation ===")
    print(f"Park: {park.width}x{park.height}")
    print(f"Rides: {len(park.rides)}")
    print(f"Patrons: {len(park.patrons)}")
    print(f"Timesteps: {num_timesteps}\n")
    
    # Set up modern dark theme
    plt.style.use('dark_background')
    
    # Create figure with GridSpec for dashboard layout
    fig = plt.figure(figsize=(18, 11))
    fig.patch.set_facecolor('#0a1929')  # type: ignore  # Dark blue background
    gs = GridSpec(4, 4, figure=fig, hspace=0.35, wspace=0.35,
                  left=0.04, right=0.96, top=0.94, bottom=0.04)
    
    # Main park view (larger, left side) - spans 4 rows, 2.5 columns
    ax_park = fig.add_subplot(gs[:, :3])
    
    # Statistics panels (right side) - more refined layout
    ax_stats = fig.add_subplot(gs[0:2, 3])    # Top right - 2 rows
    ax_rides = fig.add_subplot(gs[2, 3])      # Middle right - 1 row
    ax_patrons = fig.add_subplot(gs[3, 3])    # Bottom right - 1 row
    
    # Modern dark blue color scheme with neon accents
    colors = {
        'roaming': '#00ff88',  # Neon green
        'queued': '#00d4ff',   # Cyan
        'riding': '#ff3366',   # Hot pink
        'leaving': '#b8c5d6',  # Light blue-gray
        'idle': '#3d5a80',     # Muted blue
        'boarding': '#ffa500', # Orange
        'running': '#8b5cf6',  # Purple
        'bg_dark': '#0a1929',  # Primary dark blue
        'bg_panel': '#132f4c', # Panel background
        'border': '#1e4976',   # Border color
        'text': '#e3f2fd',     # Light text
        'accent': '#00d4ff'    # Accent cyan
    }
    
    plt.ion()
    
    for t in range(num_timesteps):
        park.step()
        
        # Get current statistics
        stats = park.get_statistics()
        
        # ==================== MAIN PARK VIEW ====================
        ax_park.clear()
        ax_park.set_xlim(-5, park.width + 5)
        ax_park.set_ylim(-5, park.height + 5)
        ax_park.set_aspect('equal')
        ax_park.set_facecolor('#0d1b2a')  # Deep dark blue
        
        # Modern title with glow effect
        ax_park.text(park.width / 2, park.height + 10, 
                    'ADVENTURE WORLD', 
                    fontsize=18, fontweight='bold', 
                    ha='center', color=colors['accent'],
                    bbox=dict(boxstyle='round,pad=0.5', 
                             facecolor=colors['bg_dark'], 
                             alpha=0.8,
                             edgecolor=colors['accent'],
                             linewidth=2))
        
        # Subtitle with timestep info
        ax_park.text(park.width / 2, park.height + 3,
                    f"LIVE SIMULATION  |  Step {stats['timestep']}/{num_timesteps}",
                    fontsize=9, ha='center', color=colors['text'],
                    alpha=0.9, fontweight='bold')
        
        # Draw park boundary with modern glass effect
        boundary = FancyBboxPatch((0, 0), park.width, park.height,
                                  boxstyle="round,pad=3", 
                                  linewidth=2.5, 
                                  edgecolor=colors['accent'],
                                  facecolor=colors['bg_panel'], 
                                  alpha=0.2,
                                  linestyle='-')
        ax_park.add_patch(boundary)
        
        # Draw sleek grid with animation
        grid_alpha = 0.1 + 0.05 * math.sin(t * 0.1)  # Subtle pulse
        ax_park.grid(True, alpha=grid_alpha, linestyle=':', 
                    linewidth=0.8, color=colors['border'])
        
        # Draw entrances with modern style
        for idx, (entrance_x, entrance_y) in enumerate(park.entrances):
            # Outer glow
            ax_park.plot(entrance_x, entrance_y, marker='o', 
                        color=colors['accent'], markersize=35, 
                        alpha=0.2, zorder=1)
            # Main star
            ax_park.plot(entrance_x, entrance_y, marker='*', 
                        color=colors['accent'], markersize=28, 
                        markeredgecolor=colors['bg_dark'], 
                        markeredgewidth=2, zorder=5,
                        label='ENTRANCE' if idx == 0 else '')
            
            # Modern entrance label with glow
            ax_park.text(entrance_x, entrance_y - 10, 'ENTRANCE',
                        ha='center', fontsize=10, fontweight='bold',
                        color=colors['accent'],
                        bbox=dict(boxstyle='round,pad=0.6', 
                                 facecolor=colors['bg_panel'], 
                                 alpha=0.9,
                                 edgecolor=colors['accent'],
                                 linewidth=2))
        
        # Plot rides with enhanced visuals
        for ride in park.rides:
            ride.plot_me(ax_park)
            
            # Modern ride info card
            x_min, y_min, x_max, y_max = ride.get_bounding_box()
            
            # State indicator
            state_symbol = {
                'idle': 'IDLE',
                'boarding': 'WAIT',
                'running': 'RUN'
            }.get(ride.state, '*')
            
            label_text = f"{state_symbol} {ride.__class__.__name__[:8]}\n"
            label_text += f"Queue: {len(ride.queue)} | Riders: {len(ride.riders)}/{ride.capacity}"
            
            # Modern info card - place UNDER the ride, centered
            label_x = (x_min + x_max) / 2
            label_y = y_min - 4  # small gap below the ride box
            ax_park.text(label_x, label_y, label_text,
                        fontsize=8.5, va='top', ha='center',
                        color=colors['text'],
                        bbox=dict(boxstyle='round,pad=0.5',
                                 facecolor=colors['bg_panel'], 
                                 alpha=0.95,
                                 edgecolor=colors.get(ride.state, colors['border']),
                                 linewidth=2.5))
        
        # Plot patrons with enhanced glow effect
        for patron in park.patrons:
            color = colors.get(patron.state, 'gray')
            
            # Outer glow
            ax_park.plot(patron.x, patron.y, 'o', 
                        color=color, markersize=12,
                        alpha=0.3, zorder=2)
            # Inner bright dot
            ax_park.plot(patron.x, patron.y, 'o', 
                        color=color, markersize=7,
                        markeredgecolor=colors['bg_dark'], 
                        markeredgewidth=1.5, zorder=3)
            ax_park.plot(patron.x, patron.y, 'o', 
                        color=color, markersize=6,
                        markeredgecolor='white', markeredgewidth=0.5)
        
        # Add modern legend with dark theme
        from matplotlib.lines import Line2D  # type: ignore
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', 
                   markerfacecolor=colors['roaming'], markersize=9,
                   markeredgecolor=colors['bg_dark'], markeredgewidth=1.5,
                   label='Roaming'),
            Line2D([0], [0], marker='o', color='w',
                   markerfacecolor=colors['queued'], markersize=9,
                   markeredgecolor=colors['bg_dark'], markeredgewidth=1.5,
                   label='Queued'),
            Line2D([0], [0], marker='o', color='w',
                   markerfacecolor=colors['riding'], markersize=9,
                   markeredgecolor=colors['bg_dark'], markeredgewidth=1.5,
                   label='Riding'),
        ]
        legend = ax_park.legend(handles=legend_elements, loc='upper right',
                               framealpha=0.95, fontsize=10,
                               facecolor=colors['bg_panel'],
                               edgecolor=colors['border'],
                               labelcolor=colors['text'])
        legend.get_frame().set_linewidth(2)
        
        # ==================== STATISTICS PANEL ====================
        ax_stats.clear()
        ax_stats.axis('off')
        ax_stats.set_xlim(0, 1)
        ax_stats.set_ylim(0, 1)
        ax_stats.set_facecolor(colors['bg_dark'])
        
        # Modern panel background
        panel_bg = FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                                  boxstyle="round,pad=0.02",
                                  facecolor=colors['bg_panel'],
                                  edgecolor=colors['border'],
                                  linewidth=2, alpha=0.9,
                                  transform=ax_stats.transAxes)
        ax_stats.add_patch(panel_bg)
        
        # Title with icon
        ax_stats.text(0.5, 0.94, 'STATISTICS',
                     ha='center', va='top', fontsize=11,
                     fontweight='bold', color=colors['accent'],
                     bbox=dict(boxstyle='round,pad=0.4', 
                              facecolor=colors['bg_dark'], 
                              alpha=0.8,
                              edgecolor=colors['accent'],
                              linewidth=1.5))
        
        # Progress bar
        progress = stats['timestep'] / num_timesteps
        bar_width = 0.7
        bar_x = 0.15
        bar_y = 0.86
        
        # Background bar
        ax_stats.add_patch(patches.Rectangle((bar_x, bar_y), bar_width, 0.03,
                                             facecolor=colors['bg_dark'],
                                             edgecolor=colors['border'],
                                             linewidth=1.5,
                                             transform=ax_stats.transAxes))
        # Progress bar with gradient effect
        ax_stats.add_patch(patches.Rectangle((bar_x, bar_y), bar_width * progress, 0.03,
                                             facecolor=colors['accent'],
                                             edgecolor='none',
                                             alpha=0.8,
                                             transform=ax_stats.transAxes))
        
        # Progress text
        ax_stats.text(0.5, bar_y + 0.015, f"{progress*100:.0f}%",
                     ha='center', va='center', fontsize=9,
                     fontweight='bold', color=colors['text'],
                     transform=ax_stats.transAxes)
        
        # Stats with modern layout
        stats_lines = [
            ('TIMESTEP', f"{stats['timestep']} / {num_timesteps}"),
            ('', ''),
            ('SPAWNED', f"{stats['total_spawned']}"),
            ('ACTIVE', f"{stats['total_patrons']}"),
            ('', ''),
            ('ROAMING', f"{stats['roaming']}"),
            ('QUEUED', f"{stats['queued']}"),
            ('RIDING', f"{stats['riding']}"),
            ('LEAVING', f"{stats['leaving']}")
        ]
        
        y_offset = 0.73
        for label, value in stats_lines:
            if label == '':  # Spacer
                y_offset -= 0.04
                continue
            
            ax_stats.text(0.12, y_offset, label,
                         ha='left', va='top', fontsize=9.5,
                         color=colors['text'], alpha=0.7,
                         transform=ax_stats.transAxes)
            ax_stats.text(0.88, y_offset, str(value),
                         ha='right', va='top', fontsize=10,
                         fontweight='bold', color=colors['accent'],
                         transform=ax_stats.transAxes)
            y_offset -= 0.095
        
        # ==================== RIDES PANEL ====================
        ax_rides.clear()
        ax_rides.axis('off')
        ax_rides.set_xlim(0, 1)
        ax_rides.set_ylim(0, 1)
        ax_rides.set_facecolor(colors['bg_dark'])
        
        # Panel background
        panel_bg = FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                                  boxstyle="round,pad=0.02",
                                  facecolor=colors['bg_panel'],
                                  edgecolor=colors['border'],
                                  linewidth=2, alpha=0.9,
                                  transform=ax_rides.transAxes)
        ax_rides.add_patch(panel_bg)
        
        ax_rides.text(0.5, 0.93, 'RIDES',
                     ha='center', va='top', fontsize=11,
                     fontweight='bold', color=colors['accent'],
                     bbox=dict(boxstyle='round,pad=0.4', 
                              facecolor=colors['bg_dark'], 
                              alpha=0.8,
                              edgecolor=colors['accent'],
                              linewidth=1.5))

        y_pos = 0.82
        for ride_stat in stats['rides']:
            state_emoji = {
                'idle': 'IDLE',
                'boarding': 'WAIT',
                'running': 'RUN'
            }.get(ride_stat['state'], '*')
            
            state_color = colors.get(ride_stat['state'], colors['text'])

            # Card background per-ride
            card_x = 0.03
            card_w = 0.94
            card_h = 0.23
            card_y = y_pos - (card_h - 0.02)
            ax_rides.add_patch(FancyBboxPatch((card_x, card_y), card_w, card_h,
                                              boxstyle="round,pad=0.02",
                                              facecolor=colors['bg_dark'],
                                              edgecolor=colors['border'],
                                              linewidth=1.2, alpha=0.6,
                                              transform=ax_rides.transAxes))

            # State badge + ride name on first line
            ride_name = ride_stat['type'].replace('PirateShip', 'PirateSh').replace('FerrisWheel', 'FerrisWh').replace('SpiderRide', 'Spider')
            # State badge
            ax_rides.text(0.06, y_pos - 0.005, state_emoji,
                         ha='left', va='top', fontsize=8,
                         fontweight='bold', color=colors['accent'],
                         bbox=dict(boxstyle='round,pad=0.25',
                                   facecolor=state_color, alpha=0.25,
                                   edgecolor=state_color, linewidth=1.0),
                         transform=ax_rides.transAxes)
            # Ride name next to badge
            ax_rides.text(0.16, y_pos - 0.005, ride_name,
                         ha='left', va='top', fontsize=9,
                         fontweight='bold', color=colors['text'],
                         transform=ax_rides.transAxes)
            
            # Queue info on second line (below)
            queue_text = f"Queue: {ride_stat['queue_length']} | Riders: {ride_stat['riders']}/{ride_stat['capacity']}"
            ax_rides.text(0.06, y_pos - 0.08,
                         queue_text,
                         ha='left', va='top', fontsize=8,
                         color=colors['text'], alpha=0.95,
                         transform=ax_rides.transAxes)
            
            # Status indicator bar (thinner, better positioned)
            capacity_ratio = ride_stat['riders'] / max(ride_stat['capacity'], 1)
            bar_width = 0.86
            # Track
            ax_rides.add_patch(patches.Rectangle((0.06, y_pos - 0.15), 
                                                 bar_width, 0.018,
                                                 facecolor=colors['bg_panel'],
                                                 edgecolor=colors['border'],
                                                 linewidth=1.0,
                                                 alpha=0.6,
                                                 transform=ax_rides.transAxes))
            # Fill
            ax_rides.add_patch(patches.Rectangle((0.06, y_pos - 0.15), 
                                                 bar_width * capacity_ratio, 0.015,
                                                 facecolor=state_color,
                                                 alpha=0.7,
                                                 transform=ax_rides.transAxes))
            
            y_pos -= 0.34
        
        # ==================== PATRON DISTRIBUTION ====================
        ax_patrons.clear()
        ax_patrons.axis('off')
        ax_patrons.set_xlim(0, 1)
        ax_patrons.set_ylim(0, 1)
        ax_patrons.set_facecolor(colors['bg_dark'])
        
        # Panel background
        panel_bg = FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                                  boxstyle="round,pad=0.02",
                                  facecolor=colors['bg_panel'],
                                  edgecolor=colors['border'],
                                  linewidth=2, alpha=0.9,
                                  transform=ax_patrons.transAxes)
        ax_patrons.add_patch(panel_bg)
        
        ax_patrons.text(0.5, 0.95, 'PATRONS', 
                       ha='center', va='top', fontsize=11,
                       fontweight='bold', color=colors['accent'],
                       transform=ax_patrons.transAxes,
                       bbox=dict(boxstyle='round,pad=0.4', 
                                facecolor=colors['bg_dark'], 
                                alpha=0.8,
                                edgecolor=colors['accent'],
                                linewidth=1.5))
        
        # Modern donut chart
        patron_counts = [stats['roaming'], stats['queued'], 
                        stats['riding'], stats['leaving']]
        patron_labels = ['Roaming', 'Queued', 'Riding', 'Leaving']
        patron_colors = [colors['roaming'], colors['queued'],
                        colors['riding'], colors['leaving']]
        
        # Filter out zero values
        data_filtered = [(c, l, col) for c, l, col in 
                        zip(patron_counts, patron_labels, patron_colors) if c > 0]
        
        if data_filtered and stats['total_patrons'] > 0:
            counts, labels, cols = zip(*data_filtered)
            
            # Create donut chart (positioned higher, away from legend)
            # Use subplot axes for better control
            chart_center_y = 0.60  # Move chart up
            
            wedges, texts, autotexts = ax_patrons.pie(
                list(counts), labels=None, colors=list(cols),
                autopct='%1.0f%%', startangle=90,
                center=(0.5, chart_center_y),
                wedgeprops=dict(width=0.3, edgecolor=colors['bg_dark'], 
                               linewidth=2),
                textprops={'fontsize': 10, 'weight': 'bold', 
                          'color': colors['text']},
                pctdistance=0.75,
                radius=0.42
            )
            
            # Style percentage labels
            for autotext in autotexts:
                autotext.set_color(colors['text'])
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            # Add center text
            ax_patrons.text(0.5, chart_center_y, f"{stats['total_patrons']}\nACTIVE",
                           ha='center', va='center',
                           fontsize=13, fontweight='bold',
                           color=colors['accent'],
                           transform=ax_patrons.transAxes)
            
            # Add clear legend below chart with better spacing
            legend_start_y = 0.18
            legend_items = list(zip(labels, counts, cols))
            
            # Arrange in single column for clarity
            for idx, (label, count, col) in enumerate(legend_items):
                y_pos = legend_start_y - (idx * 0.08)
                
                # Color indicator (circle)
                ax_patrons.plot(0.15, y_pos, 'o',
                              color=col, markersize=9,
                              markeredgecolor=colors['bg_dark'],
                              markeredgewidth=1,
                              transform=ax_patrons.transAxes)
                
                # Label with count
                ax_patrons.text(0.23, y_pos, f"{label}:",
                              ha='left', va='center', fontsize=8,
                              color=colors['text'], fontweight='bold',
                              transform=ax_patrons.transAxes)
                
                # Count value (right aligned)
                ax_patrons.text(0.85, y_pos, str(count),
                              ha='right', va='center', fontsize=8,
                              color=col, fontweight='bold',
                              transform=ax_patrons.transAxes)
        else:
            ax_patrons.text(0.5, 0.5, 'NO ACTIVE\nPATRONS',
                           ha='center', va='center',
                           fontsize=12, color=colors['text'],
                           alpha=0.5,
                           transform=ax_patrons.transAxes)
        
        # Update display
        plt.pause(0.05)
        
        # Print progress every 10 timesteps with modern format
        if (t + 1) % 10 == 0:
            bar_length = 30
            filled = int((t + 1) / num_timesteps * bar_length)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"Step [{bar}] {t+1}/{num_timesteps} | "
                  f"Patrons: {len(park.patrons)} | "
                  f"Riding: {stats['riding']} | "
                  f"Queued: {stats['queued']}")
    
    plt.ioff()
    
    # Handle window close gracefully
    try:
        plt.show()
    except KeyboardInterrupt:
        print("\n\n[Window closed by user]")
    
    print("\n✅ === SIMULATION COMPLETE ===")
    print(f" Final Statistics:")
    print(f"   ⏱️  Total timesteps: {park.timestep}")
    print(f"    Patrons spawned: {park.patrons_spawned}")
    print(f"    Patrons remaining: {len(park.patrons)}")
    print(f"    Rides operated: {len(park.rides)}")




# ============================================================================
# MAIN
# ============================================================================

def main():
    """
    Main entry point. Parse command line arguments and run simulation.
    """
    parser = argparse.ArgumentParser(
        description='Adventure World Theme Park Simulation'
    )
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Run in interactive mode')
    parser.add_argument('-f', '--map', type=str,
                        help='Map file (CSV) for batch mode')
    parser.add_argument('-p', '--params', type=str,
                        help='Parameters file (CSV) for batch mode')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.map and args.params:
        batch_mode(args.map, args.params)
    else:
        print("Error: Must specify either -i for interactive mode or "
              "-f and -p for batch mode.")
        print("Usage:")
        print("  Interactive: python adventureworld.py -i")
        print("  Batch:       python adventureworld.py -f map.csv -p params.csv")


if __name__ == "__main__":
    main()
