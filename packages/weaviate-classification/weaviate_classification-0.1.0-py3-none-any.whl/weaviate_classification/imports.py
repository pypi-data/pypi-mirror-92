""" This module parses ex-factory excel file from PVM """

import uuid
import weaviate
from .utilities import get_reference_class_name_from_field


def _generate_uuid_for_entity(entity, key):

    newuuid = ""

    uuidstring = entity + "_" + key
    newuuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, uuidstring))

    return newuuid


def _generate_uuid_for_datapoint(dataconfig, point):

    newuuid = ""

    if dataconfig is not None and point is not None:
        for dataclass in dataconfig['classes']:
            if dataclass['classname'] == point['classname']:
                string = "point_"

                # loop through the columns and add values for those columns that are identifier columns
                for col in dataclass['columns']:
                    if col['id']:
                        string = string + point[col['name']]

                    # generate the new uuid
                    newuuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, string))
                break

    return newuuid


def set_cross_references(client, dataconfig, datapoints, entities):
    """ set cross references """

    pointcount = batchcount = 0
    if client is None or dataconfig is None or datapoints is None or entities is None:
        return


    batch = weaviate.ReferenceBatchRequest()
    for point in datapoints:

        # first get the classname from the data configuration
        classname = point['classname']

        # Only set the references if the point is validated
        if point['validated']:
            pointcount += 1

            # Determine the uuid of the point
            produuid = _generate_uuid_for_datapoint(dataconfig, point)

            for key in point:
                if key != 'classname':
                    entity = get_reference_class_name_from_field(key)
                    if entity in entities:

                        # Determine the uuid of the entity
                        entuuid = _generate_uuid_for_entity(entity, point[key])

                        propertyname = "of" + entity
                        batch.add(produuid, classname, propertyname, entuuid)

                        batchcount += 1
                        if (batchcount % 999) == 0:
                            client.batch.create_references(batch)
                            batch = weaviate.ReferenceBatchRequest()
                            batchcount = 0
                            print("Cross reference data points -----------:", pointcount, end="\r")

    if batchcount > 0:
        client.batch.create_references(batch)
        print("Cross reference data points -----------:", pointcount)


def import_entities_to_weaviate(client, entities):
    """ import entities """

    if client is not None and entities is not None:

        # initialize the count variables
        totalcount = batchcount = 0

        # create the first batch request
        batch = weaviate.ObjectsBatchRequest()

        # loop through all the entities and create an instance for each value
        for entity in entities:
            for name in entities[entity]:
                thing = {}
                thing['name'] = name
                newuuid = _generate_uuid_for_entity(entity, name)
                batch.add(thing, entity, newuuid)

                batchcount += 1
                totalcount += 1
                if (batchcount % 1000) ==0:
                    print("len batch:", len(batch))
                    print("Entities imported into Weaviate -------:", totalcount, end="\r")
                    client.batch.create_objects(batch)
                    batch = weaviate.ObjectsBatchRequest()
                    batchcount = 0
        if batchcount > 0:
            client.batch.create_objects(batch)
            print("Entities imported into Weaviate -------:", totalcount)


def import_datapoints_to_weaviate(client, dataconfig, datapoints, validated=True):
    """ import the datapoints """

    if client is not None and dataconfig is not None and datapoints is not None:

        # initialize the count variables
        totalcount = batchcount = 0

        # create the first batch request
        batch = weaviate.ObjectsBatchRequest()

        # loop through all data points and create an instance for each data point
        for point in datapoints:

            # first get the classname from the data configuration
            classname = point['classname']

            if point['validated'] == validated:

                # create the thing dictionary with all the values for the properties
                thing = {}
                thing['row'] = point['row']
                thing['validated'] = point['validated']
                thing['batchNumber'] = point['batchNumber']
                for key in point:
                    if key != 'classname':
                        thing[key] = point[key]

                # create the uuid for the new data point
                newuuid = _generate_uuid_for_datapoint(dataconfig, point)

                # Add the datapoint to the batch and increase the counters
                batch.add(thing, classname, newuuid)
                batchcount += 1
                totalcount += 1

                # if the batch size reaches the maximum size, import and start a new batch
                if (batchcount % 999) == 0:
                    print("Data points imported into Weaviate ----:", totalcount, end="\r")
                    result = client.batch.create_objects(batch)
                    #print(result)
                    batch = weaviate.ObjectsBatchRequest()
                    batchcount = 0

        # if there are left over points in the last batch, import these last data points
        if batchcount > 0:
            result = client.batch.create_objects(batch)
            #print(result)
            print("Data points imported into Weaviate ----:", totalcount)
