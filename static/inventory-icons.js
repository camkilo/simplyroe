// Inventory icon generation with Three.js
export function createItemIcon(itemType) {
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');
    
    // Item color scheme
    const itemColors = {
        'Wood': { primary: '#8B4513', secondary: '#A0522D' },
        'Stone': { primary: '#808080', secondary: '#696969' },
        'Iron': { primary: '#708090', secondary: '#556B7E' },
        'Copper': { primary: '#B87333', secondary: '#CD853F' },
        'Gold': { primary: '#FFD700', secondary: '#FFA500' },
        'Herbs': { primary: '#32CD32', secondary: '#228B22' },
        'Bone': { primary: '#F0E68C', secondary: '#BDB76B' },
        'Leather': { primary: '#8B4513', secondary: '#654321' },
        'Crystal': { primary: '#00FFFF', secondary: '#00CED1' },
        'Ice': { primary: '#E0FFFF', secondary: '#ADD8E6' },
        'Mud': { primary: '#654321', secondary: '#3E2723' },
        'Sulfur': { primary: '#FFFF00', secondary: '#FFD700' },
        'Venom': { primary: '#9400D3', secondary: '#8B008B' },
        'Scale': { primary: '#2E8B57', secondary: '#3CB371' }
    };
    
    // Find matching color or use default
    let colors = itemColors['Stone']; // default
    for (const [key, value] of Object.entries(itemColors)) {
        if (itemType.includes(key)) {
            colors = value;
            break;
        }
    }
    
    // Draw icon background
    const gradient = ctx.createRadialGradient(32, 32, 10, 32, 32, 32);
    gradient.addColorStop(0, colors.primary);
    gradient.addColorStop(1, colors.secondary);
    
    ctx.fillStyle = gradient;
    ctx.beginPath();
    
    // Draw different shapes based on item type
    if (itemType.includes('Wood')) {
        ctx.roundRect(16, 8, 32, 48, 4);
    } else if (itemType.includes('Crystal') || itemType.includes('Ice')) {
        ctx.moveTo(32, 8);
        ctx.lineTo(48, 32);
        ctx.lineTo(32, 56);
        ctx.lineTo(16, 32);
    } else if (itemType.includes('Artifact')) {
        ctx.arc(32, 32, 24, 0, Math.PI * 2);
    } else {
        ctx.roundRect(12, 12, 40, 40, 6);
    }
    
    ctx.fill();
    
    // Add shine effect
    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.beginPath();
    ctx.arc(28, 24, 8, 0, Math.PI * 2);
    ctx.fill();
    
    // Add border
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.5)';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    return canvas.toDataURL();
}

export function getRarityColor(itemType) {
    if (itemType.includes('Artifact')) return '#FFD700'; // Gold
    if (itemType.includes('Crystal')) return '#00FFFF'; // Cyan
    if (itemType.includes('Gold')) return '#FFD700'; // Gold
    if (itemType.includes('Iron') || itemType.includes('Copper')) return '#C0C0C0'; // Silver
    return '#FFFFFF'; // White
}
