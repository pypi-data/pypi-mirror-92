""" This module classifies data """

import json
import random
import math
import time
import weaviate
from .utilities import read_classification_configuration_file
from .utilities import get_weaviate_client
from .utilities import time_delay
from .utilities import calculate_size_training_set
from .data_configuration import read_data_configuration_file
from .schema import create_schema_from_data_configuration
from .parser import parse_data_file
from .imports import import_entities_to_weaviate
from .imports import import_datapoints_to_weaviate
from .imports import set_cross_references
from .classify import execute_classification
from .process_result import calculate_classification_score
from .process_result import write_classification_result
from .debug import debug_compare_datapoint_count
from .debug import debug_assert_eligible_for_classification



class Classification:
    """ A clasification validation module """

    def __init__(self):

        # Read the classification configuration file
        self.config = read_classification_configuration_file()
        self.datapath = None
        self.schema = None


    def read_data_configuration(self, path=None):
        """ read the data configuration file """

        # initialize the return value
        dataconfiguration = None

        if self.config is not None:

            # Read the data configuration file: how is the data stored in the excel file
            if path is not None:
                filename = path
            else:
                if 'data_configuration' in self.config and 'config' in self.config['data_configuration']:
                    filename = self.config['data_configuration']['config']
                else:
                    print("Error: no data configuration file given!")

            # Read the data configuration file
            print("Reading data configuration file -------:", filename)
            dataconfiguration = read_data_configuration_file(filename)

            if dataconfiguration is None or dataconfiguration == {}:
                print("Error reading the data config file ----:", filename)

        else:
            print("Error: unable to read config file -----!")

        return dataconfiguration


    def create_schema(self, dataconfiguration):
        """ create schema """

        # Initialize the return value
        self.schema = create_schema_from_data_configuration(dataconfiguration)

        # Write the schema to a file in the .schema directory
        schemapath = './schema/schema.json'
        with open(schemapath, 'w+', encoding='utf-8') as file:
            json.dump(self.schema, file, indent=4)

        return self.schema


    def load_schema(self, schemapath=None):
        """ load schema """

        # get the Weaviate client
        client = get_weaviate_client(self.config)

        # Import the schema if there is not a schema already in Weaviate
        if client is not None and not client.schema.contains():
            if schemapath is None:
                client.schema.create(self.schema)
            else:
                client.schema.create(schemapath)


    def parse_data(self, dataconfiguration, path=None):
        """ parse the data """

        # initialize the return value
        data = None

        # check if the path is specified as argument, or should be read from the config file
        if path is not None:
            self.datapath = path
        else:
            # Read the path to the data file from the config file
            if self.config is not None and 'data_configuration' in self.config:
                if 'data_path' in self.config['data_configuration']:
                    self.datapath = self.config['data_configuration']['data_path']

        data = parse_data_file(dataconfiguration, self.datapath)
        if data is None:
            print("Error: unable to read data file -------:")
        else:
            print("Reading data file ---------------------:", self.datapath)
            print("Number of data records parsed ---------:", data['count'])

        return data


    def import_entities(self, entities):
        """  import entities """

        # get the Weaviate client
        client = get_weaviate_client(self.config)

        if self.config is not None and client is not None:
            # First import the entities
            import_entities_to_weaviate(client, entities)


    def import_datapoints(self, dataconfiguration, datapoints, validated=True):
        """ import the data """

        # get the Weaviate client
        client = get_weaviate_client(self.config)

        if self.config is not None and client is not None:

            # Then import the datapoints
            import_datapoints_to_weaviate(client, dataconfiguration, datapoints, validated)


    def select_training_data(self, data):
        """ select the training data """

        if data is not None and self.config is not None:
            size = calculate_size_training_set(self.config, data)

            count = total = 0
            for point in data['datapoints']:

                count += 1
                total += 1
                if size['random_selection']:
                    # pick a random number and see if this is control group or training group
                    if random.uniform(0, 100) < size['validation_percentage']:
                        training = False
                    else:
                        training = True
                else:
                    # if count equals the modulus, this is control data
                    if count == size['modulus']:
                        training = False
                        count = 0
                    else:
                        training = True

                if training:
                    point['validated'] = True
                    size['training_size'] += 1
                else:
                    point['validated'] = False
                    size['validation_size'] += 1

            print("Total number of datapoints ------------:", size['total'])
            print("Validation percentage -----------------:", size['validation_percentage'])
            print("Random selection of validation sample -:", size['random_selection'])
            print("Number of datapoints in training ------:", size['training_size'])
            print("Number of datapoints in validation ----:", size['validation_size'])


    def set_cross_references(self, dataconfiguration, datapoints, entities):
        """ set the cross references """

        # Short time delay to make sure everything is imported before we start setting cross references
        time_delay(self.config)

        # get the Weaviate client
        client = get_weaviate_client(self.config)

        if client is not None and dataconfiguration is not None:
            set_cross_references(client, dataconfiguration, datapoints, entities)


    def classify(self, dataconfiguration, value=None, count=0):
        """ classify """

        # Short time delay to make sure import and cross references are done before we classify
        time_delay(self.config)

        # get the Weaviate client
        client = get_weaviate_client(self.config)

        # will only do something if debugging is globally turned on
        self.debug_before_classify(client, dataconfiguration, count)

        if client is not None and self.config is not None:
            execute_classification(client, self.config, value=value)

            # will only do something if debugging is globally turned on
            self.debug_after_classify(client, dataconfiguration)


    def calculate_score(self, dataconfiguration):
        """ process the result """

        # Short time delay to make sure classification is done before we process the result
        time_delay(self.config)

        # get the Weaviate client
        client = get_weaviate_client(self.config)

        if client is not None and self.config is not None:
            calculate_classification_score(client, self.config, dataconfiguration)


    def write_result(self, dataconfiguration):
        """ process the result """

        # Short time delay to make sure classification is done before we process the result
        time_delay(self.config)

        # get the Weaviate client
        client = get_weaviate_client(self.config)

        if client is not None and self.config is not None:
            write_classification_result(client, self.config, dataconfiguration, self.datapath)


    def should_debug(self):
        """ is the debug flag on or off """
        # check if the debug flag is on
        if self.config is not None and 'weaviate' in self.config and 'debug' in self.config['weaviate']:
            if self.config['weaviate']['debug']:
                return True

        return False


    def debug(self, dataconfiguration):
        """ debug """

        # get the Weaviate client
        client = get_weaviate_client(self.config)

        if self.should_debug():
            debug_compare_datapoint_count(client, self.config, dataconfiguration)


    def debug_before_classify(self, client, dataconfiguration, expected):
        """ debug """
        if self.should_debug():
            debug_assert_eligible_for_classification(client, self.config, dataconfiguration, expected)


    def debug_after_classify(self, client, dataconfiguration):
        """ debug """
        if self.should_debug():
            # after a classification we always expect to find zero eligble
            # items, as all should have been classified in the previous run.
            expected = 0

            debug_assert_eligible_for_classification(client, self.config, dataconfiguration, expected)
