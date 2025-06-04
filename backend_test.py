import requests
import json
import time
import sys
from datetime import datetime

class AIProjectManagerTester:
    def __init__(self, base_url="https://04555009-223f-4b29-b351-2e5f65dbecbd.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.requirements_id = None
        self.plan_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return success, response.json()
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    print(f"Response: {response.text}")
                except:
                    pass
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        success, response = self.run_test(
            "Root API Endpoint",
            "GET",
            "",
            200
        )
        if success:
            print(f"Response message: {response.get('message', 'No message')}")
        return success

    def test_submit_project_requirements(self, project_data):
        """Test submitting project requirements"""
        success, response = self.run_test(
            "Submit Project Requirements",
            "POST",
            "project-requirements",
            200,
            data=project_data
        )
        if success and 'id' in response:
            self.requirements_id = response['id']
            print(f"Created requirements with ID: {self.requirements_id}")
        return success

    def test_get_project_requirements(self):
        """Test getting project requirements by ID"""
        if not self.requirements_id:
            print("❌ Cannot test get requirements - no requirements ID available")
            return False
            
        success, response = self.run_test(
            "Get Project Requirements",
            "GET",
            f"project-requirements/{self.requirements_id}",
            200
        )
        if success:
            print(f"Retrieved requirements with title: {response.get('title', 'No title')}")
        return success

    def test_generate_plan(self):
        """Test generating an AI project plan"""
        if not self.requirements_id:
            print("❌ Cannot test plan generation - no requirements ID available")
            return False
            
        success, response = self.run_test(
            "Generate AI Project Plan",
            "POST",
            f"generate-plan/{self.requirements_id}",
            200
        )
        if success and 'id' in response:
            self.plan_id = response['id']
            print(f"Generated plan with ID: {self.plan_id}")
            
            # Validate plan structure
            required_fields = [
                'objectives', 'wbs_tasks', 'timeline_weeks', 'resource_estimates', 
                'risk_analysis', 'success_metrics', 'next_steps', 'confidence_score'
            ]
            
            missing_fields = [field for field in required_fields if field not in response]
            
            if missing_fields:
                print(f"❌ Plan is missing required fields: {', '.join(missing_fields)}")
                return False
            else:
                print("✅ Plan contains all required fields")
                
                # Print some plan details
                print(f"Timeline: {response['timeline_weeks']} weeks")
                print(f"Confidence score: {response['confidence_score']}")
                print(f"Number of objectives: {len(response['objectives'])}")
                print(f"Number of WBS tasks: {len(response['wbs_tasks'])}")
                print(f"Number of risks identified: {len(response['risk_analysis'])}")
                
        return success

    def test_get_project_plan(self):
        """Test getting a project plan by ID"""
        if not self.plan_id:
            print("❌ Cannot test get plan - no plan ID available")
            return False
            
        success, response = self.run_test(
            "Get Project Plan",
            "GET",
            f"project-plan/{self.plan_id}",
            200
        )
        return success

    def test_get_all_plans(self):
        """Test getting all project plans"""
        success, response = self.run_test(
            "Get All Project Plans",
            "GET",
            "project-plans",
            200
        )
        if success:
            print(f"Retrieved {len(response)} project plans")
        return success

    def test_get_all_requirements(self):
        """Test getting all project requirements"""
        success, response = self.run_test(
            "Get All Project Requirements",
            "GET",
            "project-requirements",
            200
        )
        if success:
            print(f"Retrieved {len(response)} project requirements")
        return success

def main():
    # Sample project data for testing
    sample_project = {
        "title": "E-commerce Platform Development",
        "description": "Build a modern e-commerce platform with user authentication, product catalog, shopping cart, and payment processing",
        "business_context": "Need to compete with major e-commerce platforms and provide seamless shopping experience for customers",
        "success_criteria": "Platform launches successfully, handles 1000+ concurrent users, achieves 99.9% uptime, generates $100K+ revenue in first quarter",
        "constraints": "6-month deadline, $200K budget, team of 5 developers, must integrate with existing inventory system",
        "stakeholders": "Product Manager, Engineering Team, Marketing Team, Finance Team, Executive Sponsor",
        "timeline_preference": "6 months maximum, launch by Q3 2025",
        "budget_range": "$150K - $200K"
    }

    # Setup tester
    tester = AIProjectManagerTester()
    
    print("=" * 80)
    print("TESTING AUTONOMOUS AI PROJECT MANAGER API")
    print("=" * 80)
    
    # Run tests
    tester.test_root_endpoint()
    
    if tester.test_submit_project_requirements(sample_project):
        tester.test_get_project_requirements()
        
        print("\nWaiting for plan generation (this may take a moment)...")
        if tester.test_generate_plan():
            tester.test_get_project_plan()
    
    tester.test_get_all_plans()
    tester.test_get_all_requirements()
    
    # Print results
    print("\n" + "=" * 80)
    print(f"TESTS PASSED: {tester.tests_passed}/{tester.tests_run}")
    print("=" * 80)
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())
