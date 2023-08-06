from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.namespace import *
from openbiolink.nodeType import NodeType


class InMetaOntoUberonPartOf(InfileMetadata):
    CSV_NAME = "DB_ONTO_UBERON_PART_OF_ontology.csv"
    USE_COLS = ["ID", "PART_OF"]
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = None
    SOURCE = "UBERON"
    NODE1_TYPE = NodeType.ANATOMY
    NODE1_NAMESPACE = Namespace(Namespaces.MULTI)
    NODE2_TYPE = NodeType.ANATOMY
    NODE2_NAMESPACE = Namespace(Namespaces.MULTI)
    EDGE_TYPE = EdgeType.PART_OF
    MAPPING_SEP = ";"
    INFILE_TYPE = InfileType.IN_ONTO_UBERON_PART_OF

    def __init__(self):
        super().__init__(csv_name=self.CSV_NAME, cols=self.USE_COLS, infileType=self.INFILE_TYPE)
