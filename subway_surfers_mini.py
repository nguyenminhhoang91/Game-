import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Mini Subway Surfers", page_icon="🏃‍♂️", layout="centered")

st.title("🏃‍♂️ Mini Subway Surfers (Streamlit Edition)")
st.write("Sử dụng các phím mũi tên **Trái / Phải** (hoặc nút bấm bên dưới) để di chuyển nhân vật né các chướng ngại vật màu đỏ!")

# Mã nguồn HTML/JS nhúng game canvas trực tiếp vào Streamlit
game_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Subway Surfers Mini</title>
    <style>
        body {
            margin: 0;
            background-color: #1a1a1a;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white;
            font-family: Arial, sans-serif;
        }
        canvas {
            background: linear-gradient(to bottom, #87CEEB, #e0f6ff);
            border: 4px solid #fff;
            box-shadow: 0px 0px 20px rgba(0,0,0,0.5);
        }
    </style>
</head>
<body>

<div>
    <canvas id="gameCanvas" width="400" height="500"></canvas>
    <div style="text-align: center; margin-top: 10px;">
        <button onclick="moveLeft()" style="padding: 10px 20px; font-size: 16px; cursor: pointer;">⬅️ Trái</button>
        <button onclick="moveRight()" style="padding: 10px 20px; font-size: 16px; cursor: pointer;">Phải ➡️</button>
    </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// 3 làn đường: x = 80, 200, 320
const lanes = [80, 200, 320];
let playerLane = 1; // Bắt đầu ở làn giữa
let score = 0;
let isGameOver = false;

// Đối tượng người chơi
let player = {
    y: 400,
    radius: 20,
    color: "#ffcc00"
};

// Danh sách chướng ngại vật
let obstacles = [];

function spawnObstacle() {
    if (isGameOver) return;
    let lane = Math.floor(Math.random() * 3);
    obstacles.push({
        lane: lane,
        y: -50,
        width: 60,
        height: 40,
        color: "#ff4444"
    });
}

// Tạo chướng ngại vật định kỳ
setInterval(spawnObstacle, 1500);

function moveLeft() {
    if (playerLane > 0) playerLane--;
}

function moveRight() {
    if (playerLane < 2) playerLane++;
}

// Bắt sự kiện bàn phím
window.addEventListener('keydown', function(e) {
    if (e.key === "ArrowLeft" || e.key === "a") {
        moveLeft();
    } else if (e.key === "ArrowRight" || e.key === "d") {
        moveRight();
    } else if (e.key === " " && isGameOver) {
        resetGame();
    }
});

function resetGame() {
    obstacles = [];
    score = 0;
    playerLane = 1;
    isGameOver = false;
    loop();
}

function update() {
    if (isGameOver) return;

    // Di chuyển chướng ngại vật xuống dưới
    for (let i = 0; i < obstacles.length; i++) {
        obstacles[i].y += 4;

        // Kiểm tra va chạm
        let obs = obstacles[i];
        if (obs.lane === playerLane && obs.y + obs.height >= player.y - player.radius && obs.y <= player.y + player.radius) {
            isGameOver = true;
        }
    }

    // Xóa chướng ngại vật ra khỏi mảng khi ra ngoài màn hình
    obstacles = obstacles.filter(obs => obs.y < canvas.height + 50);

    score++;
}

function draw() {
    // Xóa màn hình
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Vẽ các đường ray (làn đường)
    ctx.strokeStyle = "#8b5a2b";
    ctx.lineWidth = 6;
    [140, 260].forEach(x => {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    });

    // Vẽ người chơi
    let targetX = lanes[playerLane];
    ctx.beginPath();
    ctx.arc(targetX, player.y, player.radius, 0, Math.PI * 2);
    ctx.fillStyle = player.color;
    ctx.fill();
    ctx.strokeStyle = "#b38600";
    ctx.lineWidth = 3;
    ctx.stroke();
    
    // Vẽ mặt nhân vật đơn giản
    ctx.fillStyle = "#000";
    ctx.beginPath();
    ctx.arc(targetX - 6, player.y - 4, 3, 0, Math.PI * 2);
    ctx.arc(targetX + 6, player.y - 4, 3, 0, Math.PI * 2);
    ctx.fill();

    // Vẽ chướng ngại vật (Xe lửa/Chướng ngại vật)
    for (let i = 0; i < obstacles.length; i++) {
        let obs = obstacles[i];
        let obsX = lanes[obs.lane] - obs.width / 2;
        ctx.fillStyle = obs.color;
        ctx.fillRect(obsX, obs.y, obs.width, obs.height);
        ctx.strokeStyle = "#990000";
        ctx.lineWidth = 2;
        ctx.strokeRect(obsX, obs.y, obs.width, obs.height);
    }

    // Hiển thị điểm số
    ctx.fillStyle = "#000";
    ctx.font = "20px Arial";
    ctx.fillText("Điểm: " + score, 20, 30);

    // Màn hình Game Over
    if (isGameOver) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#fff";
        ctx.font = "30px Arial";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 20);

        ctx.font = "18px Arial";
        ctx.fillText("Điểm của bạn: " + score, canvas.width / 2, canvas.height / 2 + 20);
        ctx.fillText("Nhấn phím Cách (Space) để chơi lại", canvas.width / 2, canvas.height / 2 + 60);
        ctx.textAlign = "left"; // reset
    }
}

function loop() {
    update();
    draw();
    if (!isGameOver) {
        requestAnimationFrame(loop);
    } else {
        // Vẫn vẽ lại 1 lần để hiện màn hình game over
        draw();
    }
}

loop();
</script>

</body>
</html>
"""

# Hiển thị game trong ứng dụng Streamlit
components.html(game_code, height=600, scrolling=False)
