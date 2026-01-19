from src.TablaManager import TablaManager
class DocumentosManager(TablaManager):

    def __init__(self, db_manager) -> None:
        super().__init__("documentos", db_manager)