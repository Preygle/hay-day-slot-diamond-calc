# 🌾 Hay Day Production Building Calculator

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

### Prerequisites

- Python 3.7 or higher
- [Streamlit](https://streamlit.io/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
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

## ☁️ Deployment on Streamlit Cloud

This project is ready to be deployed on [Streamlit Community Cloud](https://streamlit.io/cloud) for free!

1. **Push your code to GitHub.** Ensure `requirements.txt` is in the root directory.
2. **Log in to Streamlit Cloud** with your GitHub account.
3. **Click "New app".**
4. **Select your repository, branch, and main file path** (e.g., `app.py`).
5. **Click "Deploy".**

Streamlit Cloud will automatically detect `requirements.txt`, install the dependencies, and launch your app.

## 🛠️ Configuration

- **`requirements.txt`**: Lists all Python dependencies (`streamlit`, `Pillow`, `requests`, `beautifulsoup4`).
- **`img_scrape.py`**: Scraper script to populate the image directory.
- **`app.py`**: Main application logic.

## 📄 License

This project is for educational and personal use. Hay Day content and images are property of Supercell.
