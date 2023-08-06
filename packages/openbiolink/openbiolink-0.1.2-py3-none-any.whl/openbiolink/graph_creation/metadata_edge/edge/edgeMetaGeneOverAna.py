import os

from openbiolink.graph_creation import graphCreationConfig as glob
from openbiolink.graph_creation.metadata_edge.edgeRegularMetadata import EdgeRegularMetadata
from openbiolink.graph_creation.metadata_infile import InMetaEdgeBgeeOverExpr, InMetaMapOntoUberonAltid
from openbiolink.graph_creation.metadata_infile.mapping.inMetaMapUniEnsNcbi import InMetaMapUniEnsNcbi
from openbiolink.graph_creation.types.qualityType import QualityType


class EdgeMetaGeneOverAna(EdgeRegularMetadata):
    NAME = "Edge - Gene_overExpression_Anatomy"

    LQ_CUTOFF_TEXT = None
    MQ_CUTOFF_TEXT = None
    HQ_CUTOFF_TEXT = ["low quality"]

    EDGE_INMETA_CLASS = InMetaEdgeBgeeOverExpr
    MAP1_META_CLASS = InMetaMapUniEnsNcbi
    MAP2_ALT_ID_META_CLASS = InMetaMapOntoUberonAltid

    def __init__(self, quality: QualityType = None):
        edges_file_path = os.path.join(glob.IN_FILE_PATH, self.EDGE_INMETA_CLASS.CSV_NAME)
        mapping_file1 = os.path.join(glob.IN_FILE_PATH, self.MAP1_META_CLASS.CSV_NAME)
        altid_mapping2_file = os.path.join(glob.IN_FILE_PATH, self.MAP2_ALT_ID_META_CLASS.CSV_NAME)
        super().__init__(
            is_directional=True,
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
            altid_mapping2_file=altid_mapping2_file,
            altid_mapping2_targetnamespace=self.MAP2_ALT_ID_META_CLASS.TARGET_NAMESPACE,
            altid_map2_sourceindex=self.MAP2_ALT_ID_META_CLASS.SOURCE_COL,
            altid_map2_targetindex=self.MAP2_ALT_ID_META_CLASS.TARGET_COL,
        )
