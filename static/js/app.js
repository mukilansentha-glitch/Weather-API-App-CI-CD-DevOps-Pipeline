'use strict';

let unit = 'C';
let selectedCity = null;
let allCities = [];
let lightningTimer = null;
let debounceTimer = null;

function setupStars() {
  const c = document.getElementById('stars');
  c.innerHTML = '';
  for (let i = 0; i < 80; i++) {
    const s = document.createElement('div');
    s.className = 'star';
    const sz = Math.random() * 2.5 + 0.5;
    s.style.cssText = `width:${sz}px;height:${sz}px;top:${Math.random()*100}%;left:${Math.random()*100}%;animation-delay:${Math.random()*3}s;animation-duration:${2+Math.random()*3}s`;
    c.appendChild(s);
  }
}

function applySkyBg(bg) {
  document.getElementById('skyBg').style.background =
    `linear-gradient(180deg,${bg[0]} 0%,${bg[1]} 50%,${bg[2]} 100%)`;
  const sun = document.getElementById('sun');
  const isSunny = /fde|fbb|ef9|fac/.test(bg[2]);
  if (isSunny) {
    sun.style.cssText = 'position:fixed;width:110px;height:110px;border-radius:50%;top:50px;right:100px;z-index:2;pointer-events:none;background:radial-gradient(circle,#fffde7 30%,#ffd54f 60%,rgba(255,213,79,0) 100%);box-shadow:0 0 60px 20px rgba(255,213,79,.4)';
    sun.innerHTML = '<div class="sun-glow"></div>';
  } else {
    sun.style.cssText = 'position:fixed;z-index:2;pointer-events:none;';
    sun.innerHTML = '';
  }
}

function setupClouds(heavy) {
  const layer = document.getElementById('cloudLayer');
  layer.innerHTML = '';
  for (let i = 0; i < (heavy ? 8 : 4); i++) {
    const el = document.createElement('div');
    el.className = 'cloud';
    const w = 100 + Math.random() * 200, h = 30 + Math.random() * 40;
    const dur = 20 + Math.random() * 40, op = heavy ? 0.55 : 0.25;
    el.style.cssText = `width:${w}px;height:${h}px;top:${Math.random()*180}px;background:rgba(200,210,230,${op});animation-duration:${dur}s;animation-delay:${-Math.random()*dur}s;opacity:${op}`;
    layer.appendChild(el);
  }
}

function setupRain(heavy) {
  const layer = document.getElementById('rainLayer');
  layer.innerHTML = '';
  for (let i = 0; i < (heavy ? 80 : 40); i++) {
    const el = document.createElement('div');
    el.className = 'raindrop';
    const dur = 0.6 + Math.random() * 0.8, op = heavy ? 0.6 : 0.35;
    el.style.cssText = `height:${heavy ? 18 : 10}px;left:${Math.random()*100}%;top:${Math.random()*100}%;background:rgba(180,210,255,${op});animation-duration:${dur}s;animation-delay:${-Math.random()*dur}s;opacity:${op}`;
    layer.appendChild(el);
  }
}

function setupSnow() {
  const layer = document.getElementById('snowLayer');
  layer.innerHTML = '';
  for (let i = 0; i < 40; i++) {
    const el = document.createElement('div');
    el.className = 'snowflake';
    const dur = 3 + Math.random() * 5;
    el.style.cssText = `left:${Math.random()*100}%;animation-duration:${dur}s;animation-delay:${-Math.random()*dur}s;opacity:.7;font-size:${10+Math.random()*8}px`;
    el.textContent = ['❄','❅','❆','*'][Math.floor(Math.random()*4)];
    layer.appendChild(el);
  }
}

function clearFX() {
  document.querySelectorAll('.cloud,.raindrop,.snowflake').forEach(e => { e.style.opacity = '0'; });
  document.getElementById('stars').style.opacity = '0';
  if (lightningTimer) { clearInterval(lightningTimer); lightningTimer = null; }
}

function applyFX(condition) {
  clearFX();
  const d = (condition || '').toLowerCase();
  const hasRain    = /rain|drizzle/.test(d);
  const hasSnow    = /snow/.test(d);
  const hasClouds  = /cloud|overcast|mist|fog|haze/.test(d) || hasRain || hasSnow;
  const hasThunder = /thunder/.test(d);
  const isClear    = /clear/.test(d);

  if (hasClouds) { setupClouds(/heavy|thunder/.test(d)); document.querySelectorAll('.cloud').forEach(e => { e.style.opacity = ''; }); }
  if (hasRain)   { setupRain(/heavy/.test(d));           document.querySelectorAll('.raindrop').forEach(e => { e.style.opacity = ''; }); }
  if (hasSnow)   { setupSnow(); document.querySelectorAll('.snowflake').forEach(e => { e.style.opacity = ''; }); }
  if (isClear)   { document.getElementById('stars').style.opacity = '0.6'; }
  if (hasThunder) {
    lightningTimer = setInterval(() => {
      const el = document.getElementById('lightning');
      el.classList.add('strike');
      setTimeout(() => el.classList.remove('strike'), 150);
    }, 2500 + Math.random() * 3000);
  }
}

