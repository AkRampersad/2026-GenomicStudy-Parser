import json


class GenomicStudyParser:
    """Parses FHIR R5 GenomicStudy resources into structured analysis data."""

    def __init__(self):
        self.analyses = []

    def parse(self, input_path):
        """Parse a GenomicStudy JSON file and return extracted analyses."""
        with open(input_path, 'r') as f:
            data = json.load(f)

        patient_id = data.get('subject', {}).get('reference')
        analyses = []

        for analysis_data in data.get('analysis', []):
            analysis = {
                "patientID": patient_id,
                "analysisID": None,
                "analysisDate": analysis_data.get('date'),
                "specimenID": [],
                "genomicBuild": None,
                "studiedRegion": [],
                "dnaChangeType": [],
                "vcfFiles": []
            }

            # Extract analysis identifier
            for identifier in analysis_data.get('identifier', []):
                if identifier.get('value'):
                    analysis["analysisID"] = identifier.get('value')
                    break

            # Extract specimen references
            for specimen in analysis_data.get('specimen', []):
                ref = specimen.get('reference')
                if ref:
                    analysis["specimenID"].append(ref)

            # Extract genome build
            genome_build = analysis_data.get('genomeBuild', {})
            if genome_build:
                coding = genome_build.get('coding', [{}])[0]
                analysis["genomicBuild"] = coding.get('display') or coding.get('code')

            # Extract studied regions
            for region in analysis_data.get('regionsStudied', []):
                ref = region.get('reference')
                if ref:
                    analysis["studiedRegion"].append(ref)

            # Extract DNA change types
            for change_type in analysis_data.get('changeType', []):
                coding_list = change_type.get('coding', [])
                if coding_list:
                    analysis["dnaChangeType"].append(coding_list[0].get('display'))

            # Extract file references from outputs and inputs
            for output in analysis_data.get('output', []):
                file_ref = output.get('file', {}).get('reference')
                if file_ref:
                    analysis["vcfFiles"].append(file_ref)

            for input_item in analysis_data.get('input', []):
                file_ref = input_item.get('file', {}).get('reference')
                if file_ref:
                    analysis["vcfFiles"].append(file_ref)

            analyses.append(analysis)

        self.analyses = {"analyses": analyses}
        return self.analyses
