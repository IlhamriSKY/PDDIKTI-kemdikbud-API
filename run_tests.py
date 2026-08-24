"""PDDIKTI API test runner.

Runs every test in the tests folder with clean output.
"""

import subprocess  # nosec B404 - fixed argv, no shell, no external input
import sys
from pathlib import Path


def main():
    """Run all tests with proper output."""
    print("=" * 60)
    print("PDDIKTI API TEST SUITE")
    print("=" * 60)
    print("Testing Universitas Unika Soegijapranata Data")
    print("Student: Ilham Riski Wibowo (NIM: 15.N1.0012)")
    print("Lecturer: Ridwan Sanjaya")
    print("University: Universitas Katolik Soegijapranata")
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

        # nosec B603 - argv is built above from sys.executable and a repo path
        result = subprocess.run(cmd, check=False)  # nosec B603

        print("-" * 60)
        if result.returncode == 0:
            print("SUCCESS: All tests passed!")
            print("Framework is optimized and ready for production use!")
        else:
            print(f"FAILURE: Tests failed with exit code {result.returncode}")

        return result.returncode

    except OSError as e:
        print(f"ERROR: Failed to run tests - {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
