import tkinter as tk
from tkinter import filedialog
import brotli
import os
from PIL import Image
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math  # Import math module for logarithm function

# Global variables for storing data for plotting
compression_ratios = []
compression_times = []
original_entropies = []
compressed_entropies = []

# Function to plot compression ratio vs time and entropy

def plot_graphs(i):
    plt.clf()

    # Plot compression ratio vs time
    plt.subplot(1, 2, 1)
    plt.plot(compression_times, compression_ratios, marker='o', linestyle='-')
    plt.title('Compression Ratio vs Time Taken')
    plt.xlabel('Time (s)')
    plt.ylabel('Compression Ratio')
    plt.grid(True)

    # Calculate and annotate compression ratio / time values
    for time, ratio in zip(compression_times, compression_ratios):
        compression_ratio_time = ratio / time if time != 0 else 0
        plt.annotate(f'{compression_ratio_time:.2f}', (time, ratio), textcoords="offset points", xytext=(0, 5), ha='center')

    # Plot entropy
    plt.subplot(1, 2, 2)
    plt.bar(0.5, original_entropies[-1], width=0.2, label=f'Original Entropy: {original_entropies[-1]:.2f}', align='center')
    plt.bar(0.7, compressed_entropies[-1], width=0.2, label=f'Compressed Entropy: {compressed_entropies[-1]:.2f}', align='center')
    plt.xticks([0.5, 0.7], ['Original', 'Compressed'])
    plt.title('Entropy')
    plt.ylabel('Entropy')
    plt.legend()
    plt.grid(True)

# Rest of the code remains the same...

    # Annotate bars with values
    plt.text(0.5, original_entropies[-1], f'{original_entropies[-1]:.2f}', ha='center', va='bottom')
    plt.text(0.7, compressed_entropies[-1], f'{compressed_entropies[-1]:.2f}', ha='center', va='bottom')

    # Annotate bars with values
    plt.text(0.5, original_entropies[-1], f'{original_entropies[-1]:.2f}', ha='center', va='bottom')
    plt.text(0.7, compressed_entropies[-1], f'{compressed_entropies[-1]:.2f}', ha='center', va='bottom')


    # Annotate bars with values
    plt.text(0.5, original_entropies[-1], f'{original_entropies[-1]:.2f}', ha='center', va='bottom')
    plt.text(0.7, compressed_entropies[-1], f'{compressed_entropies[-1]:.2f}', ha='center', va='bottom')


    # Annotate bars with values
    plt.text(0.5, original_entropies[-1], f'{original_entropies[-1]:.2f}', ha='center', va='bottom')
    plt.text(0.7, compressed_entropies[-1], f'{compressed_entropies[-1]:.2f}', ha='center', va='bottom')


# Rest of the code remains the same...


# Function to convert file size in bytes to human-readable format
def convert_size(size_bytes):
    units = ['bytes', 'KB', 'MB', 'GB', 'TB']
    for unit in units:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} {units[-1]}"

# Function to get image details such as format, size, resolution, and quality
def get_image_details(file_path):
    img = Image.open(file_path)
    format = file_path.split('.')[-1].upper()
    size = os.path.getsize(file_path)
    width, height = img.size
    resolution = f"{width}x{height}"
    image_quality = determine_image_quality(width, height)
    return format, convert_size(size), resolution, image_quality

# Function to estimate image quality based on resolution
def determine_image_quality(width, height):
    if width >= 3840 and height >= 2160:
        return "4K"
    elif width >= 2560 and height >= 1440:
        return "2K"
    elif width >= 1920 and height >= 1080:
        return "1080p"
    elif width >= 1280 and height >= 720:
        return "720p"
    elif width >= 854 and height >= 480:
        return "480p"
    elif width >= 640 and height >= 360:
        return "360p"
    elif width >= 426 and height >= 240:
        return "240p"
    elif width >= 256 and height >= 144:
        return "144p"
    else:
        return "Other"

# Function to compress image using Brotli compression algorithm
def compress_image_to_file(file_path):
    compressed_brotli_path = 'compressed_image.br'
    start_time = time.time()

    with open(file_path, 'rb') as original_file:
        original_data = original_file.read()

    original_entropy = calculate_entropy(original_data)

    compressed_data = brotli.compress(original_data)

    with open(compressed_brotli_path, 'wb') as compressed_file:
        compressed_file.write(compressed_data)

    original_size = len(original_data)
    compressed_brotli_size = len(compressed_data)
    compression_ratio = original_size / compressed_brotli_size
    compression_time = time.time() - start_time

    # Get image details
    image_format, image_size, image_resolution, image_quality = get_image_details(file_path)

    # Calculate entropy for compressed image
    compressed_entropy = calculate_entropy(compressed_data)

    # Append data for plotting
    compression_ratios.append(compression_ratio)
    compression_times.append(compression_time)
    original_entropies.append(original_entropy)
    compressed_entropies.append(compressed_entropy)

    return compressed_brotli_path, original_size, compressed_brotli_size, image_format, image_size, image_resolution, image_quality

# Function to calculate entropy

def calculate_entropy(data):
    hist = [0] * 256  # Initialize a histogram with 256 bins for each possible byte value
    total_bytes = len(data)  # Total number of bytes in the data

    # Count the occurrences of each byte value in the data
    for byte in data:
        hist[byte] += 1

    entropy = 0
    # Calculate entropy using the histogram
    for count in hist:
        if count != 0:
            prob = count / total_bytes  # Probability of occurrence of a byte value
            entropy -= prob * math.log2(prob)  # Calculate entropy contribution for each byte value

    return entropy



# Function to display compression details
def display_compression_details(original_size, compressed_brotli_size, image_format, image_size, image_resolution, image_quality):
    original_size_str = convert_size(original_size)
    compressed_brotli_size_str = convert_size(compressed_brotli_size)

    compression_ratio = original_size / compressed_brotli_size
    bandwidth_saved = (1 - compression_ratio) * 100

    print(f"Compression results (Brotli):\n"
          f"Original file size: {original_size_str}\n"
          f"Compressed file size: {compressed_brotli_size_str}\n"
          f"Compression ratio: {compression_ratio:.2f}\n"
          f"Bandwidth saved: {bandwidth_saved:.2f}%\n"
          f"Image Format: {image_format}\n"
          f"Image Resolution: {image_resolution}\n"
          f"Estimated Image Quality: {image_quality}\n\n")

# Main function
def main():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    if file_path:
        brotli_path, original_size, compressed_brotli_size, image_format, image_size, image_resolution, image_quality = compress_image_to_file(file_path)
        display_compression_details(original_size, compressed_brotli_size, image_format, image_size, image_resolution, image_quality)

        # Create animation for real-time plotting
        ani = FuncAnimation(plt.gcf(), plot_graphs, interval=1000, cache_frame_data=False)


        plt.show()

if __name__ == "__main__":
    main()
