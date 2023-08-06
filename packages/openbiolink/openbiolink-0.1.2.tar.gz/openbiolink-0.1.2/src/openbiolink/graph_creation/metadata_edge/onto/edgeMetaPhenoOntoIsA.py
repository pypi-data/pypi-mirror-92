import os

from openbiolink.graph_creation import graphCreationConfig as glob
from openbiolink.graph_creation.metadata_edge.edgeOntoMetadata import EdgeOntoMetadata
from openbiolink.graph_creation.metadata_infile.onto.inMetaOntoHpoIsA import InMetaOntoHpoIsA


class EdgeMetaPhenoOntoIsA(EdgeOntoMetadata):
    NAME = "Onto - Phenotype_isA_Phenotype"

    EDGE_INMETA_CLASS = InMetaOntoHpoIsA

    def __init__(self, quality=None):
        super().__init__(
            is_directional=True,
            edges_file_path=os.path.join(glob.IN_FILE_PATH, self.EDGE_INMETA_CLASS.CSV_NAME),
            source=self.EDGE_INMETA_CLASS.SOURCE,
            colindex1=self.EDGE_INMETA_CLASS.NODE1_COL,
            colindex2=self.EDGE_INMETA_CLASS.NODE2_COL,
            edgeType=self.EDGE_INMETA_CLASS.EDGE_TYPE,
            node1_type=self.EDGE_INMETA_CLASS.NODE1_TYPE,
            node1_namespace=self.EDGE_INMETA_CLASS.NODE1_NAMESPACE,
            node2_type=self.EDGE_INMETA_CLASS.NODE2_TYPE,
            node2_namespace=self.EDGE_INMETA_CLASS.NODE2_NAMESPACE,
        )
