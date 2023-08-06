from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.namespace import *
from openbiolink.nodeType import NodeType


class InMetaEdgeStringBindInh(InfileMetadata):
    CSV_NAME = "DB_STRING_gene_bindInh_gene.csv"
    USE_COLS = ["item_id_a", "item_id_b", "score"]
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    SOURCE = "STRING"
    NODE1_TYPE = NodeType.GENE
    NODE1_NAMESPACE = Namespace(Namespaces.ENSEMBL, False, mapping={"9606.": ""})
    NODE2_TYPE = NodeType.GENE
    NODE2_NAMESPACE = Namespace(Namespaces.ENSEMBL, False, mapping={"9606.": ""})
    EDGE_TYPE = EdgeType.GENE_BINDINH_GENE
    INFILE_TYPE = InfileType.IN_EDGE_STRING_BINDINH

    MAPPING_SEP = None

    def __init__(self):
        super().__init__(csv_name=self.CSV_NAME, cols=self.USE_COLS, infileType=self.INFILE_TYPE)
