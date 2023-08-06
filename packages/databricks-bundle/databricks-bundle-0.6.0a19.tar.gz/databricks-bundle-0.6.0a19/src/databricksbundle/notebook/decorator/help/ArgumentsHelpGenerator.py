from typing import List
from databricksbundle.help.HtmlDescriptionProvider import HtmlDescriptionProvider

class ArgumentsHelpGenerator:

    def __init__(
        self,
        popularServices: List[HtmlDescriptionProvider]
    ):
        self._popularServices = popularServices

    def generate(self):
        args = self._getBase()

        for popularService in self._popularServices:
            className = popularService.__class__.__name__
            variableName = className[0].lower() + className[1:]

            arg = {
                'argument': f'{variableName}: {className}',
                'import': f'from {popularService.__module__} import {className}',
                'description': popularService.getHtmlDescription(),
            }

            args.append(arg)

        return self._getHtml(args)

    def _getBase(self):
        return [
            {
                'argument': 'spark: SparkSession',
                'import': 'from pyspark.sql.session import SparkSession',
            },
            {
                'argument': 'dbutils: DBUtils',
                'import': 'from pyspark.dbutils import DBUtils',
            },
            {
                'argument': 'logger: Logger',
                'import': 'from logging import Logger',
                'description': 'standard Python logger'
            },
        ]

    def _getHtml(self, args: list):
        def createRow(arg, index: int):
            if (index % 2) == 0:
                backgroundColor = "f7f7f7"
            else:
                backgroundColor = "#fff"

            return f'''<tr style="background-color: {backgroundColor}">
                <td style="font-family: 'Courier New', monospace; font-size: 14px; width: 25%; padding: 5px">{arg["argument"]}</td>
                <td style="font-family: 'Courier New', monospace; font-size: 14px; padding: 5px">{arg["import"]}</td>
                <td style="font-size: 14px; padding: 5px">{arg["description"] if "description" in arg else ""}</td>
            </tr>'''

        tableRows = [createRow(arg, index) for index, arg in enumerate(args)]
        headers = ['argument', 'import', 'description']
        tableHead = '<thead style="text-align: left; font-size: 14px"><th>' + '</th><th>'.join(headers) + '</th></thead>'

        return '<table width="100%">' + tableHead + '<tbody>' + ''.join(tableRows) + '</tbody></table>'
