"""
Project manager for handling .project files
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from loguru import logger

from core.document import Document


class ProjectManager:
    """Manages project files (.project format)"""
    
    PROJECT_VERSION = "1.0"
    PROJECT_EXTENSION = ".project"
    
    def __init__(self):
        """Initialize project manager"""
        pass
    
    @staticmethod
    def create_project(
        title: str,
        author: str = "",
        project_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Create a new project structure
        
        Args:
            title: Project title
            author: Project author
            project_dir: Project directory (uses temp if not specified)
            
        Returns:
            Project metadata dictionary
        """
        if project_dir is None:
            project_dir = Path.home() / ".persian_doc_editor" / "projects"
        
        project_dir = Path(project_dir)
        project_dir.mkdir(parents=True, exist_ok=True)
        
        project = {
            'version': ProjectManager.PROJECT_VERSION,
            'title': title,
            'author': author,
            'created_at': datetime.now().isoformat(),
            'modified_at': datetime.now().isoformat(),
            'project_dir': str(project_dir),
            'document': None,
            'files': [],
            'settings': {},
            'references': []
        }
        
        logger.info(f"Project created: {title}")
        return project
    
    @staticmethod
    def save_project(
        project: Dict[str, Any],
        file_path: str,
        document: Optional[Document] = None
    ) -> bool:
        """
        Save project to file
        
        Args:
            project: Project metadata
            file_path: Path to save project file
            document: Document to save (optional)
            
        Returns:
            True if successful
        """
        try:
            project_data = project.copy()
            project_data['modified_at'] = datetime.now().isoformat()
            
            if document:
                project_data['document'] = document.to_dict()
            
            file_path = Path(file_path)
            if not str(file_path).endswith(ProjectManager.PROJECT_EXTENSION):
                file_path = file_path.with_suffix(ProjectManager.PROJECT_EXTENSION)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Project saved: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save project: {e}")
            return False
    
    @staticmethod
    def load_project(file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load project from file
        
        Args:
            file_path: Path to project file
            
        Returns:
            Project metadata or None if failed
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.error(f"Project file not found: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                project = json.load(f)
            
            logger.info(f"Project loaded: {file_path}")
            return project
        except Exception as e:
            logger.error(f"Failed to load project: {e}")
            return None
    
    @staticmethod
    def load_document_from_project(project: Dict[str, Any]) -> Optional[Document]:
        """
        Reconstruct document from project data
        
        Args:
            project: Project metadata
            
        Returns:
            Document object or None if no document data
        """
        try:
            if 'document' not in project or project['document'] is None:
                return None
            
            doc_data = project['document']
            doc = Document(title=doc_data['metadata']['title'])
            
            # Restore metadata
            doc.metadata.author = doc_data['metadata']['author']
            doc.metadata.subject = doc_data['metadata']['subject']
            doc.metadata.keywords = doc_data['metadata']['keywords']
            doc.metadata.abstract = doc_data['metadata']['abstract']
            
            # Restore paragraphs
            for para_data in doc_data.get('paragraphs', []):
                para = doc.add_paragraph(para_data['text'])
                # Restore formatting if needed
            
            # Restore figures, tables, references
            doc.figures = doc_data.get('figures', [])
            doc.tables = doc_data.get('tables', [])
            doc.references = doc_data.get('references', [])
            
            logger.info(f"Document loaded from project")
            return doc
        except Exception as e:
            logger.error(f"Failed to load document from project: {e}")
            return None
    
    @staticmethod
    def add_file_to_project(
        project: Dict[str, Any],
        file_path: str,
        description: str = ""
    ) -> None:
        """
        Add a file reference to project
        
        Args:
            project: Project metadata
            file_path: Path to file
            description: File description
        """
        file_entry = {
            'path': str(file_path),
            'name': Path(file_path).name,
            'description': description,
            'added_at': datetime.now().isoformat()
        }
        
        if 'files' not in project:
            project['files'] = []
        
        project['files'].append(file_entry)
        logger.info(f"File added to project: {file_path}")
    
    @staticmethod
    def list_project_files(project: Dict[str, Any]) -> list:
        """Get list of files in project"""
        return project.get('files', [])
    
    @staticmethod
    def export_project_as_template(
        project: Dict[str, Any],
        template_path: str
    ) -> bool:
        """
        Export project as a template for reuse
        
        Args:
            project: Project to export
            template_path: Path to save template
            
        Returns:
            True if successful
        """
        try:
            template_data = {
                'template_version': ProjectManager.PROJECT_VERSION,
                'title': project['title'],
                'author': project['author'],
                'settings': project.get('settings', {}),
                'created_at': datetime.now().isoformat()
            }
            
            template_path = Path(template_path)
            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Project exported as template: {template_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export template: {e}")
            return False
    
    @staticmethod
    def get_recent_projects(max_count: int = 10) -> list:
        """Get list of recent projects"""
        try:
            recent_file = Path.home() / ".persian_doc_editor" / "recent_projects.json"
            
            if recent_file.exists():
                with open(recent_file, 'r', encoding='utf-8') as f:
                    recent = json.load(f)
                    return recent[:max_count]
            
            return []
        except Exception as e:
            logger.error(f"Failed to get recent projects: {e}")
            return []
    
    @staticmethod
    def add_recent_project(project_path: str) -> None:
        """Add project to recent list"""
        try:
            recent_file = Path.home() / ".persian_doc_editor" / "recent_projects.json"
            recent_file.parent.mkdir(parents=True, exist_ok=True)
            
            recent = []
            if recent_file.exists():
                with open(recent_file, 'r', encoding='utf-8') as f:
                    recent = json.load(f)
            
            # Remove if already exists
            if project_path in recent:
                recent.remove(project_path)
            
            # Add to top
            recent.insert(0, project_path)
            
            # Keep only last 10
            recent = recent[:10]
            
            with open(recent_file, 'w', encoding='utf-8') as f:
                json.dump(recent, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to add recent project: {e}")
    
    @staticmethod
    def get_project_statistics(project: Dict[str, Any]) -> Dict[str, Any]:
        """Get statistics about a project"""
        doc = ProjectManager.load_document_from_project(project)
        
        stats = {
            'title': project['title'],
            'author': project['author'],
            'created_at': project['created_at'],
            'modified_at': project['modified_at'],
            'file_count': len(project.get('files', [])),
            'reference_count': len(project.get('references', []))
        }
        
        if doc:
            stats['paragraph_count'] = len(doc.paragraphs)
            stats['word_count'] = doc.get_word_count()
            stats['figure_count'] = len(doc.figures)
            stats['table_count'] = len(doc.tables)
        
        return stats
    
    def __repr__(self) -> str:
        return "ProjectManager()"
