import os

from openbiolink.graph_creation import graphCreationConfig as glob
from openbiolink.graph_creation.metadata_edge.edgeRegularMetadata import EdgeRegularMetadata
from openbiolink.graph_creation.metadata_infile import InMetaEdgeStringBinding
from openbiolink.graph_creation.metadata_infile.mapping.inMetaMapString import InMetaMapString
from openbiolink.graph_creation.types.qualityType import QualityType


class EdgeMetaGeneBindingGene(EdgeRegularMetadata):
    NAME = "Edge - Gene_binding_Gene"

    LQ_CUTOFF = 0
    MQ_CUTOFF = 400
    HQ_CUTOFF = 700

    EDGE_INMETA_CLASS = InMetaEdgeStringBinding
    MAP1_META_CLASS = InMetaMapString

    def __init__(self, quality: QualityType = None):
        edges_file_path = os.path.join(glob.IN_FILE_PATH, self.EDGE_INMETA_CLASS.CSV_NAME)
        mapping_file1 = os.path.join(glob.IN_FILE_PATH, self.MAP1_META_CLASS.CSV_NAME)
        super().__init__(
            is_directional=False,
            edges_file_path=edges_file_path,
            source=self.EDGE_INMETA_CLASS.SOURCE,
            colindex1=self.EDGE_INMETA_CLASS.NODE1_COL,
            colindex2=self.EDGE_INMETA_CLASS.NODE2_COL,
            edgeType=self.EDGE_INMETA_CLASS.EDGE_TYPE,
            node1_type=self.EDGE_INMETA_CLASS.NODE1_TYPE,
            node1_namespace=self.EDGE_INMETA_CLASS.NODE1_NAMESPACE,
            node2_type=self.EDGE_INMETA_CLASS.NODE2_TYPE,
            node2_namespace=self.EDGE_INMETA_CLASS.NODE2_NAMESPACE,
            colindex_qscore=self.EDGE_INMETA_CLASS.QSCORE_COL,
            quality=quality,
            mapping1_file=mapping_file1,
            mapping1_targetnamespace=self.MAP1_META_CLASS.TARGET_NAMESPACE,
            map1_sourceindex=self.MAP1_META_CLASS.SOURCE_COL,
            map1_targetindex=self.MAP1_META_CLASS.TARGET_COL,
            mapping2_file=mapping_file1,
            mapping2_targetnamespace=self.MAP1_META_CLASS.TARGET_NAMESPACE,
            map2_sourceindex=self.MAP1_META_CLASS.SOURCE_COL,
            map2_targetindex=self.MAP1_META_CLASS.TARGET_COL,
        )