function setUnit(u) {
  unit = u;
  document.getElementById('btnC').classList.toggle('active', u === 'C');
  document.getElementById('btnF').classList.toggle('active', u === 'F');
  fetchWeather();
}

function showBanner(city) {
  document.getElementById('selectedBanner').style.display = 'block';
  document.getElementById('bannerIcon').textContent = city.icon;
  document.getElementById('bannerName').textContent = `${city.name}, ${city.country}`;
  document.getElementById('bannerDesc').textContent = city.desc;
  document.getElementById('bannerTemp').textContent = city.display_temp;
  document.getElementById('bannerStats').innerHTML = `
    <div class="banner-stat"><div class="banner-stat-label">Humidity</div>${city.humidity}%</div>
    <div class="banner-stat"><div class="banner-stat-label">Wind</div>${city.wind} km/h</div>
    <div class="banner-stat"><div class="banner-stat-label">Feels like</div>${city.feels_like}</div>
    <div class="banner-stat"><div class="banner-stat-label">Pressure</div>${city.pressure} hPa</div>
  `;
}

function selectCity(city) {
  selectedCity = city;
  applySkyBg(city.bg);
  applyFX(city.condition);
  showBanner(city);
  renderCards(allCities);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function renderCards(cities) {
  const grid = document.getElementById('cityGrid');
  grid.innerHTML = '';
  document.getElementById('countBadge').textContent = `${cities.length} cities`;
  document.getElementById('loadingMsg').style.display = 'none';

  cities.forEach((city, i) => {
    const card = document.createElement('div');
    card.className = 'city-card' + (selectedCity && selectedCity.name === city.name ? ' active' : '');
    card.style.background = city.gradient;
    card.style.animationDelay = `${(i % 12) * 0.04}s`;
    card.innerHTML = `
      <div class="card-top">
        <div>
          <div class="city-name">${city.name}</div>
          <div class="city-country">${city.country}</div>
        </div>
        <div class="weather-icon-3d" style="animation-delay:${i*.2}s">${city.icon}</div>
      </div>
      <div class="temp-display">${city.display_temp}</div>
      <div class="weather-desc">${city.desc}</div>
      <div class="card-footer">
        <div class="stat-item">💧 ${city.humidity}%</div>
        <div class="stat-item">💨 ${city.wind} km/h</div>
        <div class="stat-item">👁 ${city.visibility}km</div>
      </div>`;
    card.addEventListener('click', () => selectCity(city));
    grid.appendChild(card);
  });
}

async function fetchWeather() {
  const region = document.getElementById('regionFilter').value;
  const search = document.getElementById('searchInput').value;
  const url = `/api/weather?region=${encodeURIComponent(region)}&search=${encodeURIComponent(search)}&unit=${unit}`;

  document.getElementById('errorMsg').style.display = 'none';
  document.getElementById('loadingMsg').style.display = 'block';

  try {
    const res  = await fetch(url);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'API error');
    allCities = data.cities;
    renderCards(allCities);

    if (!selectedCity && allCities.length > 0) {
      selectCity(allCities.find(c => c.name === 'Chennai') || allCities[0]);
    } else if (selectedCity) {
      const updated = allCities.find(c => c.name === selectedCity.name);
      if (updated) { selectedCity = updated; showBanner(updated); }
    }
  } catch (err) {
    document.getElementById('loadingMsg').style.display = 'none';
    const el = document.getElementById('errorMsg');
    el.textContent = `⚠️ ${err.message}`;
    el.style.display = 'block';
  }
}

function debounce(fn, delay) {
  return () => { clearTimeout(debounceTimer); debounceTimer = setTimeout(fn, delay); };
}

document.addEventListener('DOMContentLoaded', () => {
  setupStars();
  applySkyBg(['#1a2a50','#2d4a8a','#3a5fa0']);
  document.getElementById('searchInput').addEventListener('input', debounce(fetchWeather, 400));
  document.getElementById('regionFilter').addEventListener('change', fetchWeather);
  fetchWeather();
});
