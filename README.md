# 🌾 Hay Day Production Building Calculator

Link to the app: https://diamond-calc.streamlit.app

![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fdiamond-calc.streamlit.app&label=Visitors&countColor=%23263759)

A powerful tool to help Hay Day players optimize their diamond and coin usage when unlocking slots for production buildings. This application calculates the costs required to reach your target slot counts, helping you plan your resources effectively.


## ✨ Features

- **Slot Range Calculation**: Set your current and target slots for each building to see exactly what you need to spend.
- **Batch Processing**: Adjust multiple buildings at once and calculate the total cost in one go.
- **Global Control**: Quickly reduce the target slot count for all buildings (e.g., set all to 7 instead of 9) with a single slider.
- **Multi-Instance Support**: Handles buildings with multiple instances (e.g., 5 Smelters, 2 Sugar Mills) with individual controls.
- **Smart Logic**:
    - Automatically accounts for different starting slots (e.g., Feed Mill starts at 3, Smelter at 1).
    - Distinguishes between Diamond-cost and Coin-cost buildings (e.g., Duck Salon, Lobster Pool).
    - Includes special pricing rules for Net Maker and Lure Workbench.


## 🚀 Getting Started

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Preygle/hay-day-slot-diamond-calc.git
   cd production-building-diamond
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Scrape Images:**
   If the `production_building_images` folder is empty or missing, run the scraper to fetch building icons from the wiki:
   ```bash
   python img_scrape.py
   ```

### Running the App

Launch the application locally:

```bash
streamlit run app.py
```


## 🛠️ Configuration

- **`requirements.txt`**: Lists all Python dependencies (`streamlit`, `Pillow`, `requests`, `beautifulsoup4`).
- **`img_scrape.py`**: Scraper script to populate the image directory.
- **`app.py`**: Main application and website logic.

## 📄 License

This project is for educational and personal use. Hay Day content and images are property of Supercell.
