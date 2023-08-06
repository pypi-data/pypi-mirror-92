from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.namespace import *
from openbiolink.nodeType import NodeType


class InMetaEdgeDisGeNet(InfileMetadata):
    CSV_NAME = "DB_DisGeNet_gene_disease.csv"
    USE_COLS = ["geneID", "umlsID", "score"]
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    SOURCE = "DisGeNet"
    NODE1_TYPE = NodeType.GENE
    NODE1_NAMESPACE = Namespace(Namespaces.NCBI, False)
    NODE2_TYPE = NodeType.DIS
    NODE2_NAMESPACE = Namespace(Namespaces.UMLS, False)
    EDGE_TYPE = EdgeType.GENE_DIS
    INFILE_TYPE = InfileType.IN_EDGE_DISGENET
    MAPPING_SEP = None

    def __init__(self):
        super().__init__(
            csv_name=InMetaEdgeDisGeNet.CSV_NAME, cols=self.USE_COLS, infileType=InMetaEdgeDisGeNet.INFILE_TYPE
        )
