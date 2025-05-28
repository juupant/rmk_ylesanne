from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import random

def get_bus_delay():
    # 30% chance of being on time
    if random.random() < 0.3:
        return 0
    
    # 70% chance of being off schedule
    if random.random() < 0.9:  # 90% of off-schedule times are late
        # late probabilities
        r = random.random()
        if r < 0.3: return 1  # 30% chance of 1 min late
        elif r < 0.6: return 2  # 30% chance of 2 min late
        elif r < 0.8: return 3  # 20% chance of 3 min late
        elif r < 0.9: return 4  # 10% chance of 4 min late
        elif r < 0.95: return 5  # 5% chance of 5 min late
        elif r < 0.98: return 6  # 3% chance of 6 min late
        elif r < 0.99: return 8  # 2% chance of 8 min late
        elif r < 0.995: return 10  # 1% chance of 10 min late
        else: return 15  # 1% chance of 15 min late
    else:  # 10% of off-schedule times are early
        # early probabilities
        if random.random() < 0.9:  # 90% chance of 1 min early
            return -1
        else:  # 10% chance of 2 min early
            return -2

# --- input manual bus schedule for simplicity purposes---
bus_schedule = """
1. 8:38, 8:40, 8:41, 8:43, 8:43, 8:46, 8:48, 8:49, 8:51
2. 8:48, 8:50, 8:51, 8:53, 8:53, 8:56, 8:58, 8:59, 9:01
3. 8:56, 8:58, 8:59, 9:01, 9:01, 9:04, 9:06, 9:07, 9:09
4. 9:06, 9:08, 9:09, 9:11, 9:11, 9:14, 9:16, 9:17, 9:19
5. 9:16, 9:18, 9:19, 9:21, 9:21, 9:24, 9:26, 9:27, 9:29
"""

# --- parse schedule into list of dicts ---
trip_times = []
for line in bus_schedule.strip().split("\n"):
    parts = line.split(".")[1].strip().split(",")
    stops = [datetime.strptime(time.strip(), "%H:%M") for time in parts]
    trip_times.append({
        "stops": stops,
        "first_stop": stops[0],
        "last_stop": stops[-1]
    })

# --- set constants ---
meeting_time = datetime.strptime("09:05", "%H:%M")
walk_to_bus = timedelta(seconds=300)   # 5 minutes
walk_from_bus = timedelta(seconds=240) # 4 minutes
SIMULATION_RUNS = 1000  # number of simulations per departure time

# --- simulate lateness ---
departure_range = [datetime.strptime("08:00", "%H:%M") + timedelta(minutes=i) for i in range(61)]
late_probabilities = []

for home_departure in departure_range:
    late_count = 0
    
    for _ in range(SIMULATION_RUNS):
        zoo_arrival = home_departure + walk_to_bus
        meeting_arrival = None

        for trip in trip_times:
            # apply delay to first stop time
            adjusted_first_stop = trip["first_stop"] + timedelta(minutes=get_bus_delay())
            
            if adjusted_first_stop >= zoo_arrival:
                # apply delay to last stop time
                adjusted_last_stop = trip["last_stop"] + timedelta(minutes=get_bus_delay())
                meeting_arrival = adjusted_last_stop + walk_from_bus
                break

        if meeting_arrival is None or meeting_arrival > meeting_time:
            late_count += 1
    
    late_probabilities.append(late_count / SIMULATION_RUNS)

# --- plot ---
plt.figure(figsize=(15, 8))  # changed figure size for readability
plt.plot([t.strftime("%H:%M") for t in departure_range], late_probabilities, marker='o', linestyle='-', color='red', markersize=8)

# set x-axis ticks to show every 5 minutes
plt.xticks([t.strftime("%H:%M") for t in departure_range[::5]], rotation=45, ha='right')

plt.title("Probability of Being Late vs. Home Departure Time", pad=20, fontsize=12)
plt.xlabel("Time Rita Leaves Home", fontsize=10)
plt.ylabel("Probability of Being Late", fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.ylim(-0.05, 1.05)

# add annotations for key points, but only for every 5th point for readability purposes
for i, (time, prob) in enumerate(zip(departure_range, late_probabilities)):
    if i % 5 == 0:  # only annotate every 5th point
        plt.annotate(f"{prob:.2f}", 
                    (time.strftime("%H:%M"), prob),
                    textcoords="offset points",
                    xytext=(0,10),
                    ha='center',
                    fontsize=9)

plt.tight_layout()
plt.show()



