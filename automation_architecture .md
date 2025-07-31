# 🌍 Countries Project Automation Architecture

---

## 📐 Overview
This document outlines the fully automated workflow for the **Countries Project**, covers CI/CD, containerization, scheduling, error handling.

---


## 🚀 Workflow Automation
1. **Code Commit & Validation**  
   - Push to GitHub; PRs trigger: linting, type checks, unit tests (`pytest`).  
   - Merge only on pass and peer approval.

2. **Build & Publish Containers**  
   - GitHub Actions builds Docker images (multi-stage) for backend and ETL agents.
3. **ETL Orchestration**  
   - Prefect server (in Docker) hosts flows.  
   - Prefect agents execute flows:  
     - **Daily full refresh** at 01:00 UTC.  
     - **Manual trigger** via Prefect UI/API.

4. **Scheduled Backups**  
   - GitHub Actions scheduled workflow runs nightly at 02:00 UTC to dump PostgreSQL and upload to S3.  
   - Retains the last 7 backup archives.

---

## ⏱ Execution Frequencies
- **Event-driven**: CI and container builds on every push/PR.  
- **Nightly**: ETL full refresh at 01:00 UTC; DB backup at 02:00 UTC.  
- **Manual**: Deploys ETL via UI/API.

---

## ⚠️ Error Handling & Recovery
- **Flow Retries**: Prefect configured with 3 retries and exponential backoff.  
- **Centralized Logs**: Services emit JSON logs for analysis.  
- **Failure Notifications**: Prefect alerts on flow failures via email hooks.

---

## 📈 Scalability & Optimization
- **Horizontal Scaling**: Add Linux hosts and run additional Docker containers or Prefect agents.  
- **Multi-Stage Builds**: Optimized Docker images for faster CI.  
- **Caching**: Use MongoDB for any intermediate state caching.  
- **Resource Limits**: Define CPU and memory constraints in Compose to prevent overload.  
- **Data Lifecycle**: Upload data files to S3 to follow up on changes and analyze when needed.

---
