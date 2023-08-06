from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.namespace import *
from openbiolink.nodeType import NodeType


class InMetaOntoDoIsA(InfileMetadata):
    CSV_NAME = "DB_ONTO_DO_IS_A_ontology.csv"
    USE_COLS = ["ID", "IS_A"]
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = None
    SOURCE = "DO"
    NODE1_TYPE = NodeType.DIS
    NODE1_NAMESPACE = Namespace(Namespaces.DIS)
    NODE2_TYPE = NodeType.DIS
    NODE2_NAMESPACE = Namespace(Namespaces.DIS)
    EDGE_TYPE = EdgeType.IS_A
    MAPPING_SEP = ";"
    INFILE_TYPE = InfileType.IN_ONTO_DO_IS_A

    def __init__(self):
        super().__init__(csv_name=self.CSV_NAME, cols=self.USE_COLS, infileType=self.INFILE_TYPE)
