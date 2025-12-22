#!/usr/bin/env python3
"""
Run all unit tests in the tests/ directory.
"""

import sys
import unittest
from pathlib import Path


def main():
    # Ensure project root is on sys.path
    tests_dir = Path(__file__).parent
    project_root = tests_dir.parent
    sys.path.insert(0, str(project_root))

    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=str(tests_dir),
        pattern="test*.py"
    )

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with proper status code (important for CI)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
