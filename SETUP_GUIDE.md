# Web Auditor - Complete Setup and Usage Guide 🛡️

## Overview

Web Auditor is a comprehensive cybersecurity auditing platform that integrates 50+ open-source security tools into a unified web interface. This guide provides step-by-step instructions for setup, usage, and testing.

![Homepage](https://github.com/user-attachments/assets/b3310481-1add-46ac-b5b0-d642374cc085)

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** with pip
- **Node.js 18+** with npm
- **Git**
- **Optional**: Docker and Docker Compose for containerized deployment

### Method 1: Development Setup (Recommended for Testing)

#### 1. Clone and Setup Backend
```bash
# Clone the repository
git clone https://github.com/rajiv-rathod/web-auditor.git
cd web-auditor

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Setup environment configuration
cp .env.example .env
# Edit .env file - defaults to SQLite which works out of the box
```

#### 2. Start Backend Server
```bash
# From the web-auditor directory with venv activated
python -m app.main
```
The backend will start at: **http://localhost:8000**

#### 3. Setup Frontend (New Terminal)
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```
The frontend will start at: **http://localhost:3000**

#### 4. Verify Installation
Run the comprehensive test suite:
```bash
# From the main directory with venv activated
python test_comprehensive.py
```

You should see **100% success rate** with all 17 tests passing.

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

## 📋 Step-by-Step Usage Guide

### 1. User Registration & Authentication

![Register Page](https://github.com/user-attachments/assets/fcf9cf39-4b66-48ae-b663-e2ba7e15495b)

1. **Navigate** to http://localhost:3000/register
2. **Fill out** the registration form:
   - Username (unique)
   - Email address
   - Password (8+ characters recommended)
   - Confirm password
3. **Click** "Create account"
4. **Sign in** at http://localhost:3000/login with your credentials

![Login Page](https://github.com/user-attachments/assets/b3310481-1add-46ac-b5b0-d642374cc085)

### 2. NPM Security Analysis

![NPM Security Page](https://github.com/user-attachments/assets/45c68342-9ac0-4753-9a6c-e8df316c1bc3)

The NPM Security module provides comprehensive security analysis for Node.js packages:

#### Security Audit
1. **Navigate** to the NPM Security page
2. **Paste** your package.json content in the text area
3. **Click** "Run Security Audit"
4. **Review** vulnerability findings with severity levels

#### Dependency Check
1. **Switch** to "Dependency Check" tab
2. **Enter** package names (one per line)
3. **View** security status for each package

#### License Compliance
1. **Use** "License Scan" tab
2. **Submit** package.json content
3. **Review** license compliance and risk levels

#### Package Information
1. **Select** "Package Info" tab
2. **Enter** package name
3. **Get** detailed package metadata and security info

### 3. Security Testing Features

#### Reconnaissance Tools
- **DNS Lookup**: Domain resolution and record enumeration
- **Subdomain Discovery**: Find subdomains using multiple tools
- **Port Scanning**: Network service discovery
- **WHOIS Information**: Domain registration details

#### Vulnerability Testing
- **SQL Injection**: Automated SQL injection testing
- **XSS Detection**: Cross-site scripting vulnerability scanning
- **Directory Bruteforce**: Hidden file and directory discovery
- **SSL Certificate Analysis**: Certificate security validation

#### Password & Security Analysis
- **Password Strength**: Comprehensive password analysis
- **Email Security**: SPF, DMARC, and MX record validation
- **Hash Analysis**: Check for compromised passwords

## 🧪 Testing & Quality Assurance

### Automated Testing Suite

The platform includes a comprehensive test suite that validates all functionality:

```bash
# Run all tests
python test_comprehensive.py
```

**Test Coverage:**
- ✅ Backend health checks
- ✅ API documentation accessibility  
- ✅ Frontend page loading
- ✅ User authentication flow
- ✅ NPM security features
- ✅ Password strength analysis
- ✅ SSL certificate checking
- ✅ Email security validation

### Manual Testing Checklist

#### Frontend Testing
- [ ] Homepage loads correctly
- [ ] User registration works
- [ ] User login functions
- [ ] NPM Security page is accessible
- [ ] All navigation links work
- [ ] Forms submit properly

#### Backend API Testing
- [ ] Health endpoint responds
- [ ] Authentication endpoints work
- [ ] NPM security endpoints function
- [ ] Security tool endpoints respond
- [ ] Error handling works correctly

#### Integration Testing
- [ ] Frontend-backend communication
- [ ] Authentication token handling
- [ ] File upload functionality
- [ ] Real-time updates work

## 🔧 API Documentation

### Authentication Endpoints
```
POST /api/auth/register    # User registration
POST /api/auth/login       # User login
GET  /api/auth/profile     # Get user profile
```

### NPM Security Endpoints
```
POST /api/npm/npm-audit           # NPM security audit
POST /api/npm/dependency-check    # Check specific dependencies
POST /api/npm/license-scan        # License compliance scan
POST /api/npm/outdated-packages   # Find outdated packages
GET  /api/npm/package-info/{name} # Get package information
```

### Security Tools Endpoints
```
POST /api/security/password-strength  # Analyze password strength
POST /api/security/ssl-check          # SSL certificate analysis
POST /api/security/email-security     # Email security assessment
```

### Reconnaissance Endpoints
```
POST /api/recon/dns-lookup    # DNS record lookup
POST /api/recon/subdomain     # Subdomain enumeration
POST /api/recon/port-scan     # Port scanning
POST /api/recon/whois         # WHOIS information
```

## 🚨 Troubleshooting

### Common Issues & Solutions

#### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.11+

# Verify dependencies
pip install -r requirements.txt

# Check environment file
cat .env  # Ensure DATABASE_URL is set correctly
```

#### Frontend Build Errors
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version  # Should be 18+
```

#### Test Failures
- Ensure both frontend and backend servers are running
- Check that ports 3000 and 8000 are available
- Verify environment variables are set correctly
- Check network connectivity for external API calls

#### SSL Check Issues
- In sandboxed environments, SSL checks use mock data
- For production, ensure proper DNS resolution
- External network access may be required

### Development Tips

#### Adding New Security Tools
1. Create endpoint in appropriate API module
2. Add corresponding frontend component
3. Update API client in `frontend/lib/api.ts`
4. Add tests to `test_comprehensive.py`

#### Database Changes
1. Update models in `app/models/models.py`
2. Create Alembic migration: `alembic revision --autogenerate`
3. Apply migration: `alembic upgrade head`

## 🔒 Security Considerations

### Production Deployment
- Change default SECRET_KEY in environment
- Use PostgreSQL instead of SQLite
- Enable HTTPS with proper SSL certificates
- Implement rate limiting
- Set up proper logging and monitoring
- Use environment-specific configurations

### Data Protection
- User passwords are bcrypt hashed
- JWT tokens for session management
- Input validation on all endpoints
- SQL injection protection via SQLAlchemy ORM

## 📈 Performance & Scalability

### Optimization Tips
- Use Redis for caching (configured in docker-compose)
- Implement Celery for background tasks
- Use CDN for static assets
- Enable database connection pooling
- Set up load balancing for high traffic

### Monitoring
- Health check endpoint: `/health`
- Comprehensive logging throughout application
- Error tracking and reporting
- Performance metrics collection

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-tool`
3. Make changes with proper tests
4. Run test suite: `python test_comprehensive.py`
5. Submit pull request with description

### Code Standards
- Follow PEP 8 for Python code
- Use TypeScript for frontend components
- Include comprehensive tests for new features
- Document API endpoints properly
- Follow existing project structure

## 📞 Support

For issues, feature requests, or contributions:
- Create GitHub issues for bug reports
- Submit pull requests for feature additions
- Check existing documentation first
- Provide detailed error messages and logs

---

**Web Auditor** - Professional-grade security testing made accessible 🛡️