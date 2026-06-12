"""
BibTeX file manager for handling bibliography
"""

from typing import List, Dict, Optional, Any
from pathlib import Path
import re
from loguru import logger

try:
    import bibtexparser
except ImportError:
    bibtexparser = None
    logger.warning("bibtexparser not installed")


class BibTexManager:
    """Manage BibTeX files and entries"""
    
    def __init__(self):
        """Initialize BibTeX manager"""
        self.entries: List[Dict[str, Any]] = []
        if bibtexparser is None:
            logger.warning("bibtexparser not available")
    
    def load_bibtex_file(self, file_path: str) -> bool:
        """
        Load entries from BibTeX file
        
        Args:
            file_path: Path to .bib file
            
        Returns:
            True if successful
        """
        if bibtexparser is None:
            logger.error("bibtexparser is not installed")
            return False
        
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse BibTeX content
            database = bibtexparser.loads(content)
            
            # Extract entries
            for entry in database.entries:
                self.entries.append(self._entry_to_dict(entry))
            
            logger.info(f"Loaded {len(self.entries)} entries from {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error loading BibTeX file: {e}")
            return False
    
    def save_bibtex_file(self, file_path: str) -> bool:
        """
        Save entries to BibTeX file
        
        Args:
            file_path: Path to save .bib file
            
        Returns:
            True if successful
        """
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            bibtex_content = []
            
            for entry in self.entries:
                bibtex_entry = self._dict_to_entry(entry)
                bibtex_content.append(bibtex_entry)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(bibtex_content))
            
            logger.info(f"Saved {len(self.entries)} entries to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving BibTeX file: {e}")
            return False
    
    def add_entry(self, entry_data: Dict[str, str]) -> None:
        """
        Add a new entry
        
        Args:
            entry_data: Entry data dictionary
        """
        required_fields = ['entry_type', 'key']
        
        if not all(field in entry_data for field in required_fields):
            logger.warning("Missing required fields in entry")
            return
        
        self.entries.append(entry_data)
        logger.info(f"Added entry: {entry_data.get('key')}")
    
    def remove_entry(self, key: str) -> bool:
        """
        Remove an entry by key
        
        Args:
            key: Entry key to remove
            
        Returns:
            True if successful
        """
        for i, entry in enumerate(self.entries):
            if entry.get('key') == key:
                self.entries.pop(i)
                logger.info(f"Removed entry: {key}")
                return True
        
        logger.warning(f"Entry not found: {key}")
        return False
    
    def get_entry(self, key: str) -> Optional[Dict]:
        """
        Get an entry by key
        
        Args:
            key: Entry key
            
        Returns:
            Entry dictionary or None
        """
        for entry in self.entries:
            if entry.get('key') == key:
                return entry
        
        return None
    
    def search_entries(self, query: str, field: str = 'title') -> List[Dict]:
        """
        Search entries by field
        
        Args:
            query: Search query
            field: Field to search in
            
        Returns:
            List of matching entries
        """
        results = []
        
        query_lower = query.lower()
        
        for entry in self.entries:
            if field in entry:
                if query_lower in str(entry[field]).lower():
                    results.append(entry)
        
        return results
    
    def get_all_entries(self) -> List[Dict]:
        """Get all entries"""
        return self.entries.copy()
    
    def get_entry_count(self) -> int:
        """Get total number of entries"""
        return len(self.entries)
    
    def validate_entry(self, entry: Dict) -> Tuple[bool, List[str]]:
        """
        Validate entry format
        
        Args:
            entry: Entry to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        required = ['entry_type', 'key']
        for field in required:
            if field not in entry:
                errors.append(f"Missing required field: {field}")
        
        # Check entry types
        valid_types = [
            'article', 'book', 'inproceedings', 'conference',
            'thesis', 'phdthesis', 'mastersthesis', 'techreport',
            'misc', 'website', 'online'
        ]
        
        if entry.get('entry_type', '').lower() not in valid_types:
            errors.append(f"Invalid entry type: {entry.get('entry_type')}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def _entry_to_dict(entry) -> Dict:
        """Convert BibTeX entry to dictionary"""
        result = {
            'entry_type': entry.entry_type,
            'key': entry.key
        }
        
        for field, value in entry.fields_dict.items():
            result[field.lower()] = value
        
        return result
    
    @staticmethod
    def _dict_to_entry(entry_dict: Dict) -> str:
        """Convert dictionary to BibTeX entry string"""
        entry_type = entry_dict.get('entry_type', 'article')
        key = entry_dict.get('key', 'unknown')
        
        lines = [f"@{entry_type}{{{key},"]
        
        for field, value in entry_dict.items():
            if field not in ['entry_type', 'key']:
                lines.append(f"  {field} = {{{value}}},")
        
        # Remove trailing comma from last line
        if lines[-1].endswith(','):
            lines[-1] = lines[-1][:-1]
        
        lines.append("}")
        
        return '\n'.join(lines)
    
    def import_from_json(self, json_data: List[Dict]) -> int:
        """
        Import entries from JSON format
        
        Args:
            json_data: List of entry dictionaries
            
        Returns:
            Number of imported entries
        """
        try:
            count = 0
            for entry in json_data:
                if self.validate_entry(entry)[0]:
                    self.add_entry(entry)
                    count += 1
            
            return count
        except Exception as e:
            logger.error(f"Error importing from JSON: {e}")
            return 0
    
    def export_to_json(self) -> List[Dict]:
        """
        Export all entries to JSON format
        
        Returns:
            List of entries as dictionaries
        """
        return self.entries.copy()
