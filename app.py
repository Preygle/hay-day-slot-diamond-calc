import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="Hay Day Calculator", page_icon="🌾", layout="wide")

st.title("🌾 Hay Day Production Building Calculator")
st.markdown("Calculate the number of diamonds and coins required to unlock slots for your production buildings.")

# Sidebar for Totals
st.sidebar.header("Total Required")
total_diamonds_placeholder = st.sidebar.empty()
total_coins_placeholder = st.sidebar.empty()
total_diamonds = 0
total_coins = 0

# Configuration
IMAGE_DIR = "production_building_images"
MULTI_INSTANCE_CONFIG = {
    "Feed Mill": 2,
    "Smelter": 5,
    "Sugar Mill": 2
}
EXCLUDED_BUILDINGS = ["Mine"]

# Coin Configuration
# Format: {BuildingName: {SlotNum: Cost}}
COIN_CONFIG = {
    "Lobster Pool": {
        2: 45000, 3: 52500, 4: 63800, 5: 79800, 6: 102000
    },
    "Duck Salon": {
        2: 51000, 3: 59000, 4: 72000, 5: 90000, 6: 115000
    }
}
MAX_SLOTS_DIAMOND = 9
MAX_SLOTS_COIN = 6

def calculate_diamond_cost(current_slots, start_slots):
    # User Request: "if there are 2 slots, diamonds required in 105"
    # This means calculate cost to unlock from (current_slots + 1) up to MAX_SLOTS_DIAMOND
    if current_slots >= MAX_SLOTS_DIAMOND:
        return 0
    
    cost = 0
    # Range of slots to pay for: next available slot up to max
    for n in range(current_slots + 1, MAX_SLOTS_DIAMOND + 1):
        # Cost of unlocking slot n
        # start_slots = 2. Unlock 3 (1st paid). paid_idx = 3-2-1 = 0. Cost 6.
        paid_idx = n - start_slots - 1
        step_cost = 6 + (paid_idx * 3)
        cost += step_cost
    return cost

def calculate_coin_cost(current_slots, start_slots, cost_table):
    # Inverted Logic: Calculate cost from (current_slots + 1) to MAX_SLOTS_COIN
    if current_slots >= MAX_SLOTS_COIN:
        return 0
    cost = 0
    for n in range(current_slots + 1, MAX_SLOTS_COIN + 1):
        cost += cost_table.get(n, 0)
    return cost

def get_building_name(filename):
    base = os.path.splitext(filename)[0]
    parts = base.split('_', 1)
    if len(parts) > 1 and parts[0].isdigit():
        return parts[1].replace('_', ' ')
    return base.replace('_', ' ')

# Ensure image directory exists
if not os.path.exists(IMAGE_DIR):
    st.error(f"Image directory '{IMAGE_DIR}' not found. Please run the scraper first.")
    st.stop()

files = sorted([f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

st.subheader("Adjust Slots per Building")

# Use single column layout as requested
for idx, filename in enumerate(files):
    building_name = get_building_name(filename)
    
    if building_name in EXCLUDED_BUILDINGS:
        continue

    # Setup Defaults
    instance_count = MULTI_INSTANCE_CONFIG.get(building_name, 1)
    
    if building_name == "Smelter":
        start_slots = 1
    elif building_name == "Feed Mill":
        start_slots = 3
    elif building_name in COIN_CONFIG:
        start_slots = 1
    else:
        start_slots = 2
    
    # Determine type (Coin vs Diamond)
    is_coin = building_name in COIN_CONFIG
    max_slots = MAX_SLOTS_COIN if is_coin else MAX_SLOTS_DIAMOND
    currency_label = "Coins 💰" if is_coin else "Diamonds 💎"
    
    filepath = os.path.join(IMAGE_DIR, filename)

    with st.container(border=True):
        # Two columns inside the card: Image | Sliders
        c1, c2 = st.columns([1, 2])
        
        with c1:
            try:
                img = Image.open(filepath)
                st.image(img, width=150) # Fixed width for uniformity
            except Exception as e:
                st.error(f"Error loading image: {e}")
            st.markdown(f"**{building_name}**")

        with c2:
            current_building_cost = 0
            for i in range(instance_count):
                label = "Slots"
                # Helper label to distinguish behaviors - NOW BOTH ARE SAME LOGIC
                help_text = "Add number of slots unlocked"
                
                if instance_count > 1:
                    label = f"{building_name} {i+1} - {help_text}"
                else:
                    label = f"{label} - {help_text} for {building_name}"
                
                key = f"slider_{filename}_{i}"
                slots = st.slider(
                    label, 
                    min_value=start_slots, 
                    max_value=max_slots, 
                    value=max_slots, 
                    key=key
                )
                
                cost = 0
                if is_coin:
                    cost = calculate_coin_cost(slots, start_slots, COIN_CONFIG[building_name])
                    total_coins += cost
                    caption = f"Remaining to Max: {cost:,}"
                else:
                    cost = calculate_diamond_cost(slots, start_slots)
                    total_diamonds += cost
                    caption = f"Remaining to Max: {cost:,}"
                
                current_building_cost += cost

            if current_building_cost > 0:
                 st.info(f"{currency_label} {caption.split(':')[0]}: {current_building_cost:,}")

# Update Sidebar Totals
total_diamonds_placeholder.metric("Diamonds 💎", total_diamonds)
total_coins_placeholder.metric("Coins 💰", f"{total_coins:,}")
