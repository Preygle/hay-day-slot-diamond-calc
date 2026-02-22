export const MULTI_INSTANCE_CONFIG = {
    "Feed Mill": 2,
    "Smelter": 5,
    "Sugar Mill": 2
};

export const EXCLUDED_BUILDINGS = ["Mine"];

export const COIN_CONFIG = {
    "Lobster Pool": {
        2: 45000, 3: 52500, 4: 63800, 5: 79800, 6: 102000
    },
    "Duck Salon": {
        2: 51000, 3: 59000, 4: 72000, 5: 90000, 6: 115000
    }
};

export const SPECIAL_DIAMOND_CONFIG = {
    "Net Maker": { 3: 10, 4: 20, 5: 45, 6: 90, 7: 130, 8: 260, 9: 415 },
    "Lure Workbench": { 3: 10, 4: 20, 5: 45, 6: 90, 7: 130, 8: 260, 9: 415 }
};

export const MAX_SLOTS_DIAMOND = 9;
export const MAX_SLOTS_COIN = 6;

export function calculateDiamondCost(targetSlots, startSlots, buildingName = null) {
    if (targetSlots <= startSlots) {
        return 0;
    }

    let cost = 0;

    if (buildingName && SPECIAL_DIAMOND_CONFIG[buildingName]) {
        const config = SPECIAL_DIAMOND_CONFIG[buildingName];
        for (let n = startSlots + 1; n <= targetSlots; n++) {
            cost += (config[n] || 0);
        }
        return cost;
    }

    for (let n = startSlots + 1; n <= targetSlots; n++) {
        const paidIdx = n - startSlots - 1;
        const stepCost = 6 + (paidIdx * 3);
        cost += stepCost;
    }
    return cost;
}

export function calculateCoinCost(targetSlots, startSlots, costTable) {
    if (targetSlots <= startSlots) {
        return 0;
    }
    let cost = 0;
    for (let n = startSlots + 1; n <= targetSlots; n++) {
        cost += (costTable[n] || 0);
    }
    return cost;
}

export function getBuildingName(filename) {
    // Assuming format like "01_Bakery.png"
    const base = filename.split('.').slice(0, -1).join('.');
    const parts = base.split('_');

    // If first part is a number (like '01'), remove it
    if (parts.length > 1 && !isNaN(parts[0])) {
        parts.shift();
    }

    return parts.join(' ').replace(/_/g, ' ');
}
