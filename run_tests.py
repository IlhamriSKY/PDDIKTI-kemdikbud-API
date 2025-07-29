"""
PDDIKTI API Test Runner
Runs all tests in the tests folder with clean output
"""

import sys
import subprocess
from pathlib import Path


def main():
    """Run all tests with proper output"""
    print("=" * 60)
    print("PDDIKTI API TEST SUITE")
    print("=" * 60)
    print("Testing Universitas Unika Soegijapranata Data")
    print("Student: Ilham Riski")
    print("Lecturer: Ridwan Sanjaya") 
    print("Program: Sistem Informasi")
    print("=" * 60)
    
    # Get current directory
    current_dir = Path(__file__).parent
    tests_dir = current_dir / "tests"
    
    try:
        # Run pytest with clean output
        cmd = [
            sys.executable, "-m", "pytest", 
            str(tests_dir),
            "-v", 
            "--tb=short",
            "--disable-warnings"
        ]
        
        print("Running tests...")
        print("-" * 60)
        
        result = subprocess.run(cmd)
        
        print("-" * 60)
        if result.returncode == 0:
            print("SUCCESS: All tests passed!")
            print("Framework is optimized and ready for production use!")
        else:
            print(f"FAILURE: Tests failed with exit code {result.returncode}")
            
        return result.returncode
        
    except Exception as e:
        print(f"ERROR: Failed to run tests - {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
