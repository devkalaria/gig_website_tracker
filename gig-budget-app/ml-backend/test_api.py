import requests
import json
import os

def test_prediction_api():
    """Test the prediction endpoints of the Flask API"""
    base_url = "http://127.0.0.1:5000/api"
    
    # Load test data from one of our generated files
    data_file = "data/user_1_data.json"
    
    if not os.path.exists(data_file):
        print(f"Test data file {data_file} not found. Please run train_models.py first.")
        return
    
    with open(data_file, 'r') as f:
        test_data = json.load(f)
    
    # Test each endpoint
    endpoints = [
        "forecast-income",
        "analyze-expenses",
        "savings-plan",
        "tax-suggestions",
        "low-income-preparation"
    ]
    
    for endpoint in endpoints:
        print(f"\n--- Testing {endpoint} endpoint ---")
        try:
            response = requests.post(
                f"{base_url}/{endpoint}", 
                json=test_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Success! Status code: {response.status_code}")
                print("Response preview:")
                print(json.dumps(result, indent=2)[:500] + "...")  # Show truncated response
            else:
                print(f"Error! Status code: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error testing {endpoint}: {str(e)}")
    
    print("\nTesting complete!")

def test_api_endpoints():
    """Test all API endpoints to verify they return expected data"""
    BASE_URL = "http://127.0.0.1:5000/api"
    
    # Get test data for a specific category
    print("\n1. Testing test-data endpoint...")
    response = requests.get(f"{BASE_URL}/test-data?category=Food Delivery")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Received test data with {len(data['incomeData'])} income entries and {len(data['expenseData'])} expense entries")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
    
    # Test each insight endpoint
    test_data = response.json() if response.status_code == 200 else {
        "incomeData": [],
        "expenseData": []
    }
    
    endpoints = [
        {"name": "forecast-income", "description": "Income forecast"},
        {"name": "analyze-expenses", "description": "Expense analysis"},
        {"name": "savings-plan", "description": "Savings plan"},
        {"name": "tax-suggestions", "description": "Tax suggestions"},
        {"name": "low-income-preparation", "description": "Seasonal planning"}
    ]
    
    for endpoint in endpoints:
        print(f"\n{endpoints.index(endpoint) + 2}. Testing {endpoint['description']} endpoint...")
        try:
            response = requests.post(f"{BASE_URL}/{endpoint['name']}", json=test_data)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success! Response: {json.dumps(result, indent=2)[:200]}...")
                print(f"   (Response truncated, full length: {len(json.dumps(result))} characters)")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_prediction_api()
    test_api_endpoints() 