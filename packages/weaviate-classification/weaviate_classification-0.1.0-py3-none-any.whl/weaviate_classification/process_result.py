""" This module queries Weaviate """

import os
import math
import openpyxl

from .utilities import get_field_name_from_reference_property
from .utilities import get_cellid_of_field
from .query import count_number_of_datapoints
from .query import create_get_query_batch_number
#from classification.Query import create_get_query_row_numbers


def _initialize_result_score(properties):
    score = {}
    score['total'] = 0
    for prop in properties:
        score[prop] = 0

    return score


############################################################################################################
##
## calculate_classification_score is only used in a validation run. It calculates which percentage of the
## classified items was correctly classified.
##
############################################################################################################

def _score_query_result(result, classname, properties, score):
    """ Query Weaviate """

    if result is None or 'data' not in result:
        print("No classified datapoints found --------:")
        return

    # Get the datapoints from the result argument
    datapoints = result['data']['Get'][classname]

    # For each datapoint and for each property: check if the classification is the same as the original value
    for point in datapoints:

        # count this data point to the total data points
        score['total'] += 1

        # for each property, check if the classified value is the same as the stored value
        for prop in properties:
            field = get_field_name_from_reference_property(prop)
            if prop in point and point[prop] is not None:
                if point[prop][0]['name'] == point[field]:
                    score[prop] += 1
            else:
                print(point['row'], ";Warning: property", prop, "not found.")


def calculate_classification_score(client, config, dataconfig):
    """ process result """

    if client is not None and config is not None and dataconfig is not None:

        # get the classname of the property that was classified
        classname = config['classification']['classify_class']

        # Determine the properties that have been classified
        properties = []
        if 'classification' in config and 'classify_properties' in config['classification']:
            for prop in config['classification']['classify_properties']:
                properties.append(prop)

        # get the maximum batch size from the config file
        if 'classification' in config and 'max_batch_size' in config['classification']:
            maxbatch = config['classification']['max_batch_size']

        # count the number of instances of the main class in Weaviate
        count = count_number_of_datapoints(client, classname)

        # initialize the dict that keeps score of the number of properties correctly classified
        score = _initialize_result_score(properties)

        # if count > maxbatch, we need to pull the result out in batches.
        batchcount = math.ceil(count / maxbatch)
        for batch in range(1, batchcount + 1):

            query = create_get_query_batch_number(client, config, dataconfig, batch)
            #print(query)
            result = client.query.raw(query)

            _score_query_result(result, classname, properties, score)
            print("Total number of datapoints found ------:", score['total'])

        if score['total'] > 0:
            for prop in properties:
                print(score[prop], "=", round((score[prop]/score['total'])*100),"%", "-", prop)
        else:
            print("Warning: zero classified data points --:")


############################################################################################################
##
## write_classification_result writes the outcome of the classification to an excel output file. The location
## of the file is determined by the config file, the filename is determined by the input file
##
############################################################################################################

def _write_query_result(sheet, result, dataconfig, properties, classname, score):
    """ Query Weaviate """

    if sheet is None or result is None or 'data' not in result:
        return

    # Prepare the result calculation. We count the number of correct matches. Initialize to zero for each property
    datapoints = result['data']['Get'][classname]

    # For each datapoint store the classified value
    for point in datapoints:
        score['total'] += 1
        for prop in properties:
            if prop in point and point[prop] is not None:
                field = get_field_name_from_reference_property(prop)
                cell = get_cellid_of_field(dataconfig, field, point['row'])
                if cell is not None:
                    sheet[cell] = point[prop][0]['name']


def write_classification_result(client, config, dataconfig, datapath):
    """ process result """

    if client is not None and config is not None and dataconfig is not None:

        # get the classname of the property that was classified
        classname = config['classification']['classify_class']

        # Determine the properties that have been classified
        properties = []
        if 'classification' in config and 'classify_properties' in config['classification']:
            for prop in config['classification']['classify_properties']:
                properties.append(prop)

        # get the maximum batch size from the config file
        if 'classification' in config and 'max_batch_size' in config['classification']:
            maxbatch = config['classification']['max_batch_size']

        # count the number of instances of the main class in Weaviate
        count = count_number_of_datapoints(client, classname)

        # initialize the dict that keeps score of the number of properties classified
        score = _initialize_result_score(properties)

        # create the excel file to write the result to
        workbook = openpyxl.load_workbook(datapath)
        sheet = workbook.active

        # if count > maxbatch, we need to pull the result out in batches.
        batchcount = math.ceil(count / maxbatch)
        for batch in range(1, batchcount + 1):

            query = create_get_query_batch_number(client, config, dataconfig, batch)
            print(query)
            result = client.query.raw(query)

            _write_query_result(sheet, result, dataconfig, properties, classname, score)
            print("Total number of datapoints found ------:", score['total'])

        _, tail = os.path.split(datapath)

        if 'output_path' in config:
            filename = config['output_path'] + tail
        else:
            filename = tail

        workbook.save(filename)
        workbook.close()
