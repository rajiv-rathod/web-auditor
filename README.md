# Web Auditor 🛡️

A comprehensive cybersecurity auditing platform that integrates 50+ open-source security tools into a unified web interface. Built with FastAPI backend and Next.js frontend for professional-grade security testing.

![Homepage](https://github.com/user-attachments/assets/b3310481-1add-46ac-b5b0-d642374cc085)

## ✨ Key Features

### 🔍 Reconnaissance & Footprinting
- **Subdomain Enumeration**: Find subdomains using multiple tools (Subfinder, Assetfinder, etc.)
- **DNS Lookup**: Comprehensive DNS record analysis (A, AAAA, MX, NS, TXT, etc.)
- **Port Scanning**: Network service discovery using Nmap
- **Technology Detection**: Identify web technologies and frameworks
- **WHOIS Information**: Domain registration and ownership details

### 🛡️ Web Application Vulnerability Testing
- **SQL Injection**: Automated SQLi detection using SQLMap
- **Cross-Site Scripting (XSS)**: XSS vulnerability scanning
- **Directory Bruteforce**: Hidden file and directory discovery
- **CMS Security**: WordPress, Joomla, Drupal security scanning
- **File Upload Testing**: File upload vulnerability assessment
- **Authentication Testing**: Login bypass and brute force testing

### 🔑 NPM Security Analysis
![NPM Security](https://github.com/user-attachments/assets/45c68342-9ac0-4753-9a6c-e8df316c1bc3)

- **Security Audits**: Comprehensive NPM package vulnerability scanning
- **Dependency Analysis**: Check dependencies for known vulnerabilities
- **License Compliance**: Scan for license compliance and risks
- **Outdated Packages**: Identify packages that need updates
- **Package Information**: Detailed metadata and security info

### 🔐 Password & Authentication Security
- **Password Strength Analysis**: Advanced password complexity evaluation
- **Hash Analysis**: Check for compromised passwords in breaches
- **SSL Certificate Validation**: Certificate security assessment
- **Email Security**: SPF, DMARC, DKIM validation

### 📊 Professional Reporting
- **PDF Reports**: Professional security assessment reports
- **HTML Reports**: Interactive web-based reports
- **JSON/CSV Export**: Machine-readable data formats
- **Real-time Results**: Live scan progress and updates

### ⚡ Enterprise Features
- **User Authentication**: Secure user management system
- **API Integration**: RESTful API for automation (30+ endpoints)
- **Rate Limiting**: Configurable request throttling
- **Multi-threading**: Parallel scan execution
- **Database Integration**: SQLite/PostgreSQL support

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

## 🚀 Quick Start

### Method 1: Development Setup (Recommended)

#### Prerequisites
- **Python 3.11+** with pip
- **Node.js 18+** with npm
- **Git**

#### Installation Steps

1. **Clone and Setup Backend**:
```bash
git clone https://github.com/rajiv-rathod/web-auditor.git
cd web-auditor

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
```

2. **Start Backend Server**:
```bash
python -m app.main
```
Backend available at: **http://localhost:8000**

3. **Setup Frontend** (New Terminal):
```bash
cd frontend
npm install
npm run dev
```
Frontend available at: **http://localhost:3000**

4. **Verify Installation**:
```bash
# Run comprehensive test suite
python test_comprehensive.py
# Expected: 100% success rate (17/17 tests passing)
```

### Method 2: Docker Setup

```bash
# Copy environment configuration
cp .env.example .env

# Start all services
docker-compose up -d
```

**Access Points:**
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000  
- **API Documentation**: http://localhost:8000/docs

### ✅ Verification

![Login Page](https://github.com/user-attachments/assets/b3310481-1add-46ac-b5b0-d642374cc085)

1. Navigate to http://localhost:3000
2. Create an account using the registration form
3. Access NPM Security features for comprehensive package analysis
4. Run the test suite to ensure 100% functionality

📖 **For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**
🧪 **For testing procedures, see [TESTING_GUIDE.md](TESTING_GUIDE.md)**
4. Start Celery worker:
```bash
celery -A app.core.celery worker --loglevel=info
```

## 🧪 Testing & Quality Assurance

### Automated Test Suite
```bash
# Run comprehensive test suite
python test_comprehensive.py
```

**Test Coverage:**
- ✅ Backend health checks (API, database, services)
- ✅ Frontend page loading and navigation  
- ✅ User authentication flow (register, login, profile)
- ✅ NPM security features (audit, dependency check, licensing)
- ✅ Security tools (password analysis, SSL check, email validation)
- ✅ Error handling and edge cases

**Expected Result**: 100% success rate (17/17 tests passing)

### Manual Testing Checklist
- [ ] User registration and login functionality
- [ ] NPM package security analysis
- [ ] Frontend form validation and error handling
- [ ] API endpoint responses and authentication
- [ ] Database operations and data persistence

📖 **For detailed testing procedures, see [TESTING_GUIDE.md](TESTING_GUIDE.md)**

## 🔧 Usage Guide

### Quick Security Analysis

![NPM Security Analysis](https://github.com/user-attachments/assets/45c68342-9ac0-4753-9a6c-e8df316c1bc3)

1. **Register/Login** to the platform
2. **Navigate** to NPM Security section
3. **Upload** package.json or enter package names
4. **Select** analysis type (audit, dependencies, licenses)
5. **Review** security findings and recommendations
6. **Generate** comprehensive reports

### Advanced Features
- **Real-time Scanning**: Live progress monitoring
- **Comprehensive Reports**: PDF/HTML/JSON export formats
- **API Integration**: REST API for automation (30+ endpoints)
- **Multi-user Support**: Team collaboration features

## 🛠️ API Documentation

The platform provides a comprehensive REST API for automation and integration.

**Access Interactive Documentation**: http://localhost:8000/docs

### Key Endpoints
- `/api/auth/` - Authentication and user management
- `/api/npm/` - NPM security analysis tools
- `/api/security/` - General security assessment tools
- `/api/recon/` - Reconnaissance and information gathering
- `/api/scans/` - Scan management and results

## 🔒 Security Tools Integrated

### NPM Security Analysis
- **NPM Audit**: Official npm audit for vulnerability detection
- **Dependency Check**: OWASP dependency check integration
- **License Scanner**: License compliance and risk assessment
- **Package Info**: Detailed package metadata and security info

### General Security Tools
- **Password Analysis**: Advanced password strength evaluation
- **SSL Certificate Check**: Certificate security validation
- **Email Security**: SPF, DMARC, DKIM record validation
- **Hash Analysis**: Breach detection for password hashes

### Reconnaissance Tools
- **DNS Lookup**: Comprehensive DNS record analysis
- **Subdomain Discovery**: Multiple tool integration
- **Port Scanning**: Network service discovery
- **WHOIS Information**: Domain registration details

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