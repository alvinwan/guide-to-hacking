import numpy as np
import matplotlib.pyplot as plt

# Constants
n = 2048  # Matrix size
b = 128   # Batch size

# Create s values from 0 to 10
s_values = np.linspace(0, 10, 11)  # 11 points from 0 to 10

# Calculate arithmetic intensity for each s
arithmetic_intensity = (2 * n * s_values * b) / (n * s_values + n + s_values * b)

# Create plot
plt.figure(figsize=(12, 4), facecolor='white')  # Wide and short plot
plt.plot(s_values, arithmetic_intensity, 'o-', color='white', markersize=8, markeredgecolor='white')

# Add labels above each point
for i in range(len(s_values)):
    plt.text(s_values[i], arithmetic_intensity[i] + 4.5,  # Increased spacing to +1.5
             f'{arithmetic_intensity[i]:.0f}',
             ha='center',
             va='bottom',
             fontsize=10,
             color='white')

# Set plot properties
plt.title('Batched Matrix Multiplication, n=2048, b=128', color='white')
plt.xlabel('Batch Size (s)', color='white')
plt.ylabel('Arithmetic Intensity (FLOPS/Byte)', color='white')
plt.grid(True, alpha=0.3, color='white')

# Add some vertical padding to the plot
plt.margins(y=0.1)

# Add dotted line at y=153
plt.axhline(y=153, color='white', linestyle='--', alpha=0.7)

# Add compute and memory bound labels
plt.text(9.9, 157, 'compute bound', color='white', fontsize=8, ha='right', va='bottom')
plt.text(9.9, 148, 'memory bound', color='white', fontsize=8, ha='right', va='top')

# Make tick labels white
plt.xticks(color='white')
plt.yticks(color='white')

# Make spines (plot borders) white
for spine in plt.gca().spines.values():
    spine.set_color('white')

# NOTE: without this, fonts won't show up in browser
import matplotlib as mpl
mpl.rcParams['svg.fonttype'] = 'path'  # convert all text to paths
mpl.rcParams['text.usetex'] = False

# Save with transparent background
plt.savefig('arithmetic_intensity.svg', format='svg', dpi=300, transparent=True, bbox_inches='tight')
plt.close()  # Close the plot to free up memory