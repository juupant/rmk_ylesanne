from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# --- input manual bus schedule ---
bus_schedule = """
1. 8:38 - 8:51
2. 8:48 - 9:01
3. 8:56 - 9:09
4. 9:06 - 9:19
5. 9:16 - 9:29
"""

# --- parse schedule into list of dicts ---
trip_times = []
for line in bus_schedule.strip().split("\n"):
    parts = line.split(".")[1].strip().split("-")
    dep_time = datetime.strptime(parts[0].strip(), "%H:%M")
    arr_time = datetime.strptime(parts[1].strip(), "%H:%M")
    trip_times.append({"dep": dep_time, "arr": arr_time})

# --- set constants ---
meeting_time = datetime.strptime("09:05", "%H:%M")
walk_to_bus = timedelta(seconds=300)   # 5 minutes
walk_from_bus = timedelta(seconds=240) # 4 minutes

# --- simulate lateness ---
departure_range = [datetime.strptime("08:00", "%H:%M") + timedelta(minutes=i) for i in range(61)]
late_probabilities = []

for home_departure in departure_range:
    zoo_arrival = home_departure + walk_to_bus
    meeting_arrival = None

    for trip in trip_times:
        if trip["dep"] >= zoo_arrival:
            meeting_arrival = trip["arr"] + walk_from_bus
            break

    if meeting_arrival is None or meeting_arrival > meeting_time:
        late_probabilities.append(1)
    else:
        late_probabilities.append(0)
# --- STEP 5: Plot ---
plt.figure(figsize=(12, 6))
plt.plot([t.strftime("%H:%M") for t in departure_range], late_probabilities, marker='o', linestyle='-', color='red')
plt.xticks(rotation=45, ha='right')
plt.title("Probability of Being Late vs. Home Departure Time", pad=20)
plt.xlabel("Time Rita Leaves Home")
plt.ylabel("Probability of Being Late")
plt.grid(True, linestyle='--', alpha=0.7)
plt.ylim(-0.05, 1.05)

# Add annotations for key points
for i, (time, prob) in enumerate(zip(departure_range, late_probabilities)):
    plt.annotate(f"{prob:.0f}", 
                (time.strftime("%H:%M"), prob),
                textcoords="offset points",
                xytext=(0,10),
                ha='center')

plt.tight_layout()
plt.show()



