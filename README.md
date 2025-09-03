# Web Auditor

A comprehensive web security auditing platform that integrates multiple open-source security tools into a unified interface.

## Features

### 🔍 Recon & Footprinting
- **Subdomain Enumeration**: subfinder, amass, sublist3r integration
- **DNS & WHOIS Lookup**: Comprehensive domain information gathering
- **Port Scanning**: nmap and masscan integration with service detection
- **Tech Stack Fingerprinting**: Technology detection and version identification
- **Email & Metadata Harvesting**: Information gathering from public sources

### 🛡️ Web App Vulnerability Testing
- **SQL Injection**: sqlmap integration for comprehensive SQL injection testing
- **XSS Detection**: Multiple payload testing for reflected, stored, and DOM XSS
- **Directory Bruteforce**: Hidden path and file discovery
- **File Upload Testing**: Upload bypass vulnerability detection
- **Authentication Testing**: Session management and JWT security analysis
- **CMS Security**: WordPress, Drupal, and Joomla specific scans

### 🔑 Password Attacks
- **Bruteforce/Dictionary**: hydra and medusa integration
- **Hash Cracking**: hashcat and john the ripper support
- **Wordlist Generation**: Custom wordlist creation

### 🕵️ Exploitation
- **Metasploit Integration**: Framework integration for exploitation
- **Payload Generation**: msfvenom payload creation
- **Exploit Database**: searchsploit and CVE search

### 🎭 Social Engineering
- **Phishing Page Generator**: Template-based phishing campaigns
- **QR Code Exploits**: Malicious QR code generation

### 🐍 Post Exploitation
- **Privilege Escalation**: LinPEAS and winPEAS integration
- **Credential Dumping**: pypykatz for Windows credential extraction
- **Lateral Movement**: impacket suite tools

### 📊 Reporting
- **Auto Report Generator**: PDF and HTML report generation
- **Collaboration Mode**: Real-time team collaboration features

### ⚡ Advanced Features
- **Cloud Security**: AWS, Azure, GCP misconfiguration scanning
- **Container Security**: Docker and Kubernetes security assessment
- **Dark Web Search**: Credential leak detection
- **AI Assistant**: LLM-powered vulnerability explanation and recommendations

## Architecture

- **Backend**: Python FastAPI with async support
- **Job Queue**: Celery with Redis for background task processing
- **Frontend**: React/Next.js with TypeScript
- **Database**: PostgreSQL for data persistence
- **Execution**: Docker containers for tool isolation and security
- **Authentication**: JWT-based user authentication

## Installation

### Prerequisites
- Docker and Docker Compose
- Git

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/rajiv-rathod/web-auditor.git
cd web-auditor
```

2. Copy environment configuration:
```bash
cp .env.example .env
```

3. Start the platform:
```bash
docker-compose up -d
```

4. Access the application:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Installation

1. Backend setup:
```bash
cd app
pip install -r requirements.txt
uvicorn main:app --reload
```

2. Frontend setup:
```bash
cd frontend
npm install
npm run dev
```

3. Start Redis and PostgreSQL services
4. Start Celery worker:
```bash
celery -A app.core.celery worker --loglevel=info
```

## Usage

### Quick Security Scan

1. Register/Login to the platform
2. Navigate to Reconnaissance section
3. Enter target domain or IP
4. Select scan types
5. Monitor results in real-time
6. Generate comprehensive reports

### Advanced Usage

- **Custom Scans**: Configure specific tools and parameters
- **Scheduled Scans**: Set up automated recurring scans
- **Team Collaboration**: Share scans and results with team members
- **API Integration**: Use REST API for automation and integration

## Security Tools Integrated

### Reconnaissance
- subfinder
- amass
- sublist3r
- nmap
- masscan
- dnsenum
- dig
- whois
- WhatWeb
- theHarvester

### Vulnerability Assessment
- sqlmap
- XSStrike
- dalfox
- dirsearch
- gobuster
- wpscan
- droopescan
- joomscan

### Exploitation
- Metasploit Framework
- msfvenom
- searchsploit

### Password Attacks
- hydra
- medusa
- hashcat
- john the ripper
- crunch
- cewl

### Post Exploitation
- LinPEAS
- winPEAS
- pypykatz
- impacket

## API Documentation

The platform provides a comprehensive REST API for automation and integration. 

Access the interactive API documentation at: http://localhost:8000/docs

### Key Endpoints

- `/api/auth/` - Authentication and user management
- `/api/scans/` - Scan management and results
- `/api/recon/` - Reconnaissance tools
- `/api/vulnerability/` - Vulnerability testing tools
- `/api/reports/` - Report generation

## Configuration

### Environment Variables

Key configuration options in `.env`:

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - JWT signing key
- `DEHASHED_API_KEY` - API key for breach data
- `VIRUSTOTAL_API_KEY` - VirusTotal API integration

### Docker Configuration

The platform uses Docker Compose for orchestration:

- `web` - FastAPI backend service
- `db` - PostgreSQL database
- `redis` - Redis for job queue
- `celery` - Background task worker
- `frontend` - Next.js frontend
- `nmap` - Nmap scanning container
- `sqlmap` - SQLMap container

## Development

### Project Structure

```
web-auditor/
├── app/                    # Backend application
│   ├── api/               # API endpoints
│   ├── core/              # Core configuration
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
├── frontend/              # Frontend application
│   ├── pages/             # Next.js pages
│   ├── components/        # React components
│   ├── lib/               # API client
│   └── styles/            # CSS styles
├── tools/                 # Security tool containers
└── docker-compose.yml     # Service orchestration
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

### Testing

Run the test suite:

```bash
# Backend tests
pytest app/tests/

# Frontend tests
npm test
```

## Security Considerations

- All tools run in isolated Docker containers
- Rate limiting implemented for API endpoints
- Input validation and sanitization
- Secure JWT token handling
- Database query protection
- CORS configuration for frontend security

## Legal Notice

This tool is for authorized security testing only. Users are responsible for ensuring they have proper authorization before scanning any systems. Unauthorized access to computer systems is illegal.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the API documentation

## Roadmap

- [ ] Additional security tool integrations
- [ ] Machine learning for vulnerability prioritization
- [ ] Mobile application security testing
- [ ] Cloud-native security scanning
- [ ] Integration with SIEM systems
- [ ] Advanced threat intelligence feeds
- [ ] Custom rule engine for vulnerabilities
- [ ] Multi-tenant support for enterprises