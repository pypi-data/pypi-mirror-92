from databricksbundle.notebook.decorator.ContainerManager import ContainerManager
from databricksbundle.notebook.decorator.help.ArgumentsHelpGenerator import ArgumentsHelpGenerator
from databricksbundle.notebook.ipython import userNamespace

def show():
    displayHTML = userNamespace.getValue('displayHTML') # pylint: disable = invalid-name
    argumentsHelpGenerator: ArgumentsHelpGenerator = ContainerManager.getContainer().get(ArgumentsHelpGenerator)

    displayHTML(argumentsHelpGenerator.generate())
