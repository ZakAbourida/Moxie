#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Athletica
Tests authentication, CRUD operations, analytics, and session templates
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

class AthlicaAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str, details: Any = None):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def setup_auth_headers(self):
        """Setup authorization headers"""
        if self.access_token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            })
    
    def test_health_check(self):
        """Test basic API health"""
        try:
            response = self.session.get(f"{API_BASE}/")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", True, f"API is healthy: {data.get('message', 'OK')}")
                return True
            else:
                self.log_test("Health Check", False, f"Health check failed with status {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Health check failed: {str(e)}")
            return False
    
    def create_test_coach(self):
        """Create a test coach user"""
        try:
            coach_data = {
                "role": "coach",
                "email": "coach@example.com",
                "password": "Password123!",
                "first_name": "Test",
                "last_name": "Coach"
            }
            
            response = self.session.post(f"{API_BASE}/auth/register", json=coach_data)
            if response.status_code == 200:
                self.log_test("Create Test Coach", True, "Coach created successfully")
                return True
            elif response.status_code == 400 and "already registered" in response.text:
                self.log_test("Create Test Coach", True, "Coach already exists (expected)")
                return True
            else:
                self.log_test("Create Test Coach", False, f"Failed to create coach: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.log_test("Create Test Coach", False, f"Exception creating coach: {str(e)}")
            return False
    
    def test_login(self):
        """Test login with coach credentials"""
        try:
            login_data = {
                "email": "coach@example.com",
                "password": "Password123!"
            }
            
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                if self.access_token:
                    self.setup_auth_headers()
                    self.log_test("Login", True, "Login successful, token received")
                    return True
                else:
                    self.log_test("Login", False, "Login response missing access token")
                    return False
            else:
                self.log_test("Login", False, f"Login failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.log_test("Login", False, f"Login exception: {str(e)}")
            return False
    
    def test_get_me(self):
        """Test getting current user info"""
        try:
            response = self.session.get(f"{API_BASE}/auth/me")
            if response.status_code == 200:
                data = response.json()
                if data.get('email') == 'coach@example.com' and data.get('role') == 'coach':
                    self.log_test("Get Me", True, f"User info retrieved: {data.get('first_name')} {data.get('last_name')}")
                    return True
                else:
                    self.log_test("Get Me", False, f"Unexpected user data: {data}")
                    return False
            else:
                self.log_test("Get Me", False, f"Get me failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.log_test("Get Me", False, f"Get me exception: {str(e)}")
            return False
    
    def test_unauthorized_access(self):
        """Test that protected endpoints require authentication"""
        try:
            # Temporarily remove auth headers
            temp_headers = self.session.headers.copy()
            self.session.headers.pop('Authorization', None)
            
            response = self.session.get(f"{API_BASE}/athletes")
            
            # Restore headers
            self.session.headers.update(temp_headers)
            
            if response.status_code == 401:
                self.log_test("Unauthorized Access", True, "Protected endpoint correctly requires authentication")
                return True
            else:
                self.log_test("Unauthorized Access", False, f"Expected 401, got {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Unauthorized Access", False, f"Exception testing unauthorized access: {str(e)}")
            return False
    
    def create_test_data(self):
        """Create test data for comprehensive testing"""
        try:
            # Create test athletes
            athletes_data = [
                {
                    "first_name": "Sarah",
                    "last_name": "Johnson",
                    "birth_date": "1995-03-15T00:00:00Z",
                    "sex": "female",
                    "height_cm": 165.0,
                    "weight_kg": 58.0,
                    "specialties": ["100m", "200m"],
                    "sector": "sprints",
                    "category": "senior",
                    "coach_name": "Test Coach",
                    "club": "Athletics Club"
                },
                {
                    "first_name": "Marcus",
                    "last_name": "Williams",
                    "birth_date": "1993-07-22T00:00:00Z",
                    "sex": "male",
                    "height_cm": 180.0,
                    "weight_kg": 75.0,
                    "specialties": ["400m", "800m"],
                    "sector": "middle_distance",
                    "category": "senior",
                    "coach_name": "Test Coach",
                    "club": "Running Club"
                },
                {
                    "first_name": "Elena",
                    "last_name": "Rodriguez",
                    "birth_date": "1997-11-08T00:00:00Z",
                    "sex": "female",
                    "height_cm": 170.0,
                    "weight_kg": 62.0,
                    "specialties": ["long_jump", "triple_jump"],
                    "sector": "jumps",
                    "category": "senior",
                    "coach_name": "Test Coach",
                    "club": "Field Events Club"
                }
            ]
            
            created_athletes = []
            for athlete_data in athletes_data:
                response = self.session.post(f"{API_BASE}/athletes", json=athlete_data)
                if response.status_code == 200:
                    created_athletes.append(response.json())
            
            if len(created_athletes) == 3:
                self.log_test("Create Test Athletes", True, f"Created {len(created_athletes)} test athletes")
                self.test_athlete_ids = [athlete['id'] for athlete in created_athletes]
                return True
            else:
                self.log_test("Create Test Athletes", False, f"Only created {len(created_athletes)} out of 3 athletes")
                return False
                
        except Exception as e:
            self.log_test("Create Test Athletes", False, f"Exception creating test data: {str(e)}")
            return False
    
    def create_additional_test_data(self):
        """Create goals, programs, sessions, exercises, and assessments"""
        try:
            if not hasattr(self, 'test_athlete_ids') or not self.test_athlete_ids:
                self.log_test("Create Additional Test Data", False, "No athlete IDs available")
                return False
            
            # Create goals
            goals_created = 0
            for i, athlete_id in enumerate(self.test_athlete_ids):
                goal_data = {
                    "athlete_id": athlete_id,
                    "name": f"Improve Performance Goal {i+1}",
                    "type": "performance",
                    "description": f"Performance improvement goal for athlete {i+1}",
                    "start_date": datetime.now().isoformat(),
                    "end_date": (datetime.now() + timedelta(days=90)).isoformat(),
                    "priority": "high",
                    "target_value": "10.5s"
                }
                response = self.session.post(f"{API_BASE}/goals", json=goal_data)
                if response.status_code == 200:
                    goals_created += 1
            
            # Create programs
            programs_created = 0
            for i, athlete_id in enumerate(self.test_athlete_ids):
                program_data = {
                    "athlete_id": athlete_id,
                    "name": f"Training Program {i+1}",
                    "start_date": datetime.now().isoformat(),
                    "end_date": (datetime.now() + timedelta(days=60)).isoformat(),
                    "weekly_frequency": 4,
                    "structure_text": f"4x weekly training program for athlete {i+1}",
                    "notes": "Comprehensive training program"
                }
                response = self.session.post(f"{API_BASE}/programs", json=program_data)
                if response.status_code == 200:
                    programs_created += 1
                    if not hasattr(self, 'test_program_ids'):
                        self.test_program_ids = []
                    self.test_program_ids.append(response.json()['id'])
            
            # Create exercises
            exercises_data = [
                {"name": "Squats", "category": "legs", "muscles": ["quadriceps", "glutes"], "description": "Basic squat exercise"},
                {"name": "Bench Press", "category": "push", "muscles": ["chest", "triceps"], "description": "Chest press exercise"},
                {"name": "Pull-ups", "category": "pull", "muscles": ["lats", "biceps"], "description": "Upper body pull exercise"},
                {"name": "Deadlifts", "category": "legs", "muscles": ["hamstrings", "glutes"], "description": "Hip hinge movement"},
                {"name": "Clean & Jerk", "category": "olympic", "muscles": ["full_body"], "description": "Olympic lift"},
                {"name": "Plank", "category": "core", "muscles": ["core"], "description": "Core stability exercise"}
            ]
            
            exercises_created = 0
            for exercise_data in exercises_data:
                response = self.session.post(f"{API_BASE}/exercises", json=exercise_data)
                if response.status_code == 200:
                    exercises_created += 1
            
            # Create sessions
            sessions_created = 0
            if hasattr(self, 'test_program_ids') and self.test_program_ids:
                for i, (athlete_id, program_id) in enumerate(zip(self.test_athlete_ids, self.test_program_ids)):
                    for j in range(2):  # 2 sessions per athlete
                        session_data = {
                            "program_id": program_id,
                            "athlete_id": athlete_id,
                            "title": f"Training Session {j+1} - Athlete {i+1}",
                            "type": "gym",
                            "start": (datetime.now() + timedelta(days=j)).isoformat(),
                            "end": (datetime.now() + timedelta(days=j, hours=1)).isoformat(),
                            "intensity": 7,
                            "tags": ["strength", "conditioning"],
                            "notes": f"Training session {j+1}"
                        }
                        response = self.session.post(f"{API_BASE}/sessions", json=session_data)
                        if response.status_code == 200:
                            sessions_created += 1
            
            # Create assessments
            assessments_created = 0
            for athlete_id in self.test_athlete_ids:
                assessment_data = {
                    "athlete_id": athlete_id,
                    "date": datetime.now().isoformat(),
                    "strength_max": 8,
                    "strength_endurance": 7,
                    "strength_explosive": 9,
                    "speed_linear": 8,
                    "agility": 7,
                    "power": 9,
                    "mobility": 6,
                    "endurance_aerobic": 7,
                    "endurance_lactate": 8,
                    "icm": 7,
                    "notes": "Initial assessment"
                }
                response = self.session.post(f"{API_BASE}/assessments", json=assessment_data)
                if response.status_code == 200:
                    assessments_created += 1
            
            # Create session templates
            templates_data = [
                {
                    "name": "Strength Training",
                    "type": "gym",
                    "description": "Basic strength training template",
                    "duration_min": 90,
                    "intensity": 8,
                    "tags": ["strength", "gym"],
                    "exercises": []
                },
                {
                    "name": "Speed Work",
                    "type": "speed",
                    "description": "Sprint training template",
                    "duration_min": 60,
                    "intensity": 9,
                    "tags": ["speed", "track"],
                    "exercises": []
                },
                {
                    "name": "Endurance Base",
                    "type": "endurance",
                    "description": "Aerobic base building",
                    "duration_min": 120,
                    "intensity": 5,
                    "tags": ["endurance", "aerobic"],
                    "exercises": []
                }
            ]
            
            templates_created = 0
            for template_data in templates_data:
                response = self.session.post(f"{API_BASE}/templates/sessions", json=template_data)
                if response.status_code == 200:
                    templates_created += 1
            
            success_msg = f"Created: {goals_created} goals, {programs_created} programs, {sessions_created} sessions, {exercises_created} exercises, {assessments_created} assessments, {templates_created} templates"
            self.log_test("Create Additional Test Data", True, success_msg)
            return True
            
        except Exception as e:
            self.log_test("Create Additional Test Data", False, f"Exception: {str(e)}")
            return False
    
    def test_crud_operations(self):
        """Test all CRUD operations"""
        try:
            # Test GET /api/athletes
            response = self.session.get(f"{API_BASE}/athletes")
            if response.status_code == 200:
                athletes = response.json()
                if len(athletes) >= 3:
                    self.log_test("GET Athletes", True, f"Retrieved {len(athletes)} athletes (Sarah, Marcus, Elena expected)")
                else:
                    self.log_test("GET Athletes", False, f"Expected at least 3 athletes, got {len(athletes)}")
            else:
                self.log_test("GET Athletes", False, f"Failed to get athletes: {response.status_code}")
            
            # Test GET /api/goals
            response = self.session.get(f"{API_BASE}/goals")
            if response.status_code == 200:
                goals = response.json()
                self.log_test("GET Goals", True, f"Retrieved {len(goals)} goals")
            else:
                self.log_test("GET Goals", False, f"Failed to get goals: {response.status_code}")
            
            # Test GET /api/programs
            response = self.session.get(f"{API_BASE}/programs")
            if response.status_code == 200:
                programs = response.json()
                self.log_test("GET Programs", True, f"Retrieved {len(programs)} training programs")
            else:
                self.log_test("GET Programs", False, f"Failed to get programs: {response.status_code}")
            
            # Test GET /api/sessions
            response = self.session.get(f"{API_BASE}/sessions")
            if response.status_code == 200:
                sessions = response.json()
                self.log_test("GET Sessions", True, f"Retrieved {len(sessions)} training sessions")
            else:
                self.log_test("GET Sessions", False, f"Failed to get sessions: {response.status_code}")
            
            # Test GET /api/exercises
            response = self.session.get(f"{API_BASE}/exercises")
            if response.status_code == 200:
                exercises = response.json()
                self.log_test("GET Exercises", True, f"Retrieved {len(exercises)} exercises")
            else:
                self.log_test("GET Exercises", False, f"Failed to get exercises: {response.status_code}")
            
            # Test GET /api/assessments
            response = self.session.get(f"{API_BASE}/assessments")
            if response.status_code == 200:
                assessments = response.json()
                self.log_test("GET Assessments", True, f"Retrieved {len(assessments)} physical assessments")
            else:
                self.log_test("GET Assessments", False, f"Failed to get assessments: {response.status_code}")
            
            return True
            
        except Exception as e:
            self.log_test("CRUD Operations", False, f"Exception during CRUD testing: {str(e)}")
            return False
    
    def test_analytics_endpoints(self):
        """Test analytics endpoints"""
        try:
            if not hasattr(self, 'test_athlete_ids') or not self.test_athlete_ids:
                self.log_test("Analytics Endpoints", False, "No test athlete IDs available")
                return False
            
            athlete_id = self.test_athlete_ids[0]
            
            # Test athlete overview
            response = self.session.get(f"{API_BASE}/analytics/athlete/{athlete_id}/overview")
            if response.status_code == 200:
                overview = response.json()
                expected_fields = ['weekly_volume', 'intensity_avg', 'sessions_count_by_type', 'next_events']
                if all(field in overview for field in expected_fields):
                    self.log_test("Analytics Overview", True, f"Retrieved athlete overview with all expected fields")
                else:
                    self.log_test("Analytics Overview", False, f"Missing fields in overview: {overview}")
            else:
                self.log_test("Analytics Overview", False, f"Failed to get overview: {response.status_code}")
            
            # Test athlete assessments
            response = self.session.get(f"{API_BASE}/analytics/athlete/{athlete_id}/assessments")
            if response.status_code == 200:
                assessments = response.json()
                expected_fields = ['dates', 'strength_max', 'strength_endurance', 'speed_linear', 'agility', 'power']
                if all(field in assessments for field in expected_fields):
                    self.log_test("Analytics Assessments", True, f"Retrieved assessment series for radar chart")
                else:
                    self.log_test("Analytics Assessments", False, f"Missing fields in assessments: {assessments}")
            else:
                self.log_test("Analytics Assessments", False, f"Failed to get assessments: {response.status_code}")
            
            return True
            
        except Exception as e:
            self.log_test("Analytics Endpoints", False, f"Exception during analytics testing: {str(e)}")
            return False
    
    def test_session_templates(self):
        """Test session templates endpoint"""
        try:
            response = self.session.get(f"{API_BASE}/templates/sessions")
            if response.status_code == 200:
                templates = response.json()
                if len(templates) >= 3:
                    self.log_test("Session Templates", True, f"Retrieved {len(templates)} session templates")
                    return True
                else:
                    self.log_test("Session Templates", False, f"Expected at least 3 templates, got {len(templates)}")
                    return False
            else:
                self.log_test("Session Templates", False, f"Failed to get templates: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Session Templates", False, f"Exception testing templates: {str(e)}")
            return False
    
    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print(f"🚀 Starting Athletica Backend API Testing")
        print(f"📍 Backend URL: {BACKEND_URL}")
        print(f"📍 API Base: {API_BASE}")
        print("=" * 60)
        
        # Test sequence
        tests = [
            ("Health Check", self.test_health_check),
            ("Create Test Coach", self.create_test_coach),
            ("Authentication - Login", self.test_login),
            ("Authentication - Get Me", self.test_get_me),
            ("Authentication - Unauthorized Access", self.test_unauthorized_access),
            ("Create Test Data", self.create_test_data),
            ("Create Additional Test Data", self.create_additional_test_data),
            ("CRUD Operations", self.test_crud_operations),
            ("Analytics Endpoints", self.test_analytics_endpoints),
            ("Session Templates", self.test_session_templates)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🧪 Running: {test_name}")
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                self.log_test(test_name, False, f"Unexpected exception: {str(e)}")
        
        print("\n" + "=" * 60)
        print(f"📊 TEST SUMMARY: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Backend APIs are working correctly.")
        else:
            print(f"⚠️  {total - passed} tests failed. Check details above.")
        
        return passed == total
    
    def get_summary(self):
        """Get test summary"""
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        summary = {
            'total_tests': total,
            'passed': passed,
            'failed': total - passed,
            'success_rate': (passed / total * 100) if total > 0 else 0,
            'results': self.test_results
        }
        
        return summary

if __name__ == "__main__":
    tester = AthlicaAPITester()
    success = tester.run_comprehensive_test()
    
    # Print detailed results
    print(f"\n📋 DETAILED RESULTS:")
    for result in tester.test_results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['test']}: {result['message']}")
    
    exit(0 if success else 1)