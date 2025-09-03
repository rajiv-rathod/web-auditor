#!/bin/bash

echo "🔒 Web Auditor Demo Script"
echo "=========================="
echo ""

# Start the backend
echo "📡 Starting Web Auditor Backend..."
cd /home/runner/work/web-auditor/web-auditor
python -m app.main &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

echo "✅ Backend started on http://localhost:8000"
echo ""

# Test API endpoints
echo "🧪 Testing API Endpoints:"
echo ""

echo "1. Root endpoint:"
curl -s http://localhost:8000/ | jq '.'
echo ""

echo "2. Health check:"
curl -s http://localhost:8000/health | jq '.'
echo ""

echo "3. Testing user registration:"
curl -s -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@example.com","password":"demopass123"}' | jq '.'
echo ""

echo "4. Testing user login:"
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo&password=demopass123")
echo $LOGIN_RESPONSE | jq '.'

# Extract token
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')
echo ""

echo "5. Testing authenticated endpoint:"
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/auth/me | jq '.'
echo ""

echo "6. Testing recon endpoints:"
echo "DNS Lookup:"
curl -s -X POST "http://localhost:8000/api/recon/dns-lookup" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"domain":"google.com","record_type":"A"}' | jq '.'
echo ""

echo "7. Testing subdomain enumeration:"
curl -s -X POST "http://localhost:8000/api/recon/subdomain" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"domain":"example.com","tools":["subfinder"]}' | jq '.'
echo ""

echo "8. API Documentation available at: http://localhost:8000/docs"
echo ""

echo "🎯 Demo completed! Backend still running..."
echo "Kill the backend with: kill $BACKEND_PID"