import json
import os
from fpdf import FPDF

HISTORY_FILE = "trip_history.json"


# Save trip history
def save_trip(destination, duration, budget, style, itinerary):
    trip_data = {
        "destination": destination,
        "duration": duration,
        "budget": budget,
        "style": style,
        "itinerary": itinerary
    }

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)

    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)

    data.append(trip_data)

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Load trip history
def load_trips():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


# Generate PDF
def generate_pdf(content, filename="itinerary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in content.split("\n"):
        pdf.multi_cell(0, 8, line)

    pdf.output(filename)