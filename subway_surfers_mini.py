import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Subway Surfers 3D Pro Edition", page_icon="🛹", layout="centered")

st.markdown("""
    <h2 style='text-align: center; color: #ff6600;'>🛹 Subway Surfers: Streamlit Pro Edition</h2>
    <p style='text-align: center; color: #666;'>Chạy trốn cảnh sát, né tàu hỏa, nhảy qua rào chắn và thu thập tiền vàng!</p>
""", unsafe_allow_html=True)

# Mã nguồn HTML/JS nâng cấp đồ họa tuyệt đẹp
game_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Subway Surfers Pro</title>
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
            padding: 12px 24px;
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

// Thông số trò chơi phong cách phối cảnh 3D giả lập (Perspective)
const lanes = [130, 240, 350]; // 3 vị trí làn đường ở đáy
let playerLane = 1; // 0: Trái, 1: Giữa, 2: Phải
let playerY = 480;
let isJumping = false;
let jumpVelocity = 0;
let score = 0;
let coins = 0;
let speed = 5;
let isGameOver = false;

let obstacles = [];
let coinItems = [];

// Khởi tạo phím điều khiển
window.addEventListener('keydown', function(e) {
    if (e.key === "ArrowLeft" || e.key === "a") moveLeft();
    if (e.key === "ArrowRight" || e.key === "d") moveRight();
    if (e.key === "ArrowUp" || e.key === "w" || e.key === " ") jump();
    if (e.key === "r" && isGameOver) resetGame();
});

function moveLeft() {
    if (playerLane > 0 && !isGameOver) playerLane--;
}

function moveRight() {
    if (playerLane < 2 && !isGameOver) playerLane++;
}

function jump() {
    if (!isJumping && !isGameOver) {
        isJumping = true;
        jumpVelocity = -12;
    }
}

function resetGame() {
    obstacles = [];
    coinItems = [];
    score = 0;
    coins = 0;
    speed = 5;
    playerLane = 1;
    isJumping = false;
    isGameOver = false;
    loop();
}

// Sinh chướng ngại vật (Tàu hỏa, rào chắn) và Tiền vàng
function spawnEntities() {
    if (isGameOver) return;
    
    // Tỷ lệ xuất hiện chướng ngại vật
    let lane = Math.floor(Math.random() * 3);
    let type = Math.random() > 0.4 ? "train" : "barrier";
    
    obstacles.push({
        lane: lane,
        z: 0.1, // z chạy từ 0.1 (xa) đến 1.0 (gần)
        type: type,
        height: type === "train" ? 120 : 50
    });

    // Sinh tiền vàng bổ trợ
    if (Math.random() > 0.3) {
        let coinLane = (lane + 1) % 3;
        coinItems.push({
            lane: coinLane,
            z: 0.1
        });
    }
}

setInterval(spawnEntities, 1800);

// Hàm hỗ trợ chiếu phối cảnh 3D (Perspective Projection)
function project(laneX, screenY, z) {
    // Điểm tụ ở giữa màn hình (240, 160)
    let vanishingX = 240;
    let vanishingY = 160;
    let x = vanishingX + (laneX - vanishingX) * z;
    let y = vanishingY + (screenY - vanishingY) * z;
    return { x: x, y: y, scale: z };
}

