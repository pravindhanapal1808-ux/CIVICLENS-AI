# 🚨 CIVICLENS AI

## See a problem. Understand it. Solve it.

CIVICLENS AI is an AI-powered civic issue reporting and prioritization system that transforms a simple photograph of a civic problem into a structured, location-aware and actionable incident report.

Instead of simply reporting a problem, CIVICLENS AI helps identify the issue, estimate its severity and impact, prioritize it, and recommend an appropriate authority action.

---

## 🎯 Problem

Civic problems such as:

- 🕳️ Potholes
- 🗑️ Garbage accumulation
- 🌳 Fallen trees
- 💡 Broken streetlights
- 🛣️ Road problems

are often reported through unstructured channels.

This can make it difficult to:

- Identify the exact problem
- Understand its urgency
- Locate the incident
- Prioritize multiple reports
- Assign the appropriate authority
- Maintain structured incident records

---

## 💡 Our Solution

CIVICLENS AI creates an intelligent workflow:

📸 Image  
↓  
🤖 AI Image Analysis  
↓  
🔎 Civic Issue Identification  
↓  
📍 GPS Location  
↓  
🌐 Address Detection  
↓  
⚠️ Severity Assessment  
↓  
📊 Impact Score  
↓  
🧠 Smart Priority Engine  
↓  
🏛️ Authority Action  
↓  
💾 SQLite Storage  
↓  
📊 Dashboard + 🗺️ Map  
↓  
📄 Incident Report

---

# ✨ Key Features

### 🤖 AI-Powered Image Analysis

Uses the open-source BLIP image-captioning model to analyze uploaded civic issue images.

### 📍 GPS-Based Location

Captures the user's geographic coordinates through browser location services.

### 🌐 Address Detection

Uses OpenStreetMap Nominatim reverse geocoding to convert coordinates into a readable address.

### ⚠️ Severity Assessment

The system categorizes detected civic issues into severity levels such as:

- HIGH
- MEDIUM
- LOW

### 📊 Impact Scoring

Each incident receives an estimated impact score used by the priority engine.

### 🧠 Smart Priority Engine

Combines severity and impact to generate:

- 🚨 CRITICAL
- 🔴 HIGH
- 🟡 MEDIUM
- 🟢 LOW

### 🏛️ Authority Action Center

Maps civic issues to relevant departments and provides recommended actions.

### 🗺️ Civic Map

Displays location-aware civic incidents on a map.

### 🔎 Search & Filtering

Reports can be searched and filtered by:

- Report ID
- Issue
- Description
- Location
- Priority
- Severity
- Department
- GPS availability

### 📄 Incident Reports

Generates downloadable incident reports containing important information about each civic issue.

### 💾 Local Database

Uses SQLite to store civic incident records.

---

# 🏗️ System Architecture

```text
                 CIVICLENS AI
                      │
                      ▼
              📸 Image Upload
                      │
                      ▼
             🤖 BLIP AI Model
                      │
                      ▼
             Civic Issue Analysis
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     📍 GPS Data              AI Description
          │                       │
          ▼                       ▼
   Nominatim API            Issue Classification
          │                       │
          └───────────┬───────────┘
                      ▼
              ⚠️ Severity Engine
                      │
                      ▼
                📊 Impact Score
                      │
                      ▼
             🧠 Priority Engine
                      │
                      ▼
             🏛️ Authority Action
                      │
                      ▼
                💾 SQLite DB
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      📊 Dashboard  🗺️ Map   📄 Reports