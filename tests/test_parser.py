import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from parser import GenomicStudyParser

ARTIFACTS_PATH = Path(__file__).parent.parent / 'artifacts' / 'GenomicStudies'
EXPECTED_PATH = Path(__file__).parent / 'expected'

TEST_CASES = [
    ('lungMass.json', 'lungMass_files.json'),
    ('TrioStudy-DeNovoMutation1.json', 'TrioStudy-DeNovoMutation1_files.json'),
    ('TrioStudy-DeNovoMutation2.json', 'TrioStudy-DeNovoMutation2_files.json'),
]


def run_test(input_filename, expected_filename):
    parser = GenomicStudyParser()
    actual = parser.parse(ARTIFACTS_PATH / input_filename)

    with open(EXPECTED_PATH / expected_filename, 'r') as f:
        expected = json.load(f)

    assert actual == expected, f"Mismatch for {input_filename}"
    print(f"PASS: {input_filename}")


if __name__ == '__main__':
    for input_file, expected_file in TEST_CASES:
        run_test(input_file, expected_file)
    print("\nAll tests passed!")
