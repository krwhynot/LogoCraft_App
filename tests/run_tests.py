import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_test_suite():
    """Run all test suites"""
    # Create test loader
    loader = unittest.TestLoader()

    # Discover all tests in the tests directory
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')

    # Create test runner
    runner = unittest.TextTestRunner(verbosity=2)

    print("\nRunning Test Suites:")
    print("=" * 70)
    print("1. Unit Tests (test_unit_image_processor.py)")
    print("   - Individual component testing")
    print("   - Image processing functionality")
    print("   - Color and format handling")
    print("   - Error handling")
    print("\n2. Integration Tests (test_integration.py)")
    print("   - Complete workflow scenarios")
    print("   - Cross-component interaction")
    print("   - GUI functionality")
    print("   - File operations")
    print("\n3. Format Tests (test_image_formats.py)")
    print("   - Various image formats")
    print("   - Different dimensions")
    print("   - Aspect ratio handling")
    print("=" * 70)
    print("\nTest Results:\n")

    # Run the test suite
    result = runner.run(suite)

    # Return 0 if all tests passed, 1 if any failed
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_test_suite())
