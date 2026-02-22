import React, { useState, useEffect } from 'react';
import './App.css';
import { MULTI_INSTANCE_CONFIG, COIN_CONFIG, MAX_SLOTS_DIAMOND, MAX_SLOTS_COIN, EXCLUDED_BUILDINGS } from './utils/calculator';
import BuildingCard from './components/BuildingCard';

function App() {
    const [globalReduce, setGlobalReduce] = useState(0);
    const [totals, setTotals] = useState({ diamonds: 0, coins: 0 });

    // This will securely hold the state of all sliders later
    const [sliderStates, setSliderStates] = useState({});

    // This structure holds cost per building: { "Bakery": { cost: 100, isCoin: false }, ... }
    const [buildingCosts, setBuildingCosts] = useState({});

    // List of files that would be returned from Python os.listdir
    // We'll hardcode the known list based on standard Hay Day buildings or fetch dynamically
    // For standard vite, we can use import.meta.glob to read the public folder images if they were in src,
    // but since they are in public we can just use a predefined array or fetch them.
    // We'll assume a comprehensive static list or fetch from an API if we had one. 
    // Actually, Vite doesn't list `public/` files dynamically at runtime easily without a manifest.
    // For simplicity, let's inject a known list or use a robust fallback.
    const [buildingFiles, setBuildingFiles] = useState([
        "01_Bakery.png", "02_Feed_Mill.png", "03_Dairy.png", "04_Sugar_Mill.png",
        "05_Popcorn_Pot.png", "06_BBQ_Grill.png", "07_Pie_Oven.png", "08_Loom.png",
        "09_Sewing_Machine.png", "10_Cake_Oven.png", "11_Mine.png", "12_Smelter.png",
        "13_Juice_Press.png", "14_Lure_Workbench.png", "15_Ice_Cream_Maker.png",
        "16_Net_Maker.png", "17_Jam_Maker.png", "18_Jeweler.png", "19_Honey_Extractor.png",
        "20_Coffee_Kiosk.png", "21_Lobster_Pool.png", "22_Soup_Kitchen.png",
        "23_Candle_Maker.png", "24_Flower_Shop.png", "25_Duck_Salon.png",
        "26_Candy_Machine.png", "27_Sauce_Maker.png", "28_Sushi_Bar.png",
        "29_Salad_Bar.png", "30_Sandwich_Bar.png", "31_Smoothie_Mixer.png",
        "32_Pasta_Maker.png", "33_Essential_Oils_Lab.png", "34_Wok_Kitchen.png",
        "35_Hat_Maker.png", "36_Pasta_Kitchen.png", "37_Hot_Dog_Stand.png",
        "38_Donut_Maker.png", "39_Taco_Kitchen.png", "40_Omelet_Station.png",
        "41_Tea_Stand.png", "42_Fondue_Pot.png", "43_Bath_Kiosk.png",
        "44_Deep_Fryer.png", "45_Preservation_Station.png", "46_Pottery_Studio.png",
        "47_Fudge_Shop.png", "48_Yogurt_Maker.png", "49_Stew_Pot.png",
        "50_Cupcake_Maker.png", "51_Perfumerie.png", "52_Waffle_Maker.png",
        "53_Porridge_Bar.png", "54_Milkshake_Bar.png"
    ]);

    const handleCostChange = (buildingName, cost, isCoin) => {
        setBuildingCosts(prev => ({
            ...prev,
            [buildingName]: { cost, isCoin }
        }));
    };

    useEffect(() => {
        let newDiamonds = 0;
        let newCoins = 0;

        Object.values(buildingCosts).forEach(b => {
            if (b.isCoin) newCoins += b.cost;
            else newDiamonds += b.cost;
        });

        setTotals({ diamonds: newDiamonds, coins: newCoins });
    }, [buildingCosts]);

    return (
        <div className="app-container">
            <header className="header">
                <h1>🌾 Hay Day Calculator</h1>
                <p>Optimize your diamonds and coins for production building slots.</p>
            </header>

            <div className="layout-grid">
                <aside className="sidebar glass-panel">
                    <div className="total-card">
                        <div className="total-label">Total Diamonds</div>
                        <div className="total-value">💎 {totals.diamonds.toLocaleString()}</div>
                    </div>
                    <div className="total-card">
                        <div className="total-label">Total Coins</div>
                        <div className="total-value">💰 {totals.coins.toLocaleString()}</div>
                    </div>

                    <div className="global-control">
                        <h3>Global Target Reduction</h3>
                        <p className="text-sm text-muted mb-2">Reduce max target slots by:</p>
                        {/* Global slider component will go here */}
                        <input type="range" min="0" max="8" value={globalReduce} onChange={(e) => setGlobalReduce(parseInt(e.target.value))} style={{ width: '100%' }} />
                        <div style={{ textAlign: 'center', marginTop: '0.5rem' }}>{globalReduce} Slots</div>
                    </div>
                </aside>

                <main className="buildings-grid">
                    {buildingFiles.map(filename => (
                        <BuildingCard
                            key={filename}
                            filename={filename}
                            excludedBuildings={EXCLUDED_BUILDINGS}
                            globalReduce={globalReduce}
                            onCostChange={handleCostChange}
                        />
                    ))}
                </main>
            </div>

            <div className="bottom-bar glass-panel">
                <div className="bottom-totals">
                    <div className="bottom-total-item">
                        <span className="total-label">Diamonds:</span>
                        <span className="total-value-small">💎 {totals.diamonds.toLocaleString()}</span>
                    </div>
                    <div className="bottom-total-item">
                        <span className="total-label">Coins:</span>
                        <span className="total-value-small">💰 {totals.coins.toLocaleString()}</span>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
