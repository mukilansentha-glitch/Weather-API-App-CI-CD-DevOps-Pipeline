# 🌍 World Weather App — Jenkins CI/CD Pipeline

Python Flask weather app using **OpenWeatherMap API**, with a full Jenkins pipeline including SonarQube quality gate and Docker deployment.

---

## Project Structure

```
weather-pipeline/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # API endpoints
│   └── weather.py           # OpenWeatherMap logic
├── static/
│   ├── css/style.css        # 3D atmospheric UI
│   └── js/app.js            # Frontend JS
├── templates/index.html     # Main UI
├── tests/
│   └── test_weather.py      # 40+ tests (mocked API)
├── Dockerfile
├── docker-compose.yml       # App + Jenkins + SonarQube
├── Jenkinsfile              # 8-stage pipeline
├── requirements.txt
├── setup.cfg                # pytest + flake8 config
└── sonar-project.properties
```

---

## Step 1 — Get OpenWeatherMap API Key

1. Go to https://openweathermap.org/api and sign up (free)
2. My API Keys → copy your key
3. Free tier supports 60 calls/minute — enough for this app

---

## Step 2 — Local Run

```bash
git clone https://github.com/YOUR_USERNAME/world-weather-app.git
cd world-weather-app

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

export OPENWEATHER_API_KEY=your_key_here
python run.py
# Open http://localhost:5000
```

---

## Step 3 — Run Tests

```bash
pytest
# Coverage report → htmlcov/index.html
# Must be ≥ 80% to pass
```

---

## Step 4 — Push to GitHub

```bash
git init
git add .
git commit -m "feat: World Weather App with Jenkins pipeline"
git remote add origin https://github.com/YOUR_USERNAME/world-weather-app.git
git push -u origin main
```

---

## Step 5 — Jenkins + SonarQube Setup

### Start services

```bash
docker-compose up -d
```

| Service    | URL                      | Credentials   |
|------------|--------------------------|---------------|
| Jenkins    | http://localhost:8080    | (wizard)      |
| SonarQube  | http://localhost:9000    | admin / admin |
| Weather App| http://localhost:5000    | —             |

### Jenkins configuration

**Install plugins:**
- SonarQube Scanner
- Pipeline
- Git
- Credentials Binding
- HTML Publisher
- JUnit

**Add credentials** (Manage Jenkins → Credentials → Global → Add):

| ID                   | Type        | Value                          |
|----------------------|-------------|--------------------------------|
| `sonar-token`        | Secret text | Token from SonarQube → My Account → Security |
| `openweather-api-key`| Secret text | Your OpenWeatherMap API key    |

**Configure SonarQube** (Manage Jenkins → Configure System → SonarQube servers):
- Name: `SonarQube`
- URL: `http://sonarqube:9000`

**Install sonar-scanner on Jenkins agent:**
```bash
docker exec -it jenkins bash
wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-6.1.0.4477-linux-x64.zip
unzip sonar-scanner-cli-*.zip -d /opt/
export PATH=$PATH:/opt/sonar-scanner-6.1.0.4477-linux-x64/bin
```

**Add SonarQube webhook** (SonarQube → Administration → Webhooks → Create):
- Name: Jenkins
- URL: `http://jenkins:8080/sonarqube-webhook/`

### Create Pipeline job

1. New Item → Pipeline
2. Pipeline → Definition: **Pipeline script from SCM**
3. SCM: Git → your GitHub repo URL
4. Script Path: `Jenkinsfile`
5. Save → **Build Now**

---

## Pipeline Stages

| # | Stage            | What happens                              |
|---|------------------|-------------------------------------------|
| 1 | Checkout         | Clone from GitHub                         |
| 2 | Install          | Create virtualenv, install requirements   |
| 3 | Lint             | flake8 code style check                   |
| 4 | Test & Coverage  | pytest + JUnit report + HTML coverage     |
| 5 | SonarQube        | Send metrics to SonarQube                 |
| 6 | Quality Gate     | Block pipeline if gate fails              |
| 7 | Docker Build     | Build & tag Docker image                  |
| 8 | Deploy           | Run container on port 5000                |

---

## API Endpoints

```
GET /                          → Weather UI
GET /api/weather               → All cities (?region=india&search=mum&unit=C)
GET /api/weather/<city_name>   → Single city (?unit=F)
GET /health                    → Health check
```
