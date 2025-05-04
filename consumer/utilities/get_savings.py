import json
import uuid
import random
from datetime import datetime, timedelta
import os

# Define the start and end dates for the period (Feb 1, 2024 to July 31, 2024)
start_date = datetime(2024, 2, 1)
end_date = datetime(2024, 7, 31)
delta = end_date - start_date

# Read vendor names from the partner_vendors.json file
partner_vendors_path = "/Users/1arijits/PROFESSIONAL/Revpoints-Plus/data/partner_vendors.json"
with open(partner_vendors_path, "r") as f:
    partner_vendors = json.load(f)
all_vendors = list({vendor["vendor_name"] for vendor in partner_vendors})
# Ensure we have at least 50 entries, if not, repeat as needed, then slice
if len(all_vendors) < 50:
    all_vendors = (all_vendors * ((50 // len(all_vendors)) + 1))[:50]
else:
    all_vendors = all_vendors[:50]

# Use these 50 vendors in transactions
vendors = all_vendors

def random_date():
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86400)
    return start_date + timedelta(days=random_days, seconds=random_seconds)

def generate_promotion_text(pts, saved, perc, price):
    """
    Generates a promotion description based on the computed values.
    """
    if pts < 500:
        return f"Small savings: Spend {pts} points to save €{saved} ({perc}% off) on a product originally priced at €{price}."
    elif pts < 2000:
        return f"Great deal: Redeem {pts} points and enjoy a discount of €{saved} ({perc}% off) on your purchase of €{price}."
    else:
        return f"Premium offer: {pts} points unlock a massive saving of €{saved}, which is roughly {perc}% off an item priced at €{price}."

transactions = []

for _ in range(300):
    # Decide between a fixed euro discount or a percentage discount based offer
    if random.choice([True, False]):
        # Euro discount approach with lower points spent and discount amount
        pts_spent = random.randint(10, 200)
        money_saved = round(random.uniform(2, 10), 2)
        actual_price = round(random.uniform(money_saved + 3, money_saved + 20), 2)
        perc_saved = round((money_saved / actual_price) * 100)
    else:
        # Percentage discount approach with lower points spent and milder discounts
        pts_spent = random.randint(10, 200)
        perc_saved = random.choice([2, 5, 7, 10])
        actual_price = round(random.uniform(20, 80), 2)
        money_saved = round(actual_price * (perc_saved / 100), 2)
    
    # Generate a promotion description using the computed values
    promotion_description_used = generate_promotion_text(pts_spent, money_saved, perc_saved, actual_price)
    
    transaction = {
        "pointtransactionid": str(uuid.uuid4()),
        "timestamp": random_date().isoformat(),
        "vendor_name": random.choice(vendors),
        "points_spent": pts_spent,
        "money_saved": money_saved,
        "percentage_saved": perc_saved,
        "actual_price": actual_price,
        "promotion_description_used": promotion_description_used
    }
    transactions.append(transaction)

# Save the transactions to a JSON file
data_folder = "/Users/1arijits/PROFESSIONAL/Revpoints-Plus/data"
output_file = os.path.join(data_folder, "revpoint_transactions.json")
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
with open(output_file, "w") as f:
    json.dump(transactions, f, indent=4)

print(f"Generated 300 point transactions in {output_file}")