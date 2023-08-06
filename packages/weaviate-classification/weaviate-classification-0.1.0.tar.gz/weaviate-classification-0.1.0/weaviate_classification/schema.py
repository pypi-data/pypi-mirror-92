""" This module creates a Weaviate schema from a data configuration file """

from .utilities import get_reference_property_name_from_field
from .utilities import get_reference_class_name_from_field


def _create_default_schema(config):

    # Initialize the return value
    schema = None

    if config is not None and 'classes' in config:

        # Add the default emppty list for classes to the schema
        schema = {}
        schema['classes'] = []

    return schema


def _create_property_from_column(col):
    prop = None

    if col is not None:
        prop = {}
        prop['name'] = col['name']
        prop['dataType'] = [col['type']]
        prop['description'] = col['name']
        prop['indexInverted'] = col['indexInverted']
        prop['moduleConfig'] = {}
        prop['moduleConfig']['text2vec-contextionary'] = {}
        prop['moduleConfig']['text2vec-contextionary']['skip'] = not prop['indexInverted']
        prop['moduleConfig']['text2vec-contextionary']['vectorizePropertyName'] = False

    return prop


def _create_reference_property_from_column(col):
    prop = None

    if col is not None:
        prop = {}
        prop['name'] = get_reference_property_name_from_field(col['name'])
        prop['dataType'] = [get_reference_class_name_from_field(col['name'])]
        prop['description'] = prop['dataType'][0]
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig']['text2vec-contextionary'] = {}
        prop['moduleConfig']['text2vec-contextionary']['skip'] = False
        prop['moduleConfig']['text2vec-contextionary']['vectorizePropertyName'] = False

    return prop


def _create_class_from_column(col):
    newclass = None

    if col is not None:
        newclass = {}
        newclass['class'] = get_reference_class_name_from_field(col['name'])
        newclass['description'] = newclass['class']
        newclass['moduleConfig'] = {}
        newclass['moduleConfig']['text2vec-contextionary'] = {}
        newclass['moduleConfig']['text2vec-contextionary']['vectorizeClassName'] = False
        newclass['properties'] = []
        prop = {}
        prop['name'] = 'name'
        prop['dataType'] = ["string"]
        prop['description'] = "Name of this instance of this class"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig']['text2vec-contextionary'] = {}
        prop['moduleConfig']['text2vec-contextionary']['skip'] = True
        prop['moduleConfig']['text2vec-contextionary']['vectorizePropertyName'] = False
        newclass['properties'].append(prop)

    return newclass


def _add_default_properties_to_mainclass(mainclass):

    if mainclass is not None:

        # the row proporty indicates the row number from the excel file that the data point was on
        prop = {}
        prop['name'] = 'row'
        prop['dataType'] = ["int"]
        prop['description'] = "The row number of the data point"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig']['text2vec-contextionary'] = {}
        prop['moduleConfig']['text2vec-contextionary']['skip'] = True
        prop['moduleConfig']['text2vec-contextionary']['vectorizePropertyName'] = False
        mainclass['properties'].append(prop)

        # the validated property indicates whether this data point can be used for training
        prop = {}
        prop['name'] = 'validated'
        prop['dataType'] = ["boolean"]
        prop['description'] = "Indicates whether this data point can be used for training purposes"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig']['text2vec-contextionary'] = {}
        prop['moduleConfig']['text2vec-contextionary']['skip'] = True
        prop['moduleConfig']['text2vec-contextionary']['vectorizePropertyName'] = False
        mainclass['properties'].append(prop)

        # the batchnumber property is used if the number of items to be classified exceeds the max
        prop = {}
        prop['name'] = 'batchNumber'
        prop['dataType'] = ["int"]
        prop['description'] = "Indicates the batch number if batching is used"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig']['text2vec-contextionary'] = {}
        prop['moduleConfig']['text2vec-contextionary']['skip'] = True
        prop['moduleConfig']['text2vec-contextionary']['vectorizePropertyName'] = False
        mainclass['properties'].append(prop)


def create_schema_from_data_configuration(config):
    """ create schema """

    # Initialize the return value
    schema = None

    # keep track of which classes for entities have been created
    entities = []

    # Create the schema from the data_configuration file
    if config is not None:
        schema = _create_default_schema(config)

        if schema is not None:
            for dataclass in config['classes']:
                # Add the main class to the schema
                mainclass = {}
                mainclass['class'] = dataclass['classname']
                mainclass['moduleConfig'] = {}
                mainclass['moduleConfig']['text2vec-contextionary'] = {}
                mainclass['moduleConfig']['text2vec-contextionary']['vectorizeClassName'] = False
                mainclass['description'] = "The class in this classification setup"
                mainclass['properties'] = []
                _add_default_properties_to_mainclass(mainclass)
                schema['classes'].append(mainclass)

                for col in dataclass['columns']:

                    # Create the property and add it to the schema
                    prop = _create_property_from_column(col)
                    if prop is not None:
                        mainclass['properties'].append(prop)

                    # If the column represents an entity we need to create a reference property and a new class
                    if col['entity']:
                        prop = _create_reference_property_from_column(col)
                        if prop is not None:
                            mainclass['properties'].append(prop)

                        if col['name'] not in entities:
                            entities.append(col['name'])
                            newclass = _create_class_from_column(col)
                            if newclass is not None:
                                schema['classes'].append(newclass)

    return schema
