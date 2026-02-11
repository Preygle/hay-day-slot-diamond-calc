import streamlit as st
import os
from PIL import Image

# Monkeypatch for streamlit_analytics which uses removed experimental_get_query_params
try:
    if not hasattr(st, "experimental_get_query_params"):
        # st.query_params returns a dict-like object. 
        # experimental_get_query_params returned {key: [val, ...]}
        # We'll map it to match the expected format roughly or just dict
        st.experimental_get_query_params = lambda: {k: [v] for k, v in st.query_params.items()}
except AttributeError:
    pass

import streamlit_analytics

st.set_page_config(page_title="Hay Day Calculator", page_icon="🌾", layout="wide")

with streamlit_analytics.track():
    st.title("🌾 Hay Day Production Building Calculator")
    st.markdown("Calculate the number of diamonds and coins required to unlock remaining slots.")

    with st.expander("📖 **How to Use this Calculator**", expanded=True):
        st.markdown("""
        1. **Slot Range (Current ➔ Target)**: 
           - Use the **Left Handle** to set how many slots you *currently* have.
           - Use the **Right Handle** to set your *target* number of slots.
           - The *Cost* is calculated for the difference between them.
        
        2. **Batch Calculation**:
           - Adjust as many sliders as you like.
           - Click the **"Calculate Costs"** button at the very bottom to update the totals.
        
        3. **Global Controls (Sidebar)**:
           - Use **"Reduce Max Target By"** to automatically set all building targets to `Max - X` (e.g., set everyone to 7 slots instead of 9).
        """)

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
    COIN_CONFIG = {
        "Lobster Pool": {
            2: 45000, 3: 52500, 4: 63800, 5: 79800, 6: 102000
        },
        "Duck Salon": {
            2: 51000, 3: 59000, 4: 72000, 5: 90000, 6: 115000
        }
    }

    # Special Diamond Configuration
    SPECIAL_DIAMOND_CONFIG = {
        "Net Maker": {3: 10, 4: 20, 5: 45, 6: 90, 7: 130, 8: 260, 9: 415},
        "Lure Workbench": {3: 10, 4: 20, 5: 45, 6: 90, 7: 130, 8: 260, 9: 415}
    }

    MAX_SLOTS_DIAMOND = 9
    MAX_SLOTS_COIN = 6

    # --- Logic Functions ---

    def calculate_diamond_cost(target_slots, start_slots, building_name=None):
        # Calculate cost to reach 'target_slots' from 'start_slots'
        if target_slots <= start_slots:
            return 0
        
        cost = 0

        # Check for special configuration first
        if building_name and building_name in SPECIAL_DIAMOND_CONFIG:
            config = SPECIAL_DIAMOND_CONFIG[building_name]
            # Calculate cost for unlocking slots from start+1 up to target
            for n in range(start_slots + 1, target_slots + 1):
                 cost += config.get(n, 0)
            return cost

        # Standard logic
        for n in range(start_slots + 1, target_slots + 1):
            # Cost of unlocking slot n
            # start_slots = 2. Slot 3 is 1st paid.
            # paid_idx = 3 - 2 - 1 = 0 -> 6
            paid_idx = n - start_slots - 1
            step_cost = 6 + (paid_idx * 3)
            cost += step_cost
        return cost

    def calculate_coin_cost(target_slots, start_slots, cost_table):
        if target_slots <= start_slots:
            return 0
        cost = 0
        for n in range(start_slots + 1, target_slots + 1):
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

    # --- GLOBAL CONTROL ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("Global Controls")

    # 1. Reduce Max Targets
    reduce_amount = st.sidebar.slider(
        "Reduce Max Target By", 
        min_value=0, 
        max_value=8, 
        value=0,
        help="Reduces the target slot count by this amount from the maximum."
    )

    if st.sidebar.button("Apply Reduction"):
        for f in files:
            b_name = get_building_name(f)
            if b_name in EXCLUDED_BUILDINGS: continue
            
            # Identify max slots for this building
            is_c = b_name in COIN_CONFIG
            m_slots = MAX_SLOTS_COIN if is_c else MAX_SLOTS_DIAMOND
            
            # Determine start slots (standard or custom)
            if b_name == "Smelter":
                s_slots = 1
            elif b_name == "Feed Mill":
                s_slots = 3
            elif is_c:
                s_slots = 1
            else:
                s_slots = 2
            
            # Calculate new target
            new_target = m_slots - reduce_amount
            
            # Only apply if valid (Target >= Start)
            if new_target >= s_slots:
                i_count = MULTI_INSTANCE_CONFIG.get(b_name, 1)
                for i in range(i_count):
                    key = f"slider_{f}_{i}"
                    # We set the range to (Start, New Target)
                    # This implies user wants to unlock UP TO this new target.
                    # Or should we respect existing start? 
                    # Usually global control overrides. Let's reset start to default.
                    st.session_state[key] = (s_slots, new_target)
        st.rerun()

    st.subheader("Adjust Slots per Building")

    # FORM START
    with st.form("calculator_form"):
        # Render Loop
        for idx, filename in enumerate(files):
            building_name = get_building_name(filename)
            
            if building_name in EXCLUDED_BUILDINGS:
                continue

            # Setup Defaults
            instance_count = MULTI_INSTANCE_CONFIG.get(building_name, 1)
            
            if building_name == "Smelter":
                default_start = 1
            elif building_name == "Feed Mill":
                default_start = 3
            elif building_name in COIN_CONFIG:
                default_start = 1
            else:
                default_start = 2
            
            # Determine type (Coin vs Diamond)
            is_coin = building_name in COIN_CONFIG
            max_slots = MAX_SLOTS_COIN if is_coin else MAX_SLOTS_DIAMOND
            currency_label = "Coins 💰" if is_coin else "Diamonds 💎"
            
            filepath = os.path.join(IMAGE_DIR, filename)

            with st.container(border=True):
                # Two main columns: Info (Left) | Controls (Right)
                c_info, c_controls = st.columns([1, 3])
                
                with c_info:
                    try:
                        img = Image.open(filepath)
                        st.image(img, width="stretch") 
                    except Exception:
                        st.write("🖼️")
                    st.markdown(f"**{building_name}**")

                with c_controls:
                    current_building_cost = 0
                    
                    # Loop for each instance (e.g. 5 smelters)
                    for i in range(instance_count):
                        # Unique session key for slider
                        key = f"slider_{filename}_{i}"
                        
                        # Initialize default key if strictly needed for range
                        # Note: st.slider inside form reads from key on Rerun, 
                        # but if we just set it via sidebar it works!
                        if key not in st.session_state:
                             st.session_state[key] = (default_start, max_slots)

                        # Instance Label if multiple
                        label = "Slot Range (Current -> Target)"
                        if instance_count > 1:
                            label = f"{building_name} #{i+1} Range"

                        # RANGE SLIDER
                        slider_vals = st.slider(
                            label,
                            min_value=default_start, 
                            max_value=max_slots,
                            key=key,
                            help="Left handle: Current Slots. Right handle: Target Slots."
                        )
                        
                        if isinstance(slider_vals, tuple):
                             s_current, s_target = slider_vals
                        else:
                             s_current, s_target = slider_vals, slider_vals

                        # Calculate Cost
                        cost = 0
                        if is_coin:
                            cost = calculate_coin_cost(s_target, s_current, COIN_CONFIG[building_name])
                            total_coins += cost
                        else:
                            cost = calculate_diamond_cost(s_target, s_current, building_name)
                            total_diamonds += cost
                        
                        current_building_cost += cost
                    
                    # Summary for this building
                    # Because we are in a form, this logic runs on 'Submit' reruns.
                    # Or initial run.
                    if current_building_cost > 0:
                         st.info(f"Cost: {current_building_cost:,} {currency_label}")
                    else:
                         st.success("Analysis: No cost")

        st.markdown("---")
        submitted = st.form_submit_button("Calculate Costs", type="primary", use_container_width=True)

    # Update Sidebar Totals (Outside Form)
    total_diamonds_placeholder.metric("Diamonds 💎", total_diamonds)
    total_coins_placeholder.metric("Coins 💰", f"{total_coins:,}")
