import os

from openbiolink.graph_creation import graphCreationConfig as g
from openbiolink.graph_creation.file_reader.csvReader import CsvReader
from openbiolink.graph_creation.metadata_db_file.edge.dbMetaEdgeHpoDis import DbMetaEdgeHpoDis
from openbiolink.graph_creation.types.dbType import DbType
from openbiolink.graph_creation.types.readerType import ReaderType


class EdgeHpoDisReader(CsvReader):
    DB_META_CLASS = DbMetaEdgeHpoDis

    def __init__(self):
        super().__init__(
            in_path=os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
            sep=None,
            cols=self.DB_META_CLASS.COLS,
            use_cols=self.DB_META_CLASS.FILTER_COLS,
            nr_lines_header=self.DB_META_CLASS.HEADER,
            dtypes={col_name: "str" for col_name in self.DB_META_CLASS.FILTER_COLS},
            readerType=ReaderType.READER_EDGE_HPO_DIS,
            dbType=DbType.DB_EDGE_HPO_DIS,
        )
