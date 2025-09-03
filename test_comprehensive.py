#!/usr/bin/env python3
"""
Comprehensive Test Suite for Web Auditor Application
Tests all modules and functionality A to Z
"""

import requests
import json
import time
import sys
import os

# Configuration
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

class WebAuditorTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        self.test_results = []
        
    def log_test(self, test_name, status, message=""):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_symbol} {test_name}: {message}")
        
    def test_health_check(self):
        """Test basic health endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/health")
            if response.status_code == 200 and response.json().get("status") == "healthy":
                self.log_test("Health Check", "PASS", "Backend is healthy")
            else:
                self.log_test("Health Check", "FAIL", f"Health check failed: {response.text}")
        except Exception as e:
            self.log_test("Health Check", "FAIL", f"Connection error: {str(e)}")
            
    def test_user_registration(self):
        """Test user registration"""
        try:
            test_user = {
                "username": f"testuser_{int(time.time())}",
                "email": f"test_{int(time.time())}@example.com", 
                "password": "SecurePassword123!"
            }
            
            response = self.session.post(f"{BASE_URL}/api/auth/register", json=test_user)
            if response.status_code == 200:
                data = response.json()
                self.user_id = data.get("id")
                self.log_test("User Registration", "PASS", f"User created with ID: {self.user_id}")
                return test_user
            else:
                self.log_test("User Registration", "FAIL", f"Registration failed: {response.text}")
                return None
        except Exception as e:
            self.log_test("User Registration", "FAIL", f"Registration error: {str(e)}")
            return None
            
    def test_user_login(self, user_data):
        """Test user login"""
        if not user_data:
            self.log_test("User Login", "SKIP", "No user data from registration")
            return False
            
        try:
            login_data = {
                "username": user_data["username"],
                "password": user_data["password"]
            }
            
            response = self.session.post(
                f"{BASE_URL}/api/auth/token",
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                self.log_test("User Login", "PASS", "Login successful, token obtained")
                return True
            else:
                self.log_test("User Login", "FAIL", f"Login failed: {response.text}")
                return False
        except Exception as e:
            self.log_test("User Login", "FAIL", f"Login error: {str(e)}")
            return False
            
    def test_user_profile(self):
        """Test user profile retrieval"""
        if not self.token:
            self.log_test("User Profile", "SKIP", "No authentication token")
            return
            
        try:
            response = self.session.get(f"{BASE_URL}/api/auth/me")
            if response.status_code == 200:
                data = response.json()
                self.log_test("User Profile", "PASS", f"Profile retrieved for user: {data.get('username')}")
            else:
                self.log_test("User Profile", "FAIL", f"Profile retrieval failed: {response.text}")
        except Exception as e:
            self.log_test("User Profile", "FAIL", f"Profile error: {str(e)}")
            
    def test_npm_package_info(self):
        """Test NPM package information retrieval"""
        if not self.token:
            self.log_test("NPM Package Info", "SKIP", "No authentication token")
            return
            
        try:
            response = self.session.get(f"{BASE_URL}/api/npm/package-info/express")
            if response.status_code == 200:
                data = response.json()
                self.log_test("NPM Package Info", "PASS", f"Retrieved info for: {data.get('name')}")
            else:
                self.log_test("NPM Package Info", "FAIL", f"Package info failed: {response.text}")
        except Exception as e:
            self.log_test("NPM Package Info", "FAIL", f"Package info error: {str(e)}")
            
    def test_dependency_check(self):
        """Test dependency vulnerability check"""
        if not self.token:
            self.log_test("Dependency Check", "SKIP", "No authentication token")
            return
            
        try:
            test_data = {
                "dependencies": ["express", "lodash", "react"]
            }
            
            response = self.session.post(f"{BASE_URL}/api/npm/dependency-check", json=test_data)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Dependency Check", "PASS", f"Checked {data.get('checked_packages')} packages")
            else:
                self.log_test("Dependency Check", "FAIL", f"Dependency check failed: {response.text}")
        except Exception as e:
            self.log_test("Dependency Check", "FAIL", f"Dependency check error: {str(e)}")
            
    def test_password_strength(self):
        """Test password strength analyzer"""
        if not self.token:
            self.log_test("Password Strength", "SKIP", "No authentication token")
            return
            
        try:
            test_passwords = [
                "weak",
                "StrongPassword123!",
                "VerySecureComplexPassword2024!"
            ]
            
            for password in test_passwords:
                test_data = {"password": password}
                response = self.session.post(
                    f"{BASE_URL}/api/security/password-strength",
                    json=test_data
                )
                
                if response.status_code == 200:
                    data = response.json()
                    strength = data.get('strength')
                    self.log_test("Password Strength", "PASS", f"Password '{password[:8]}...' rated as {strength}")
                else:
                    self.log_test("Password Strength", "FAIL", f"Password analysis failed: {response.text}")
                    break
                    
        except Exception as e:
            self.log_test("Password Strength", "FAIL", f"Password strength error: {str(e)}")
            
    def test_ssl_check(self):
        """Test SSL certificate checking"""
        if not self.token:
            self.log_test("SSL Check", "SKIP", "No authentication token")
            return
            
        try:
            test_data = {"domain": "google.com"}
            response = self.session.post(f"{BASE_URL}/api/security/ssl-check", json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("SSL Check", "PASS", f"SSL check for {data.get('domain')} - Score: {data.get('security_score')}")
            else:
                self.log_test("SSL Check", "FAIL", f"SSL check failed: {response.text}")
        except Exception as e:
            self.log_test("SSL Check", "FAIL", f"SSL check error: {str(e)}")
            
    def test_email_security(self):
        """Test email security analysis"""
        if not self.token:
            self.log_test("Email Security", "SKIP", "No authentication token")
            return
            
        try:
            test_data = {"email": "test@gmail.com"}
            response = self.session.post(f"{BASE_URL}/api/security/email-security", json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Email Security", "PASS", f"Email security check - Assessment: {data.get('assessment')}")
            else:
                self.log_test("Email Security", "FAIL", f"Email security check failed: {response.text}")
        except Exception as e:
            self.log_test("Email Security", "FAIL", f"Email security error: {str(e)}")
            
    def test_frontend_accessibility(self):
        """Test frontend page accessibility"""
        try:
            pages = [
                "/",
                "/login", 
                "/register",
                "/npm-security"
            ]
            
            for page in pages:
                response = requests.get(f"{FRONTEND_URL}{page}")
                if response.status_code == 200:
                    self.log_test("Frontend Page", "PASS", f"Page {page} accessible")
                else:
                    self.log_test("Frontend Page", "FAIL", f"Page {page} returned {response.status_code}")
                    
        except Exception as e:
            self.log_test("Frontend Page", "FAIL", f"Frontend accessibility error: {str(e)}")
            
    def test_api_documentation(self):
        """Test API documentation accessibility"""
        try:
            response = self.session.get(f"{BASE_URL}/docs")
            if response.status_code == 200:
                self.log_test("API Documentation", "PASS", "Swagger docs accessible")
            else:
                self.log_test("API Documentation", "FAIL", f"API docs returned {response.status_code}")
                
            # Test OpenAPI schema
            response = self.session.get(f"{BASE_URL}/openapi.json")
            if response.status_code == 200:
                data = response.json()
                self.log_test("OpenAPI Schema", "PASS", f"Schema contains {len(data.get('paths', {}))} endpoints")
            else:
                self.log_test("OpenAPI Schema", "FAIL", f"OpenAPI schema returned {response.status_code}")
                
        except Exception as e:
            self.log_test("API Documentation", "FAIL", f"API documentation error: {str(e)}")
            
    def run_all_tests(self):
        """Run the complete test suite"""
        print("🚀 Starting Web Auditor Comprehensive Test Suite")
        print("=" * 60)
        
        # Basic connectivity tests
        self.test_health_check()
        self.test_api_documentation()
        self.test_frontend_accessibility()
        
        # Authentication tests
        user_data = self.test_user_registration()
        login_success = self.test_user_login(user_data)
        
        if login_success:
            self.test_user_profile()
            
            # NPM Security tests
            self.test_npm_package_info()
            self.test_dependency_check()
            
            # Security Tools tests
            self.test_password_strength()
            self.test_ssl_check()
            self.test_email_security()
        
        # Print summary
        self.print_summary()
        
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["status"] == "PASS"])
        failed_tests = len([t for t in self.test_results if t["status"] == "FAIL"])
        skipped_tests = len([t for t in self.test_results if t["status"] == "SKIP"])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️ Skipped: {skipped_tests}")
        
        success_rate = (passed_tests / (total_tests - skipped_tests)) * 100 if (total_tests - skipped_tests) > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for test in self.test_results:
                if test["status"] == "FAIL":
                    print(f"  - {test['test']}: {test['message']}")
        
        print("\n🎉 Test suite completed!")
        return failed_tests == 0

if __name__ == "__main__":
    tester = WebAuditorTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)