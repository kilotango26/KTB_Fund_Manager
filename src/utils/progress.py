"""
Progress tracking utilities for KTB Fund Manager.
"""

from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console

console = Console()


class ProgressTracker:
    """Simple progress tracker for agent operations."""
    
    def __init__(self):
        self.progress = None
        self.task_id = None
    
    def start(self, description: str = "Running hedge fund analysis..."):
        """Start progress tracking."""
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]{task.description}"),
            console=console,
        )
        self.task_id = self.progress.add_task(description, total=None)
        self.progress.start()
    
    def stop(self):
        """Stop progress tracking."""
        if self.progress:
            self.progress.stop()
            self.progress = None
            self.task_id = None
    
    def update(self, description: str):
        """Update progress description."""
        if self.progress and self.task_id is not None:
            self.progress.update(self.task_id, description=description)


# Global progress instance
progress = ProgressTracker()
