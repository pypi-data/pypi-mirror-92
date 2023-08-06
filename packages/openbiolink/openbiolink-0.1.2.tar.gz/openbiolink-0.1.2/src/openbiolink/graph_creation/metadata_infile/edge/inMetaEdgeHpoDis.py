from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.namespace import *
from openbiolink.nodeType import NodeType


class InMetaEdgeHpoDis(InfileMetadata):
    CSV_NAME = "DB_HPO_disease_phenotype.csv"
    USE_COLS = ["DOI", "HPO_ID", "evidence_code"]
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    SOURCE = "HPO"
    NODE1_TYPE = NodeType.DIS
    NODE1_NAMESPACE = Namespace(Namespaces.MULTI, mapping={"OMIM": "MIM", "PMID": "PUBMED"})
    NODE2_TYPE = NodeType.PHENOTYPE
    NODE2_NAMESPACE = Namespace(Namespaces.HPO)
    EDGE_TYPE = EdgeType.DIS_PHENOTYPE
    INFILE_TYPE = InfileType.IN_EDGE_HPO_DIS

    MAPPING_SEP = None

    def __init__(self):
        super().__init__(
            csv_name=InMetaEdgeHpoDis.CSV_NAME, cols=self.USE_COLS, infileType=InMetaEdgeHpoDis.INFILE_TYPE
        )
