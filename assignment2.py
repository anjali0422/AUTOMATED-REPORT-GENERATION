import requests
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime

# Configuration
API_KEY = "ca424025f2ab8d8c87046bda67b47709"
CITY = "Mumbai"
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

# Get weather data
response = requests.get(URL)
data = response.json()

# Extract necessary data
dates = []
temps = []
descriptions = []

for entry in data['list'][:10]:  # Next 10 time blocks (~30 hours)
    dates.append(entry['dt_txt'])
    temps.append(entry['main']['temp'])
    descriptions.append(entry['weather'][0]['description'])

# Plotting temperature chart
plt.figure(figsize=(10, 5))
plt.plot(dates, temps, marker='o', linestyle='-', color='blue')
plt.title(f"Temperature Forecast for {CITY}")
plt.xlabel("Date/Time")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("forecast_chart.png")
plt.close()

# Generate PDF Report
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, f"Weather Forecast Report: {CITY}", ln=True)

pdf.set_font("Arial", "", 12)
pdf.cell(0, 10, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
pdf.ln(5)

# Add summary table
for dt, temp, desc in zip(dates, temps, descriptions):
    pdf.cell(0, 10, f"{dt} | {temp} °C | {desc.title()}", ln=True)

# Add graph
pdf.image("forecast_chart.png", x=10, y=None, w=180)

# Save PDF
pdf.output("Weather_Report.pdf")

print("✅ Weather_Report.pdf generated successfully!")
