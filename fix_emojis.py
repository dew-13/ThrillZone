#!/usr/bin/env python3
"""
Script to remove all emoji/unicode characters from adventureworld.py 
and replace with proper text labels with spacing
"""

import re

# Read the file
with open('adventureworld.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all emoji characters with text equivalents
replacements = {
    # Panel titles
    "'🎡 ADVENTURE WORLD'": "'ADVENTURE WORLD'",
    "'📈 STATISTICS'": "'STATISTICS'",
    "'🎢 RIDES'": "'RIDES'",
    "'👨‍👩‍👧‍👦 PATRONS'": "'PATRONS'",
    
    # Entrance labels
    "'⭐ ENTRANCE'": "'ENTRANCE'",
    "'⚡ ENTRANCE'": "'ENTRANCE'",
    
    # Legend items
    "'🟢 Roaming'": "'Roaming'",
    "'🔵 Queued'": "'Queued'",
    "'🔴 Riding'": "'Riding'",
    
    # State emojis in stats
    "'⏱️  TIMESTEP'": "'TIMESTEP'",
    "'👥 SPAWNED'": "'SPAWNED'",
    "'🎯 ACTIVE'": "'ACTIVE'",
    "'🚶 ROAMING'": "'ROAMING'",
    "'⏳ QUEUED'": "'QUEUED'",
    "'🎢 RIDING'": "'RIDING'",
    "'👋 LEAVING'": "'LEAVING'",
    
    # Console output emojis  
    "'💤'": "'IDLE'",
    "'⏳'": "'WAIT'",
    "'⚡'": "'RUN'",
    "'●'": "'*'",
    
    # Print statements
    "print(f'📊 Final Statistics:')": "print(f'=== Final Statistics ===')",
    "f'⏱️  [{bar}] {t+1}/{num_timesteps}'": "f'Progress: [{bar}] {t+1}/{num_timesteps}'",
    "f' | 👥 {stats['total_patrons']}'": "f' | Patrons: {stats['total_patrons']}'",
    "f' | 🎢 {stats['riding']}'": "f' | Riding: {stats['riding']}'",
    "f' | ⏳ {stats['queued']}'": "f' | Queued: {stats['queued']}'",
}

# Apply replacements
for old, new in replacements.items():
    content = content.replace(old, new)

# Remove any remaining emoji patterns (fallback)
# This removes characters outside the Basic Multilingual Plane
content = re.sub(r'[^\x00-\x7F\u0080-\uFFFF]+', '', content)

# Adjust spacing for title - increase top margin
content = content.replace(
    "ax_park.text(park.width / 2, park.height + 8,",
    "ax_park.text(park.width / 2, park.height + 12,"
)

# Adjust subtitle position for better spacing
content = content.replace(
    "ax_park.text(park.width / 2, park.height + 3,",
    "ax_park.text(park.width / 2, park.height + 4,"
)

# Increase fontsize for main title
content = content.replace(
    "'ADVENTURE WORLD', \n                    fontsize=24,",
    "'ADVENTURE WORLD', \n                    fontsize=28,"
)

# Add background box to main title for better visibility
if "'ADVENTURE WORLD', \n                    fontsize=28, fontweight='bold', \n                    ha='center', color=colors['accent'])" in content:
    content = content.replace(
        "'ADVENTURE WORLD', \n                    fontsize=28, fontweight='bold', \n                    ha='center', color=colors['accent'])",
        "'ADVENTURE WORLD', \n                    fontsize=28, fontweight='bold', \n                    ha='center', color=colors['accent'],\n                    bbox=dict(boxstyle='round,pad=1.0', \n                             facecolor=colors['bg_panel'], \n                             alpha=0.8,\n                             edgecolor=colors['accent'],\n                             linewidth=3))"
    )

# Increase panel title font sizes
content = content.replace(
    "'STATISTICS',\n                     ha='center', va='top', fontsize=13,",
    "'STATISTICS',\n                     ha='center', va='top', fontsize=14,"
)

content = content.replace(
    "'RIDES',\n                     ha='center', va='top', fontsize=12,",
    "'RIDES',\n                     ha='center', va='top', fontsize=14,"
)

content = content.replace(
    "'PATRONS', \n                       ha='center', va='top', fontsize=12,",
    "'PATRONS', \n                       ha='center', va='top', fontsize=14,"
)

# Write the file back
with open('adventureworld.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Successfully removed all emoji characters")
print("✓ Adjusted spacing and margins")
print("✓ Increased font sizes for better visibility")
print("\nChanges made:")
print("  - Removed all emoji icons")
print("  - Added text labels instead")
print("  - Increased title margin (height + 12)")
print("  - Adjusted subtitle spacing")
print("  - Increased main title font to 28pt")
print("  - Added background box to main title")
print("  - Increased panel title fonts to 14pt")
