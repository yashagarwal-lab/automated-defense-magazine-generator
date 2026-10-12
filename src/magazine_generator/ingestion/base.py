from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pathlib import Path

class BaseIngestor(ABC):
    """Abstract base class for article ingestion sources."""

    @abstractmethod
    def ingest(self, source: Any) -> List[Dict[str, Any]]:
        """Ingest raw content and return normalized article records.

        Each returned dictionary must at minimum contain:
          - 'id': str
          - 'title': str
          - 'text': str (or 'body': list of str)
          - 'source': str
          - 'date': str (ISO YYYY-MM-DD)
          - 'url': str
        """
        pass
