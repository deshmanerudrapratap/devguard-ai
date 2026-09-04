from scanners.base import BaseScanner, ScanRequest, ScanResult


class PlaceholderScanner(BaseScanner):
    scanner_id = "placeholder"

    def scan(self, request: ScanRequest) -> ScanResult:
        return ScanResult(
            scanner_id=self.scanner_id,
            implemented=False,
            message="No scanners are implemented in the foundation stage.",
            findings=[],
        )
