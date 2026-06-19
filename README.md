# EcoTrack AI: Personal Carbon Footprint Advisor 🌍⚡

An advanced, context-aware digital application built for Main Challenge 3 of PromptWars 2026 (in collaboration with Google for Developers). EcoTrack AI enables individuals to dynamically calculate, analyze, and systematically reduce their daily environmental footprint using generative artificial intelligence.

## 🔗 Live Deployments
* Live Application URL: https://ecotrack-carbon-platform-765144110696.us-central1.run.app/
* Source Code Repository: https://github.com/era651868-ctrl/EcoTrack-ai
* Developer Organization: Hack2skill PromptWars 2026

---

## 🚀 Key Features

* Real-time Footprint Calculator: Processes inputs across core carbon sectors (Commutes & Transport, Grid Utility Energy, and Dietary Vectors) to map an instantaneous carbon baseline.
* Gemini 2.5 Intelligence Engine: Integrates deep semantic modeling to process user footprint telemetry and generate hyper-localized structural mitigation strategies.
* Context-Aware Constraints: Factors in geographical profile bounds (e.g., target carbon ceilings and regional operational zones) to tailor recommendations that fit safe lifestyle limits.
* Dynamic Visualization: Live tracking interface built with reactive data components to log environmental overhead over time.

---

## 🛠️ Technical Architecture & Stack

The application leverages a containerized serverless layout engineered for zero-downtime scaling and modern credential standards:

* Core Runtime: Python 3.10
* Frontend UI Framework: Streamlit (Reactive Web Wrapper)
* Generative Model SDK: Google GenAI SDK (google-genai)
* AI Orchestration Engine: Gemini 2.5 Flash
* Containerization & Hosting: Google Cloud Build & Google Cloud Run (Serverless Microservices)
* Security & Authentication: Google Cloud IAM & Service-Bound Google AI Studio Auth Keys

---

## ⚙️ Environment Configuration

To replicate or run this system locally, the following target variables must be configured in your workspace environment:

GEMINI_API_KEY="your_google_ai_studio_auth_key"
GO_PYTHON_VERSION="3.10"

### Installation & Local Setup Instructions

Follow these commands in your terminal to set up and execute the project locally:

1. Clone the repository:
   git clone https://github.com/era651868-ctrl/EcoTrack-ai.git
   cd EcoTrack-ai

2. Install core project dependencies:
   pip install -r requirements.txt

3. Initialize the local runtime server:
   streamlit run app.py

---

## 🏆 Project Insights & Submission Notes

This platform was built and optimized to meet Google's latest security guidelines, shifting completely away from unrestricted standard keys to bound secure authorization pathways. Built end-to-end to ensure carbon tracking is accessible, automated, and contextually precise.

Developed with passion for PromptWars 2026. 🚀
