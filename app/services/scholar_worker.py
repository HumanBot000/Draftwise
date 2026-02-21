from PySide6.QtCore import QObject, Signal, Slot
from scholarly import scholarly

class ScholarWorker(QObject):
    results_ready = Signal(list)
    search_failed = Signal(str)

    def __init__(self, query):
        super().__init__()
        self.query = query

    @Slot()
    def run(self):
        try:
            search_results = scholarly.search_pubs(self.query)
            # Limit results to avoid overwhelming the user and the UI
            results = [pub for i, pub in enumerate(search_results) if i < 20]
            self.results_ready.emit(results)
        except Exception as e:
            self.search_failed.emit(str(e))
