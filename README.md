
# 💼 Resume_JD_Agent

> An AI-powered web application that helps users compare their resumes with job descriptions and provides personalized feedback, scoring, and optimization tips.

---

## 📌 Overview

Resume_JD_Agent is designed to bridge the gap between job seekers and job requirements using powerful AI analysis. Upload a resume, paste a job description, and instantly get insights, alignment scores, and improvement tips — all through an intuitive UI powered by a modern backend and LLM (Large Language Model) integration.

---

## 🧠 Features

- ✅ Upload Resume (PDF/Text)
- ✅ Paste or Upload Job Description
- ✅ Get Match Score & Compatibility Report
- ✅ Personalized Tips to Improve Resume
- ✅ Multilingual UI (Planned)
- ✅ Secure Authentication (Planned)
- ✅ File Uploads with Cloud Storage (Planned)
- ✅ Visual Feedback Charts (Planned)

---

## 🏗️ System Architecture

The application follows a modular architecture with clearly separated concerns.

### High-Level Architecture

```
User Browser --> UI (React/HTML) --> API/Backend (Flask) --> LLM Engine (OpenAI) --> Response
                                                           |
                                                           ---> Database (MongoDB / PostgreSQL)
                                                           ---> File Storage (S3 / Local)
```

- **Frontend:** React-based UI (or HTML+JS) to handle forms and results.
- **Backend/API:** Flask/Python REST API for request handling, auth, and AI orchestration.
- **AI Agent:** Module to interact with OpenAI's GPT model, format prompts, and analyze content.
- **Database:** MongoDB or PostgreSQL for storing users, resumes, job descriptions, and reports.
- **File Storage:** Secure storage for resume files, integrated with cloud providers.

---

## 🔍 Core Components

| Component         | Responsibility |
|------------------|----------------|
| **Frontend UI**  | Resume/JD input, display feedback, multilingual UI |
| **API Server**   | Auth, orchestrate AI logic, interface with DB & storage |
| **AI Module**    | Use GPT to compare and score resumes vs JD |
| **Database**     | Store users, documents, scores, tips |
| **Auth Service** | JWT or OAuth-based planned authentication |
| **Storage Layer**| Cloud/local file storage for resumes & cover letters |

---

## 🧩 UML Diagrams

All architecture and flow diagrams have been designed in `.drawio` format and exported to PNG for easy reference.

- ✅ Component Diagram  
- ✅ Class Diagram  
- ✅ Deployment Diagram  
- ✅ Use Case Diagram  
- ✅ Activity Flow Diagram  
- ✅ System Architecture Diagram  
- ✅ Requirement Diagram  
- ✅ Data Flow Diagram  

📁 View diagrams in the [`/diagrams`](./diagrams) folder.

---

## 🚀 Deployment

The system can be deployed locally using Docker or manually with Python + Node.js. Here's a quick start guide.

### Prerequisites

- Python 3.10+
- Node.js & npm
- MongoDB or PostgreSQL
- OpenAI API Key

### Local Setup

```bash
# Clone the repo
git clone https://github.com/yourname/resume-jd-agent.git
cd resume-jd-agent


# Set up backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

# Set up frontend
cd ../frontend
npm install
npm run start
```

setup .env file

```bash
MISTRAL_API_KEY=""
DATABASE_URL=""
DISCORD_WEBHOOK_URL=""
DISCORD_CHANNEL_ID=""
DISCORD_SERVER_ID=""

```

---

## 📂 Project Structure

```
resume-jd-agent/
├── backend/
│   ├── app.py
│   ├── agent_logic/
│   └── models/
├── frontend/
│   ├── public/
│   └── src/
├── diagrams/
│   └── *.drawio
├── .env.example
├── README.md
```

---

## 💡 Future Plans

- 📘 Resume version tracking
- 🧠 AI resume builder
- 🌐 Multilingual support
- 🔒 OAuth2 Authentication
- 📊 Graphical scoring dashboard
- ☁️ Full cloud-native deployment (AWS/GCP)


---

> *“Helping every resume find the right job — powered by AI.”*
