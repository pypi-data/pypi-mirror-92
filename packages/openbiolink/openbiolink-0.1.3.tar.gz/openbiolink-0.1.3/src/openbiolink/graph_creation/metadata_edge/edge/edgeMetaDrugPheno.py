import os

from openbiolink.graph_creation import graphCreationConfig as glob
from openbiolink.graph_creation.metadata_edge.edgeRegularMetadata import EdgeRegularMetadata
from openbiolink.graph_creation.metadata_infile import InMetaMapOntoHpoAltid
from openbiolink.graph_creation.metadata_infile.edge.inMetaEdgeSiderSe import InMetaEdgeSiderSe
from openbiolink.graph_creation.metadata_infile.mapping.inMetaMapOntoHpoUmls import InMetaMapOntoHpoUmls
from openbiolink.graph_creation.types.qualityType import QualityType


class EdgeMetaDrugPheno(EdgeRegularMetadata):
    NAME = "Edge - Drug_sideEffect_Phenotype"

    EDGE_INMETA_CLASS = InMetaEdgeSiderSe
    MAP2_META_CLASS = InMetaMapOntoHpoUmls
    MAP2_ALT_ID_META_CLASS = InMetaMapOntoHpoAltid

    def __init__(self, quality: QualityType = None):
        edges_file_path = os.path.join(glob.IN_FILE_PATH, self.EDGE_INMETA_CLASS.CSV_NAME)
        mapping_file2 = os.path.join(glob.IN_FILE_PATH, self.MAP2_META_CLASS.CSV_NAME)
        altid_mapping_file2 = os.path.join(glob.IN_FILE_PATH, self.MAP2_ALT_ID_META_CLASS.CSV_NAME)

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
            mapping2_file=mapping_file2,
            mapping2_targetnamespace=self.MAP2_META_CLASS.TARGET_NAMESPACE,
            map2_sourceindex=self.MAP2_META_CLASS.SOURCE_COL,
            map2_targetindex=self.MAP2_META_CLASS.TARGET_COL,
            altid_mapping2_file=altid_mapping_file2,
            altid_mapping2_targetnamespace=self.MAP2_ALT_ID_META_CLASS.TARGET_NAMESPACE,
            altid_map2_sourceindex=self.MAP2_ALT_ID_META_CLASS.SOURCE_COL,
            altid_map2_targetindex=self.MAP2_ALT_ID_META_CLASS.TARGET_COL,
        )
