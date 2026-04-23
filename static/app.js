const canvas = document.getElementById('pulseCanvas');
const ctx = canvas.getContext('2d');
const stateLabel = document.getElementById('state-label');
const wallContainer = document.getElementById('memory-wall');
const feedContainer = document.getElementById('whisper-feed');

let width, height;
function resize() {
    width = canvas.parentElement.clientWidth;
    height = canvas.parentElement.clientHeight - 40; // minus header
    canvas.width = width;
    canvas.height = height;
}
window.addEventListener('resize', resize);
resize();

// HMM States and Colors
const STATE_MAP = {
    0: { name: "🌊 Drift", color: "#0096FF", amp: 0.5, freq: 1.0, jag: 0.0 },
    1: { name: "🔥 Ignition", color: "#FF6400", amp: 1.5, freq: 2.0, jag: 0.1 },
    2: { name: "🧱 Wall", color: "#C80032", amp: 0.2, freq: 0.5, jag: 0.3 },
    3: { name: "😴 Exhaustion", color: "#646464", amp: 0.5, freq: 0.5, jag: 0.0 },
    4: { name: "🐋 Accumulation", color: "#9600C8", amp: 2.0, freq: 0.3, jag: 0.0 },
    5: { name: "💥 Panic", color: "#FF0000", amp: 3.0, freq: 3.0, jag: 1.5 },
    6: { name: "🎯 Conviction", color: "#00FF64", amp: 2.0, freq: 2.5, jag: 0.0 }
};

// Current Pulse Animation State
let phase = 0;
let currentConfig = STATE_MAP[0];
let targetConfig = STATE_MAP[0];

// Smoothly interpolate between states
function lerp(start, end, amt) {
    return (1 - amt) * start + amt * end;
}
function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? { r: parseInt(result[1], 16), g: parseInt(result[2], 16), b: parseInt(result[3], 16) } : null;
}

// Memory Wall Array
const MAX_HISTORY = 60;
const historyBlocks = [];

// Initialize Memory Wall DOM
for(let i=0; i<MAX_HISTORY; i++) {
    const block = document.createElement('div');
    block.className = 'memory-block';
    block.style.backgroundColor = 'transparent';
    wallContainer.appendChild(block);
    historyBlocks.push(block);
}

// WebSocket Connection
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const wsUrl = `${protocol}//${window.location.host}/ws`;
let ws;

function connect() {
    ws = new WebSocket(wsUrl);
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'tick') {
            updateDashboard(data.state, data.narrative);
        } else if (data.type === 'narrative') {
            addNarrative(data.text, "#505060");
        }
    };
    
    ws.onclose = () => {
        setTimeout(connect, 1000);
    };
}
connect();

function updateDashboard(stateIdx, narrativeText) {
    const stateData = STATE_MAP[stateIdx] || STATE_MAP[0];
    
    // Update Target Config for Pulse
    targetConfig = stateData;
    
    // Update Label
    stateLabel.innerText = stateData.name;
    stateLabel.style.color = stateData.color;
    
    // Update Memory Wall
    for(let i=0; i<MAX_HISTORY-1; i++) {
        historyBlocks[i].style.backgroundColor = historyBlocks[i+1].style.backgroundColor;
    }
    historyBlocks[MAX_HISTORY-1].style.backgroundColor = stateData.color;
    
    // Update Feed
    if(narrativeText) {
        addNarrative(narrativeText, stateData.color);
    }
}

function addNarrative(text, color) {
    const line = document.createElement('div');
    line.className = 'whisper-line';
    
    const time = new Date().toLocaleTimeString('en-US', { hour12: false });
    
    line.innerHTML = `<span class="timestamp">${time} — </span><span style="color: ${color}">${text}</span>`;
    
    feedContainer.appendChild(line);
    feedContainer.scrollTop = feedContainer.scrollHeight;
}

// Pulse Animation Loop
function drawPulse() {
    requestAnimationFrame(drawPulse);
    
    // Lerp parameters
    currentConfig.amp = lerp(currentConfig.amp, targetConfig.amp, 0.05);
    currentConfig.freq = lerp(currentConfig.freq, targetConfig.freq, 0.05);
    currentConfig.jag = lerp(currentConfig.jag, targetConfig.jag, 0.05);
    
    ctx.clearRect(0, 0, width, height);
    
    phase -= 0.1 * currentConfig.freq;
    
    ctx.beginPath();
    ctx.moveTo(0, height / 2);
    
    // Draw Wave
    for (let x = 0; x < width; x++) {
        const normalizedX = (x / width) * 10;
        
        let y = Math.sin(normalizedX * 2 + phase) * (currentConfig.amp * 30);
        y += Math.sin(normalizedX * 5 - phase * 1.5) * (currentConfig.amp * 10);
        
        if (currentConfig.jag > 0) {
            y += (Math.random() - 0.5) * currentConfig.jag * 30;
        }
        
        ctx.lineTo(x, (height / 2) + y);
    }
    
    const rgb = hexToRgb(targetConfig.color);
    
    // Style Line
    ctx.strokeStyle = `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 1)`;
    ctx.lineWidth = 4;
    ctx.stroke();
    
    // Fill Underneath
    ctx.lineTo(width, height);
    ctx.lineTo(0, height);
    ctx.closePath();
    
    const gradient = ctx.createLinearGradient(0, height/2, 0, height);
    gradient.addColorStop(0, `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0.3)`);
    gradient.addColorStop(1, `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0)`);
    ctx.fillStyle = gradient;
    ctx.fill();
}

drawPulse();
