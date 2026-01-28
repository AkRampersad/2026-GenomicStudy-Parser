import json


class Genomic_Study_Parser:
    def __init__(self, *args, **kwargs):
        self.files = {}

    def parse_genomic_study(self, input_path, api_link=None):
        """
        Parse a FHIR R5 GenomicStudy resource and extract file/artifact references.

        Args:
            input_path: Path to the JSON file containing the GenomicStudy resource
            api_link: Optional base API URL for constructing full file URLs

        Returns:
            Dictionary containing file references from all analyses
        """
        self.api_link = api_link

        with open(input_path, 'r') as json_file:
            data = json.load(json_file)

        input_files = []
        output_files = []
        regions_studied = []
        regions_called = []

        for analysis in data.get('analysis', []):
            # Input files (VCF, etc.)
            for input_item in analysis.get('input', []):
                file_ref = input_item.get('file', {}).get('reference')
                if file_ref:
                    input_files.append(self._build_file_url(file_ref))

            # Output files (VCF, etc.)
            for output in analysis.get('output', []):
                file_ref = output.get('file', {}).get('reference')
                if file_ref:
                    output_files.append(self._build_file_url(file_ref))

            # Regions studied (BED files)
            for region in analysis.get('regionsStudied', []):
                ref = region.get('reference')
                if ref:
                    regions_studied.append(self._build_file_url(ref))

            # Regions called (BED files)
            for region in analysis.get('regionsCalled', []):
                ref = region.get('reference')
                if ref:
                    regions_called.append(self._build_file_url(ref))

        self.files = {
            'input_files': list(dict.fromkeys(input_files)),
            'output_files': list(dict.fromkeys(output_files)),
            'regions_studied': list(dict.fromkeys(regions_studied)),
            'regions_called': list(dict.fromkeys(regions_called))
        }

        return self.files

    def _build_file_url(self, reference):
        """Build full API URL from a FHIR reference."""
        if self.api_link:
            return f"{self.api_link.rstrip('/')}/{reference}"
        return reference
