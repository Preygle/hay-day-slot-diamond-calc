import React, { useState, useEffect } from 'react';
import './BuildingCard.css';
import { calculateDiamondCost, calculateCoinCost, getBuildingName, MULTI_INSTANCE_CONFIG, COIN_CONFIG, MAX_SLOTS_DIAMOND, MAX_SLOTS_COIN } from '../utils/calculator';
import RangeSlider from './RangeSlider';

const BuildingCard = ({ filename, excludedBuildings, globalReduce, onCostChange }) => {
    const buildingName = getBuildingName(filename);

    if (excludedBuildings.includes(buildingName)) {
        return null;
    }

    const isCoin = COIN_CONFIG.hasOwnProperty(buildingName);
    const maxSlots = isCoin ? MAX_SLOTS_COIN : MAX_SLOTS_DIAMOND;
    const currencyLabel = isCoin ? "Coins 💰" : "Diamonds 💎";

    // Default logic based on Python script
    let defaultStart = 2;
    if (buildingName === "Smelter" || isCoin) {
        defaultStart = 1;
    } else if (buildingName === "Feed Mill") {
        defaultStart = 3;
    }

    const instanceCount = MULTI_INSTANCE_CONFIG[buildingName] || 1;

    // State for all instances of this building (e.g., 5 smelters)
    // Array of tuples: [[current, target], [current, target], ...]
    const [sliderValues, setSliderValues] = useState(
        Array.from({ length: instanceCount }, () => [defaultStart, maxSlots])
    );

    // Apply global reduction when it changes
    useEffect(() => {
        const newTarget = maxSlots - globalReduce;
        if (newTarget >= defaultStart) {
            setSliderValues(prev => prev.map(() => [defaultStart, newTarget]));
        }
    }, [globalReduce, maxSlots, defaultStart]);

    const [totalBuildingCost, setTotalBuildingCost] = useState(0);

    useEffect(() => {
        let cost = 0;
        sliderValues.forEach(([start, target]) => {
            if (isCoin) {
                cost += calculateCoinCost(target, start, COIN_CONFIG[buildingName]);
            } else {
                cost += calculateDiamondCost(target, start, buildingName);
            }
        });
        setTotalBuildingCost(cost);
        // Report back to App level
        onCostChange(buildingName, cost, isCoin);
    }, [sliderValues, isCoin, buildingName]);

    const handleSliderChange = (index, newValue) => {
        setSliderValues(prev => {
            const newVals = [...prev];
            newVals[index] = newValue; // newValue is an array [start, target]
            return newVals;
        });
    };

    return (
        <div className="building-card glass-panel">
            <div className="card-header">
                <div className="img-container">
                    <img src={`/images/${filename}`} alt={buildingName} onError={(e) => { e.target.onerror = null; e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='48' height='48'%3E%3Crect width='48' height='48' fill='rgba(255,255,255,0.1)'/%3E%3Ctext x='50%25' y='50%25' font-size='20' text-anchor='middle' alignment-baseline='middle' fill='white'%3E🖼️%3C/text%3E%3C/svg%3E" }} />
                </div>
                <h3 className="building-name">{buildingName}</h3>
            </div>

            <div className="sliders-container">
                {sliderValues.map((vals, idx) => (
                    <div key={idx} className="slider-group">
                        {instanceCount > 1 && <div className="instance-label">Instance #{idx + 1}</div>}
                        <RangeSlider
                            min={defaultStart}
                            max={maxSlots}
                            value={vals}
                            onChange={(newVals) => handleSliderChange(idx, newVals)}
                        />
                    </div>
                ))}
            </div>

            <div className={`cost-summary ${totalBuildingCost === 0 ? 'no-cost' : 'has-cost'}`}>
                {totalBuildingCost > 0
                    ? `Cost: ${totalBuildingCost.toLocaleString()} ${currencyLabel}`
                    : "Analysis: No cost"}
            </div>
        </div>
    );
};

export default BuildingCard;
