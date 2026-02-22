import React, { useRef, useEffect, useState, useCallback } from 'react';
import './RangeSlider.css';

const RangeSlider = ({ min, max, value, onChange }) => {
    const [startValue, targetValue] = value;
    const sliderRef = useRef(null);

    // Percentages for positioning the thumbs and track fill
    const getPercent = useCallback(
        (val) => Math.round(((val - min) / (max - min)) * 100),
        [min, max]
    );

    const startPercent = getPercent(startValue);
    const targetPercent = getPercent(targetValue);

    const handleStartChange = (e) => {
        const val = Math.min(Number(e.target.value), targetValue);
        onChange([val, targetValue]);
    };

    const handleTargetChange = (e) => {
        const val = Math.max(Number(e.target.value), startValue);
        onChange([startValue, val]);
    };

    return (
        <div className="range-slider-container">
            <div className="values-display">
                <span className="value-label">Current: <strong>{startValue}</strong></span>
                <span className="value-label">Target: <strong>{targetValue}</strong></span>
            </div>

            <div className="slider-wrapper">
                <input
                    type="range"
                    min={min}
                    max={max}
                    value={startValue}
                    onChange={handleStartChange}
                    className="thumb thumb-left"
                    style={{ zIndex: startValue > max - 100 ? 5 : 3 }}
                />
                <input
                    type="range"
                    min={min}
                    max={max}
                    value={targetValue}
                    onChange={handleTargetChange}
                    className="thumb thumb-right"
                />

                <div className="slider-track-container" ref={sliderRef}>
                    <div className="slider-track" />
                    <div
                        className="slider-range-fill"
                        style={{
                            left: `${startPercent}%`,
                            width: `${targetPercent - startPercent}%`
                        }}
                    />
                </div>
            </div>

            <div className="ticks-container">
                {Array.from({ length: max - min + 1 }, (_, i) => min + i).map((tick) => (
                    <div key={tick} className="tick">
                        {tick}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default RangeSlider;
