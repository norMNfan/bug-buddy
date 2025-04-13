# bug-buddy 🐛🔍

**Bud Buddy** is a web application that leverages AI to automatically detect, analyze, and fix errors in your applications. The app connects to your applications logs to fetch error logs, pulls your code from GitHub, analyzes the issue, and creates GitHub issues with proposed fixes.

## Features
- 🔄 Automatic error detection from AWS CloudWatch logs
- 📂 Code analysis from your GitHub repositories
- 🤖 AI-powered (Portia) error diagnosis and fix generation
- 🚀 Automated GitHub issue creation with detailed fix proposals
- 📊 Dashboard to track and manage your code repositories
- 🔍 Interactive UI for reviewing AI-suggested fixes

## Development

### Prerequisities
- Docker and Docker Compose
- Node.js and Yarn
- Github account and personal access token
- AWS credentials and CloudWatch access
- Portia and Anthropic API keys

### Environment Setup

First, add the necessary `.env` files for the external dependencies for the frontend and backend

`/frontend/.env`
```
SUPABASE_URL=
SUPABASE_ANON_KEY=

AUTH_TRUST_HOST=true
AUTH_SECRET=

GITHUB_USERNAME=
GITHUB_TOKEN=
```

`/backend/.env`
```
export PORTIA_API_KEY=
export ANTHROPIC_API_KEY=

export AWS_ACCESS_KEY=
export AWS_SECRET=
export AWS_REGION=

export GITHUB_TOKEN=
export GITHUB_USERNAME=
export GITHUB_REPO=
```

### Installing and Running
Install the frontend dependencies:

```
cd frontend
yarn install
```

Build and start the application using Docker:
```
docker-compose up --build
```

## How It Works
1. 📡 Log Collection: Bug Buddy connects to AWS CloudWatch and monitors your logs for errors
2. 🧩 Code Analysis: When an error is detected, Bug Buddy fetches the relevant code from your GitHub repository
3. 🧠 AI Analysis (Portia): The AI agent analyzes the error and code to determine the root cause
4. 📝 Fix Generation: The AI generates a potential fix for the issue
5. 🎫 Issue Creation: Bug Buddy creates a GitHub issue with details about the error and the proposed fix
6. 👀 Review & Implement: You can review the issue and implement the suggested fix

## User Workflow
1. **Connect** your AWS and Github account
Clicking 'Sign in with GitHub' will redirect you to a GitHub page requesting you to authorize Bug Buddy to make actions to GitHub on your behalf.
<img src="https://github.com/norMNfan/bug-buddy/blob/main/images/step1.png" width="100%" alt="Connect to GitHub">

2. **Configure**: Setup your repositories and log groups to monitor
<img src="https://github.com/norMNfan/bug-buddy/blob/main/images/step2.png" width="100%" alt="Connect to GitHub">

3. **Analyze**: Start the analysis process with a single click
<img src="https://github.com/norMNfan/bug-buddy/blob/main/images/step3.png" width="100%" alt="Connect to GitHub">

4. **Review**: Examine the AI-generated diagnosis and proposed fixes
<img src="https://github.com/norMNfan/bug-buddy/blob/main/images/step4.png" width="100%" alt="Connect to GitHub">

5. **Approve**: Choose to implement the suggested fix
<img src="https://github.com/norMNfan/bug-buddy/blob/main/images/step5.png" width="100%" alt="Connect to GitHub">

6. **Issue Creation**: The Issue will be created in Github
<img src="https://github.com/norMNfan/bug-buddy/blob/main/images/step6.png" width="100%" alt="Connect to GitHub">

7. **Pull Request Creation**: The Pull Request will be created in GitHub
<img src="https://github.com/norMNfan/bug-buddy/blob/main/images/pull-request.pdf" width="100%" alt="Connect to GitHub">

## Tech Stack

<div style="display: flex; align-items: center; gap: 10px;">
  <span><strong>Frontend</strong>: Astro + React + Supabase</span>
  <img src="https://github.com/norMNfan/bug-buddy/blob/main/images/astro-logo.png" alt="Astro Logo" style="width: 30px; height: 30px;">
  <img src="https://github.com/norMNfan/bug-buddy/blob/main/images/react-logo.png" alt="React Logo" style="width: 30px; height: 30px;">
  <img src="https://github.com/norMNfan/bug-buddy/blob/main/images/supabase-logo.jpeg" alt="Supabase Logo" style="width: 30px; height: 30px;">
</div>

<div style="display: flex; align-items: center; gap: 10px;">
  <span><strong>Backend</strong>: Python + FastAPI</span>
  <img src="https://github.com/norMNfan/bug-buddy/blob/main/images/python-logo.jpeg" alt="Python Logo" style="width: 30px; height: 30px;">
  <img src="https://github.com/norMNfan/bug-buddy/blob/main/images/fastapi-logo.png" alt="FastAPI Logo" style="width: 30px; height: 30px;">
</div>

<div style="display: flex; align-items: center; gap: 10px;">
  <span><strong>Containerization</strong>: Docker</span>
  <img src="https://github.com/norMNfan/bug-buddy/blob/main/images/docker-logo.png" alt="Docker Logo" style="width: 30px; height: 30px;">
</div>

<div style="display: flex; align-items: center; gap: 10px;">
  <span><strong>AI Agent</strong>: Portia</span>
  <img src="https://github.com/norMNfan/bug-buddy/blob/main/images/portia-logo.jpeg" alt="Portia Logo" style="width: 30px; height: 30px;">
</div>


## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Contact
If you have any questions or feedback, please open an issue on this repository.