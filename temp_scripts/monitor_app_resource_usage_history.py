import csv
import datetime
import time

import matplotlib.pyplot as plt
import psutil
from logger import get_logger

logger = get_logger()


def find_raycast_process():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'Raycast':
            logger.info(f"Found Raycast process with PID {proc.pid}")
            return proc
    return None


def monitor_app(duration_minutes=5, app_name=None, frequency_hz=10, save_to_csv=False, save_to_chart=True):
    raycast = find_raycast_process()
    if not raycast:
        logger.warning(f"Cannot find Process:{app_name}")
        return

    data = []
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)

    while time.time() < end_time:
        try:
            cpu_percent = raycast.cpu_percent()
            # get memory usage absolute value
            memory_info = raycast.memory_info()
            memory_usage = memory_info.rss / \
                (1024 * 1024) / 1024  # Convert bytes to GB
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data.append([timestamp, cpu_percent, memory_usage])
            time.sleep(1/30)  # Sample every second
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            print("Lost access to Raycast process")
            break

    # Save to CSV
    if save_to_csv:
        filename = f'app_resource_history_{app_name}_{datetime.datetime.now().strftime("%d_%H%M")}.csv'
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'CPU %', 'Memory'])
            writer.writerows(data)
        logger.info(f"Data saved to {filename}")

    # Plot the data
    if save_to_chart:
        timestamps = [row[0] for row in data]
        cpu_values = [row[1] for row in data]
        mem_values = [row[2] for row in data]

        # Increased height from 6 to 8
        fig, ax1 = plt.subplots(figsize=(24, 8))

        # Calculate number of x-ticks to show
        n_timestamps = len(timestamps)
        step = max(n_timestamps // 10, 1)

        ax1.set_xlabel('Time')
        ax1.set_ylabel('CPU %', color='tab:blue')
        ax1.plot(timestamps, cpu_values, label='CPU %', color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        # Set x-ticks to show fewer labels
        ax1.set_xticks(timestamps[::step])
        ax1.set_xticklabels(timestamps[::step], rotation=45, ha='right')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Memory (GB)', color='tab:red')
        ax2.plot(timestamps, mem_values, label='Memory (GB)', color='tab:red')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        # Add legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

        # Set title before adjusting layout
        plt.title(f'Raycast Resource Usage, Frequency: {frequency_hz} Hz')

        # Adjust layout with specific margins
        plt.subplots_adjust(
            bottom=0.2,    # More space for x-labels
            top=0.9,       # More space for title
            right=0.9,     # More space for right y-axis
            left=0.1       # Space for left y-axis
        )

        plt.savefig(f'{app_name}_metrics_chart_{datetime.datetime.now().strftime("%H%M")}.png',
                    bbox_inches='tight', dpi=300)
        logger.info("Chart saved to raycast_metrics_chart.png")


if __name__ == "__main__":
    # Monitor for 5 minutes
    monitor_app(duration_minutes=10, app_name='Raycast',
                save_to_csv=True, save_to_chart=True)
