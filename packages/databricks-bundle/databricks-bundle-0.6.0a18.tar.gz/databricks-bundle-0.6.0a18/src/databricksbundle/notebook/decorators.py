# pylint: disable = unused-import
from databricksbundle.notebook.decorator.notebookFunction import notebookFunction
from databricksbundle.etl.dataFrameLoader import dataFrameLoader
from databricksbundle.etl.transformation import transformation
from databricksbundle.etl.dataFrameSaver import dataFrameSaver

def tableParams(identifier: str):
    return f'%datalakebundle.tables."{identifier}".params%'