function update() {
    if (isGameOver) return;

    // Xử lý nhảy
    if (isJumping) {
        playerY += jumpVelocity;
        jumpVelocity += 0.8; // Trọng lực
        if (playerY >= 480) {
            playerY = 480;
            isJumping = false;
        }
    }

    // Tăng tốc độ theo điểm
    speed = 5 + Math.floor(score / 500);

    // Cập nhật chướng ngại vật
    for (let i = 0; i < obstacles.length; i++) {
        obstacles[i].z += 0.02 * (speed / 5);

        // Kiểm tra va chạm khi vật thể đến gần người chơi (z khoảng 0.85 -> 1.0)
        let obs = obstacles[i];
        if (obs.z >= 0.82 && obs.z <= 0.98 && obs.lane === playerLane) {
            if (obs.type === "train" || (obs.type === "barrier" && playerY >= 430)) {
                isGameOver = true;
            }
        }
    }
    obstacles = obstacles.filter(obs => obs.z < 1.1);

    // Cập nhật tiền vàng
    for (let i = 0; i < coinItems.length; i++) {
        coinItems[i].z += 0.02 * (speed / 5);
        let c = coinItems[i];
        if (c.z >= 0.82 && c.z <= 0.98 && c.lane === playerLane) {
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

    // 1. Vẽ bầu trời và cảnh nền (Thành phố đồ họa phong cách Subway Surfers)
    ctx.fillStyle = "#70c5ce";
    ctx.fillRect(0, 0, canvas.width, 160);

    // Tòa nhà phía xa
    ctx.fillStyle = "#5298a0";
    ctx.fillRect(40, 60, 70, 100);
    ctx.fillRect(130, 40, 90, 120);
    ctx.fillRect(280, 50, 100, 110);
    ctx.fillRect(390, 70, 60, 90);

    // 2. Vẽ đường ray và hiệu ứng phối cảnh 3D mặt đất
    ctx.fillStyle = "#2c2c2c";
    ctx.beginPath();
    ctx.moveTo(240, 160);
    ctx.lineTo(0, 640);
    ctx.lineTo(480, 640);
    ctx.closePath();
    ctx.fill();

    // Vẽ 3 làn đường (Đường ray xe lửa màu nâu sẫm, có các thanh tà vẹt gỗ)
    let baseLanesX = [130, 240, 350];
    let topVanishingX = 240;
    let topVanishingY = 160;

    for (let i = 0; i < 3; i++) {
        ctx.strokeStyle = "#8b5a2b";
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(topVanishingX, topVanishingY);
        ctx.lineTo(baseLanesX[i], 640);
        ctx.stroke();
    }

    // 3. Vẽ Tiền Vàng
    for (let i = 0; i < coinItems.length; i++) {
        let c = coinItems[i];
        let p = project(baseLanesX[c.lane], 500, c.z);
        let radius = 12 * c.scale;
        
        ctx.beginPath();
        ctx.arc(p.x, p.y - 20, radius, 0, Math.PI * 2);
        ctx.fillStyle = "#ffd700";
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = "#ff8c00";
        ctx.stroke();
        
        // Ký hiệu chữ $ bên trong coin
        ctx.fillStyle = "#b36b00";
        ctx.font = `${Math.floor(12 * c.scale)}px Arial`;
        ctx.fillText("$", p.x - 4 * c.scale, p.y - 15 * c.scale);
    }

    // 4. Vẽ Chướng ngại vật (Tàu hỏa siêu ngầu & Rào chắn)
    // Sắp xếp vẽ từ xa tới gần để hiển thị lớp phối cảnh chính xác
    let allEntities = [];
    obstacles.forEach(o => allEntities.push({...o, entityType: 'obs'}));
    allEntities.sort((a, b) => a.z - b.z);

    allEntities.forEach(item => {
        let p = project(baseLanesX[item.lane], 480, item.z);
        let scale = item.scale;

        if (item.type === "train") {
            // Thân tàu hỏa 3D giả lập
            let w = 90 * scale;
            let h = 130 * scale;
            let x = p.x - w / 2;
            let y = p.y - h;

            // Màu đầu tàu (Đỏ/Cam phong cách Subway Surfers)
            ctx.fillStyle = "#e74c3c";
            ctx.fillRect(x, y, w, h);

            // Kính chắn gió đầu tàu
            ctx.fillStyle = "#3498db";
            ctx.fillRect(x + w * 0.15, y + h * 0.1, w * 0.7, h * 0.3);

            // Đèn pha tàu
            ctx.fillStyle = "#f1c40f";
            ctx.beginPath();
            ctx.arc(x + w * 0.5, y + h * 0.6, 8 * scale, 0, Math.PI * 2);
            ctx.fill();

            // Viền kim loại tàu
            ctx.strokeStyle = "#c0392b";
            ctx.lineWidth = 3;
            ctx.strokeRect(x, y, w, h);
        } else {
            // Rào chắn màu sọc vàng đen
            let w = 80 * scale;
            let h = 45 * scale;
            let x = p.x - w / 2;
            let y = p.y - h;

            ctx.fillStyle = "#d35400";
            ctx.fillRect(x, y, w, h);

            // Các sọc vàng cảnh báo
            ctx.fillStyle = "#f1c40f";
            ctx.fillRect(x + w * 0.2, y, w * 0.2, h);
            ctx.fillRect(x + w * 0.6, y, w * 0.2, h);
            
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 2;
            ctx.strokeRect(x, y, w, h);
        }
    });

    // 5. Vẽ Nhân vật chính (Jake đội mũ lưỡi trai, mặc áo hoodie, đi ván trượt) ở phía trước
    let playerX = baseLanesX[playerLane];
    let pRadius = 28;

    // Ván trượt bên dưới nhân vật
    ctx.fillStyle = "#9b59b6";
    ctx.beginPath();
    ctx.ellipse(playerX, playerY + 12, 22, 8, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#512e5f";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Thân nhân vật (Áo Hoodie xanh/trắng)
    ctx.fillStyle = "#ecf0f1";
    ctx.beginPath();
    ctx.arc(playerX, playerY - 10, pRadius, 0, Math.PI * 2);
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = "#bdc3c7";
    ctx.stroke();

    // Khuôn mặt & Mũ lưỡi trai đỏ đặc trưng của Subway Surfers
    ctx.fillStyle = "#f39c12"; // Khuôn mặt
    ctx.beginPath();
    ctx.arc(playerX, playerY - 14, 16, 0, Math.PI * 2);
    ctx.fill();

    // Mũ lưỡi trai đỏ
    ctx.fillStyle = "#c0392b";
    ctx.beginPath();
    ctx.arc(playerX, playerY - 22, 14, Math.PI, Math.PI * 2);
    ctx.fill();
    ctx.fillRect(playerX - 2, playerY - 26, 16, 5); // Vành mũ

    // 6. Giao diện HUD điểm số và tiền vàng trên màn hình Canvas
    ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
    ctx.fillRect(15, 15, 160, 70);
    
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 18px Arial";
    ctx.fillText("🌟 Điểm: " + score, 25, 42);
    ctx.fillText("💰 Tiền: " + coins, 25, 70);

    // Màn hình Game Over chi tiết
    if (isGameOver) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#e74c3c";
        ctx.font = "bold 38px Arial";
        ctx.textAlign = "center";
        ctx.fillText("BẮT GIỮ!", canvas.width / 2, canvas.height / 2 - 40);

        ctx.fillStyle = "#ffffff";
        ctx.font = "20px Arial";
        ctx.fillText("Tổng điểm: " + score, canvas.width / 2, canvas.height / 2 + 10);
        ctx.fillText("Số vàng thu thập: " + coins, canvas.width / 2, canvas.height / 2 + 45);

        ctx.fillStyle = "#f1c40f";
        ctx.font = "bold 16px Arial";
        ctx.fillText("Nhấn phím 'R' hoặc tải lại để chạy tiếp", canvas.width / 2, canvas.height / 2 + 95);
        ctx.textAlign = "left";
    }
}

function loop() {
    update();
    draw();
    if (!isGameOver) {
        requestAnimationFrame(loop);
    } else {
        draw();
    }
}

loop();
</script>

</body>
</html>
"""

# Hiển thị game bên trong giao diện ứng dụng Streamlit
components.html(game_code, height=720, scrolling=False)
