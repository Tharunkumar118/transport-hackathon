# filename: generate_data.py
import pandas as pd
import numpy as np
import random

# CONFIGURATION
# We will simulate traffic for 'Today'
hours = range(7, 20) # 7 AM to 8 PM

data = []

print("Generating Sample Data Sheet...")

for hour in hours:
    # ---------------------------------------------------------
    # SCENARIO 1: 9:00 AM - The "Solo Driver" Problem
    # High volume of cars with only 1 passenger
    # ---------------------------------------------------------
    if hour == 9:
        for _ in range(45): # 45 Solo cars
            data.append([f"{hour}:00", "Car", 1, "Main Gate"])
        for _ in range(5):  # 5 Carpools
            data.append([f"{hour}:15", "Car", 3, "Main Gate"])
        # 2 Full Buses (Good)
        data.append([f"{hour}:30", "Bus", 45, "Main Gate"])
        data.append([f"{hour}:45", "Bus", 50, "Main Gate"])

    # ---------------------------------------------------------
    # SCENARIO 2: 11:00 AM - The "Ghost Bus" Problem
    # A big bus running almost empty
    # ---------------------------------------------------------
    elif hour == 11:
        # THE PROBLEM: 1 Bus with only 2 people
        data.append([f"{hour}:10", "Bus", 2, "Main Gate"]) 
        # Normal light traffic
        for _ in range(8):
            data.append([f"{hour}:20", "Car", 1, "Main Gate"])

    # ---------------------------------------------------------
    # NORMAL TRAFFIC (Randomized)
    # ---------------------------------------------------------
    else:
        # Random Cars (1-3 passengers)
        for _ in range(random.randint(5, 15)):
            data.append([f"{hour}:{random.randint(10,59)}", "Car", random.choice([1, 2]), "Main Gate"])
        
        # Random Bikes
        for _ in range(random.randint(10, 25)):
            data.append([f"{hour}:{random.randint(10,59)}", "Bike", 1, "Main Gate"])
            
        # Occasional Bus (Peak hours)
        if hour in [8, 17]:
            data.append([f"{hour}:00", "Bus", random.randint(30, 50), "Main Gate"])

# Save to CSV
df = pd.DataFrame(data, columns=["Time", "Vehicle_Type", "Passenger_Count", "Gate_Location"])
df.to_csv("campus_traffic_log.csv", index=False)

print(f"✅ Success! Generated 'campus_traffic_log.csv' with {len(df)} records.")
