async function fetchTime(zone, format) {
  try {
    const res = await fetch(`/api/time?timezone=${zone}&format=${format}`);
    if (!res.ok) return;
    const data = await res.json();
    updateClock(data.time);
  } catch (e) {
    console.error("Error fetching time:", e);
  }
}

function updateClock(timeStr) {
  const [h, m, s] = timeStr
    .replace(/[^0-9:]/g, "")
    .split(":")
    .map(Number);

  const hours = h % 12;
  const hourDeg = (hours / 12) * 360 + (m / 60) * 30;
  const minuteDeg = (m / 60) * 360;
  const secondDeg = (s / 60) * 360;

  document.getElementById("hour").style.transform = `translateX(-50%) rotate(${hourDeg}deg)`;
  document.getElementById("minute").style.transform = `translateX(-50%) rotate(${minuteDeg}deg)`;
  document.getElementById("second").style.transform = `translateX(-50%) rotate(${secondDeg}deg)`;

  document.getElementById("digital-time").textContent = timeStr;
}

function positionNumbers() {
  const radius = 140;
  const numbers = document.querySelectorAll(".number");
  numbers.forEach((num) => {
    const n = parseInt(num.dataset.num);
    const angle = (n - 3) * (Math.PI / 6);
    const x = 150 + radius * Math.cos(angle);
    const y = 150 + radius * Math.sin(angle);
    num.style.left = `${x}px`;
    num.style.top = `${y}px`;
  });
}

function init() {
  const zoneSelect = document.getElementById("zone");
  const formatSelect = document.getElementById("format");

  const update = () => fetchTime(zoneSelect.value, formatSelect.value);

  zoneSelect.addEventListener("change", update);
  formatSelect.addEventListener("change", update);
  setInterval(update, 1000);
  update();
}

window.onload = () => {
  positionNumbers();
  init();
};
