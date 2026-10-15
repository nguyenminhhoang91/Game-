import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Subway Surfers Pro - Fixed", page_icon="🛹", layout="centered")

st.markdown("""
    <h2 style='text-align: center; color: #ff6600; margin-bottom: 0;'>🛹 Subway Surfers: Streamlit Edition</h2>
    <p style='text-align: center; color: #666; margin-top: 5px;'>Né tàu hỏa, rào chắn và thu thập tiền vàng!</p>
""", unsafe_allow_html=True)

# Mã nguồn HTML/JS hoàn thiện có màn hình Bắt đầu & Nút Chơi lại
game_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Subway Surfers Fixed</title>
    <style>
        body {
            margin: 0;
            background: #111;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
        }
        #game-container {
            position: relative;
            box-shadow: 0 15px 35px rgba(0,0,0,0.7);
            border-radius: 12px;
            overflow: hidden;
            border: 4px solid #333;
        }
        canvas {
            display: block;
            background: linear-gradient(to bottom, #4a90e2, #b4e0ff);
        }
        .controls {
            margin-top: 12px;
            display: flex;
            gap: 15px;
        }
        button {
            padding: 10px 22px;
            font-size: 16px;
            font-weight: bold;
            background: #ffcc00;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px #b38600;
            transition: 0.1s;
        }
        button:active {
            transform: translateY(4px);
            box-shadow: 0 0 #b38600;
        }
    </style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="480" height="640"></canvas>
</div>

<div class="controls">
    <button onclick="moveLeft()">⬅️ Trái</button>
    <button onclick="jump()">⬆️ Nhảy</button>
    <button onclick="moveRight()">Phải ➡️</button>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const lanes = [130, 240, 350];
let playerLane = 1;
let playerY = 480;
let isJumping = false;
let jumpVelocity = 0;
let score = 0;
let coins = 0;
let speed = 4;

// Trạng thái game
let gameStarted = false;
let isGameOver = false;

let obstacles = [];
let coinItems = [];
let obstacleTimer = null;

// Lắng nghe sự kiện bàn phím
window.addEventListener('keydown', function(e) {
    if (!gameStarted && (e.key === "Enter" || e.key === " ")) {
        startGame();
        return;
    }
    if (isGameOver && (e.key === "r" || e.key === "R" || e.key === " ")) {
        resetGame();
        return;
    }
    if (e.key === "ArrowLeft" || e.key === "a") moveLeft();
    if (e.key === "ArrowRight" || e.key === "d") moveRight();
    if (e.key === "ArrowUp" || e.key === "w" || e.key === " ") jump();
});

// Xử lý click chuột trên canvas để bấm nút Bắt đầu / Chơi lại
canvas.addEventListener('click', function(e) {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    if (!gameStarted) {
        // Nút Bắt đầu (vùng giữa màn hình)
        if (x >= 140 && x <= 340 && y >= 360 && y <= 420) {
            startGame();
        }
    } else if (isGameOver) {
        // Nút Chơi lại
        if (x >= 140 && x <= 340 && y >= 400 && y <= 460) {
            resetGame();
        }
    }
});

function moveLeft() {
    if (playerLane > 0 && gameStarted && !isGameOver) playerLane--;
}

function moveRight() {
    if (playerLane < 2 && gameStarted && !isGameOver) playerLane++;
}

function jump() {
    if (!isJumping && gameStarted && !isGameOver) {
        isJumping = true;
        jumpVelocity = -12;
    }
}

function startGame() {
    gameStarted = true;
    isGameOver = false;
    resetGameValues();
    if (obstacleTimer) clearInterval(obstacleTimer);
    obstacleTimer = setInterval(spawnEntities, 2000);
    loop();
}

function resetGameValues() {
    obstacles = [];
    coinItems = [];
    score = 0;
    coins = 0;
    speed = 4;
    playerLane = 1;
    playerY = 480;
    isJumping = false;
    isGameOver = false;
}

function resetGame() {
    resetGameValues();
    gameStarted = true;
    if (obstacleTimer) clearInterval(obstacleTimer);
    obstacleTimer = setInterval(spawnEntities, 2000);
    loop();
}

function spawnEntities() {
    if (!gameStarted || isGameOver) return;
    
    let lane = Math.floor(Math.random() * 3);
    let type = Math.random() > 0.4 ? "train" : "barrier";
    
    obstacles.push({
        lane: lane,
        z: 0.1, // Bắt đầu từ xa rõ ràng hơn
        type: type
    });

    // Sinh tiền vàng
    if (Math.random() > 0.3) {
        let coinLane = (lane + 1) % 3;
        coinItems.push({
            lane: coinLane,
            z: 0.1
        });
    }
}

function project(laneX, screenY, z) {
    let vanishingX = 240;
    let vanishingY = 160;
    let x = vanishingX + (laneX - vanishingX) * z;
    let y = vanishingY + (screenY - vanishingY) * z;
    return { x: x, y: y, scale: z };
}

function update() {
    if (!gameStarted || isGameOver) return;

    if (isJumping) {
        playerY += jumpVelocity;
        jumpVelocity += 0.8;
        if (playerY >= 480) {
            playerY = 480;
            isJumping = false;
        }
    }

    speed = 4 + Math.floor(score / 400);

    // Cập nhật chướng ngại vật
    for (let i = 0; i < obstacles.length; i++) {
        obstacles[i].z += 0.025 * (speed / 4);

        let obs = obstacles[i];
        // Va chạm khi đến gần (z từ 0.80 đến 0.98)
        if (obs.z >= 0.80 && obs.z <= 0.98 && obs.lane === playerLane) {
            if (obs.type === "train" || (obs.type === "barrier" && playerY >= 430)) {
                isGameOver = true;
            }
        }
    }
    obstacles = obstacles.filter(obs => obs.z < 1.1);

    // Cập nhật tiền vàng
    for (let i = 0; i < coinItems.length; i++) {
        coinItems[i].z += 0.025 * (speed / 4);
        let c = coinItems[i];
        if (c.z >= 0.80 && c.z <= 0.98 && c.lane === playerLane) {
            coins += 10;
            coinItems.splice(i, 1);
            i--;
        }
    }
    coinItems = coinItems.filter(c => c.z < 1.1);

    score += 1;
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Bầu trời
    ctx.fillStyle = "#70c5ce";
    ctx.fillRect(0, 0, canvas.width, 160);

    // Tòa nhà nền
    ctx.fillStyle = "#5298a0";
    ctx.fillRect(40, 60, 70, 100);
    ctx.fillRect(130, 40, 90, 120);
    ctx.fillRect(280, 50, 100, 110);
    ctx.fillRect(390, 70, 60, 90);

    // 2. Mặt đất & Đường ray
    ctx.fillStyle = "#2c2c2c";
    ctx.beginPath();
    ctx.moveTo(240, 160);
    ctx.lineTo(0, 640);
    ctx.lineTo(480, 640);
    ctx.closePath();
    ctx.fill();

    let baseLanesX = [130, 240, 350];
    let topVanishingX = 240;
    let topVanishingY = 160;

    for (let i = 0; i < 3; i++) {
        ctx.strokeStyle = "#8b5a2b";
        ctx.lineWidth = 5;
        ctx.beginPath();
        ctx.moveTo(topVanishingX, topVanishingY);
        ctx.lineTo(baseLanesX[i], 640);
        ctx.stroke();
    }

    // 3. Tiền vàng
    for (let i = 0; i < coinItems.length; i++) {
        let c = coinItems[i];
        let p = project(baseLanesX[c.lane], 500, c.z);
        let radius = 14 * c.scale;
        
        ctx.beginPath();
        ctx.arc(p.x, p.y - 20, radius, 0, Math.PI * 2);
        ctx.fillStyle = "#ffd700";
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = "#ff8c00";
        ctx.stroke();
        
        ctx.fillStyle = "#b36b00";
        ctx.font = `bold ${Math.floor(14 * c.scale)}px Arial`;
        ctx.fillText("$", p.x - 5 * c.scale, p.y - 14 * c.scale);
    }

    // 4. Chướng ngại vật (Tàu hỏa & Rào chắn)
    let allEntities = [];
    obstacles.forEach(o => allEntities.push(o));
    allEntities.sort((a, b) => a.z - b.z);

    allEntities.forEach(item => {
        let p = project(baseLanesX[item.lane], 480, item.z);
        let scale = item.scale;

        if (item.type === "train") {
            let w = 100 * scale;
            let h = 140 * scale;
            let x = p.x - w / 2;
            let y = p.y - h;

            // Thân tàu hỏa màu đỏ nổi bật
            ctx.fillStyle = "#e74c3c";
            ctx.fillRect(x, y, w, h);

            // Kính chắn gió
            ctx.fillStyle = "#3498db";
            ctx.fillRect(x + w * 0.15, y + h * 0.1, w * 0.7, h * 0.3);

            // Đèn pha
            ctx.fillStyle = "#f1c40f";
            ctx.beginPath();
            ctx.arc(x + w * 0.5, y + h * 0.6, 9 * scale, 0, Math.PI * 2);
            ctx.fill();

            ctx.strokeStyle = "#c0392b";
            ctx.lineWidth = 3;
            ctx.strokeRect(x, y, w, h);
        } else {
            let w = 90 * scale;
            let h = 50 * scale;
            let x = p.x - w / 2;
            let y = p.y - h;

            ctx.fillStyle = "#d35400";
            ctx.fillRect(x, y, w, h);

            // Sọc vàng cảnh báo
            ctx.fillStyle = "#f1c40f";
            ctx.fillRect(x + w * 0.2, y, w * 0.2, h);
            ctx.fillRect(x + w * 0.6, y, w * 0.2, h);
            
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 2;
            ctx.strokeRect(x, y, w, h);
        }
    });

    // 5. Nhân vật
    let playerX = baseLanesX[playerLane];
    let pRadius = 28;

    // Ván trượt
    ctx.fillStyle = "#9b59b6";
    ctx.beginPath();
    ctx.ellipse(playerX, playerY + 12, 22, 8, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#512e5f";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Thân
    ctx.fillStyle = "#ecf0f1";
    ctx.beginPath();
    ctx.arc(playerX, playerY - 10, pRadius, 0, Math.PI * 2);
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = "#bdc3c7";
    ctx.stroke();

    // Mặt
    ctx.fillStyle = "#f39c12";
    ctx.beginPath();
    ctx.arc(playerX, playerY - 14, 16, 0, Math.PI * 2);
    ctx.fill();

    // Mũ lưỡi trai đỏ
    ctx.fillStyle = "#c0392b";
    ctx.beginPath();
    ctx.arc(playerX, playerY - 22, 14, Math.PI, Math.PI * 2);
    ctx.fill();
    ctx.fillRect(playerX - 2, playerY - 26, 16, 5);

    // Điểm số HUD
    if (gameStarted && !isGameOver) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
        ctx.fillRect(15, 15, 160, 70);
        
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 18px Arial";
        ctx.fillText("🌟 Điểm: " + Math.floor(score), 25, 42);
        ctx.fillText("💰 Tiền: " + coins, 25, 70);
    }

    // --- MÀN HÌNH BẮT ĐẦU ---
    if (!gameStarted) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#ffcc00";
        ctx.font = "bold 34px Arial";
        ctx.textAlign = "center";
        ctx.fillText("SUBWAY SURFERS", canvas.width / 2, canvas.height / 2 - 70);

        ctx.fillStyle = "#ffffff";
        ctx.font = "16px Arial";
        ctx.fillText("Dùng phím Trái/Phải hoặc nút bên dưới để né tránh", canvas.width / 2, canvas.height / 2 - 25);

        // Nút Bắt Đầu
        ctx.fillStyle = "#27ae60";
        ctx.fillRect(canvas.width / 2 - 100, canvas.height / 2 + 20, 200, 50);
        ctx.strokeStyle = "#2ecc71";
        ctx.lineWidth = 3;
        ctx.strokeRect(canvas.width / 2 - 100, canvas.height / 2 + 20, 200, 50);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 20px Arial";
        ctx.fillText("BẮT ĐẦU CHƠI", canvas.width / 2, canvas.height / 2 + 52);
        ctx.textAlign = "left";
    }

    // --- MÀN HÌNH GAME OVER (KẾT THÚC) ---
    if (isGameOver) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#e74c3c";
        ctx.font = "bold 36px Arial";
        ctx.textAlign = "center";
        ctx.fillText("BẮT GIỮ!", canvas.width / 2, canvas.height / 2 - 60);

        ctx.fillStyle = "#ffffff";
        ctx.font = "18px Arial";
        ctx.fillText("Tổng điểm: " + Math.floor(score), canvas.width / 2, canvas.height / 2 - 10);
        ctx.fillText("Số vàng thu thập: " + coins, canvas.width / 2, canvas.height / 2 + 20);

        // Nút Chơi Lại có chữ rõ ràng
        ctx.fillStyle = "#f39c12";
        ctx.fillRect(canvas.width / 2 - 100, canvas.height / 2 + 60, 200, 50);
        ctx.strokeStyle = "#f1c40f";
        ctx.lineWidth = 3;
        ctx.strokeRect(canvas.width / 2 - 100, canvas.height / 2 + 60, 200, 50);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 20px Arial";
        ctx.fillText("CHƠI LẠI", canvas.width / 2, canvas.height / 2 + 92);
        ctx.textAlign = "left";
    }
}

function loop() {
    update();
    draw();
    if (gameStarted && !isGameOver) {
        requestAnimationFrame(loop);
    }
}

// Vẽ khung hình chờ ban đầu
draw();
</script>

</body>
</html>
"""

components.html(game_code, height=720, scrolling=False)
