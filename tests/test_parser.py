import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from parser import Genomic_Study_Parser

ARTIFACTS_PATH = Path(__file__).parent.parent / 'artifacts' / 'GenomicStudies'
EXPECTED_PATH = Path(__file__).parent / 'expected'


def run_test(input_filename, expected_filename):
    """
    Generic test runner that compares parser output against expected output.

    Args:
        input_filename: Name of the GenomicStudy JSON file in artifacts
        expected_filename: Name of the expected output JSON file in tests/expected
    """
    parser = Genomic_Study_Parser()
    actual = parser.parse_genomic_study(ARTIFACTS_PATH / input_filename)

    with open(EXPECTED_PATH / expected_filename, 'r') as f:
        expected = json.load(f)

    assert actual == expected, f"Mismatch for {input_filename}!\nExpected: {expected}\nActual: {actual}"
    print(f"PASS: {input_filename}")


def run_test_with_api_link(input_filename, expected_filename, api_link):
    """
    Generic test runner that tests API link URL construction.

    Args:
        input_filename: Name of the GenomicStudy JSON file in artifacts
        expected_filename: Name of the expected output JSON file in tests/expected
        api_link: Base API URL to prepend to references
    """
    parser = Genomic_Study_Parser()
    actual = parser.parse_genomic_study(ARTIFACTS_PATH / input_filename, api_link=api_link)

    with open(EXPECTED_PATH / expected_filename, 'r') as f:
        expected_raw = json.load(f)

    expected = {
        key: [f"{api_link.rstrip('/')}/{ref}" for ref in refs]
        for key, refs in expected_raw.items()
    }

    assert actual == expected, f"Mismatch for {input_filename} with API link!\nExpected: {expected}\nActual: {actual}"
    print(f"PASS: {input_filename} with API link")


# Test cases: (input_file, expected_file)
TEST_CASES = [
    ('lungMass.json', 'lungMass_files.json'),
    ('TrioStudy-DeNovoMutation1.json', 'TrioStudy-DeNovoMutation1_files.json'),
    ('TrioStudy-DeNovoMutation2.json', 'TrioStudy-DeNovoMutation2_files.json'),
]


if __name__ == '__main__':
    for input_file, expected_file in TEST_CASES:
        run_test(input_file, expected_file)

    # Test API link construction with first test case
    run_test_with_api_link(
        TEST_CASES[0][0],
        TEST_CASES[0][1],
        'https://fhir.example.org/r5'
    )

    print("\nAll tests passed!")
