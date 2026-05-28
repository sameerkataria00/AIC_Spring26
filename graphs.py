# Python script that our graph/data will be stored

# Imports section
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv('data/uber_trips_dataset_50k.csv')  # Uber data

# Extract hour and day of week from pickup_time
df["pickup_time"] = pd.to_datetime(df["pickup_time"])
df["hour"] = df["pickup_time"].dt.hour
df["day_of_week"] = df["pickup_time"].dt.day_name()

# print out some cool data points 
print("Highest fare:", df["fare_amount"].max()) #highest fare
print("Lowest fare:", df["fare_amount"].min()) #lowest fare
print("Average fare:", df["fare_amount"].mean().round(2)) #average fare

os.makedirs("outputs", exist_ok=True)

# ── Graph 1: Average fare by hour (line chart) ────────────────────────────────
hourly_avg = df.groupby("hour")["fare_amount"].mean().reset_index()

plt.figure(figsize=(10, 5))
plt.plot(hourly_avg["hour"], hourly_avg["fare_amount"], marker="o", linewidth=2.5, color="#1DB954")
plt.title("Average Uber Fare by Hour of Day")
plt.xlabel("Hour of Day (0–23)")
plt.ylabel("Average Fare ($)")
plt.xticks(range(0, 24))
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/avg_price_by_hour.png", dpi=150)
plt.close()

# ── Graph 2: Average fare by day of week (bar chart) ─────────────────────────
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
daily_avg = df.groupby("day_of_week")["fare_amount"].mean().reindex(day_order).reset_index()

plt.figure(figsize=(9, 5))
sns.barplot(data=daily_avg, x="day_of_week", y="fare_amount", palette="Blues_d")
plt.title("Average Uber Fare by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Average Fare ($)")
plt.ylim(15.5, 16.5)  # zooms in so the small differences between days are actually visible
plt.tight_layout()
plt.savefig("outputs/avg_price_by_day.png", dpi=150)
plt.close()

# ── Graph 3: Fare distribution histogram ─────────────────────────────────────
plt.figure(figsize=(9, 5))
plt.hist(df["fare_amount"].dropna(), bins=40, color="#E8704A", edgecolor="white")
plt.title("Distribution of Uber Fares")
plt.xlabel("Fare ($)")
plt.ylabel("Count")
plt.xlim(0, df["fare_amount"].quantile(0.99))  # cuts off the stretched empty space on the right
plt.tight_layout()
plt.savefig("outputs/price_distribution.png", dpi=150)
plt.close()

print("Done! All 3 graphs saved to the outputs folder.")