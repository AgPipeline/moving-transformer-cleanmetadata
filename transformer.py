"""Transformer for cleaning gantry metadata before further processing
"""

import json
import os
import logging

from terrautils.metadata import clean_metadata as tr_clean_metadata
import terrautils.lemnatec

import transformer_class

terrautils.lemnatec.SENSOR_METADATA_CACHE = os.path.dirname(os.path.realpath(__file__))

# List of sensors that cannot be cleaned
SKIP_SENSORS = ['Full Field']

def check_continue(transformer: transformer_class.Transformer, check_md: dict, transformer_md: list, full_md: list) -> tuple:
    """Checks if conditions are right for continuing processing
    Arguments:
        transformer: instance of transformer class
    Return:
        Returns a tuple containing the return code for continuing or not, and
        an error message if there's an error
    """
    # pylint: disable=unused-argument
    # Check that the sensor is one to process. Returns a positive value if it's to be skipped so that nothing gets
    # downloaded.
    if 'sensor' in check_md:
        return tuple(1) if check_md['sensor'] in SKIP_SENSORS else (0)

    # Return a negative number if the sensor isn't specified
    return -1, "Sensor type not specified. Invalid runtime environment detected."

def perform_process(transformer: transformer_class.Transformer, check_md: dict, transformer_md: list, full_md: list) -> dict:
    """Performs the processing of the data
    Arguments:
        transformer: instance of transformer class
    Return:
        Returns a dictionary with the results of processing
    """
    # pylint: disable=unused-argument
    # See if we need to do anything
    if check_md['sensor'] in SKIP_SENSORS:
        return {'code': 0, 'warning': "Skipping sensor %s does not have metadata that needs to be cleaned." % (check_md['sensor'])}

    # Get the working metadata
    metadata = full_md[0]
    if '@context' in metadata and 'content' in metadata:
        parse_md = metadata['content']
    else:
        parse_md = metadata

    # Make sure we have something to work with
    if not parse_md:
        return {'code': -1000, 'error': "No metadata specified" if not full_md else "Invalid metadata detected"}

    # Clean the metadata and prepare the result
    logging.debug("Calling into clean_metadata with sensor '%s' and metadata %s", check_md['sensor'], str(parse_md))
    md_json = tr_clean_metadata(parse_md, check_md['sensor'])
    format_md = {
        '@context': ['https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld',
                     {'@vocab': 'https://terraref.ncsa.illinois.edu/metadata/uamac#'}],
        'content': md_json,
        'agent': {
            '@type': 'cat:user'
        }
    }

    if check_md['userid']:
        logging.debug("Setting agent user_id to %s", check_md['userid'])
        format_md['agent']['user_id'] = check_md['userid']
 
    # Create the output file and write the metadata to it
    filename_parts = os.path.splitext(os.path.basename(check_md['trigger_name'][0]))
    new_filename = filename_parts[0] + '_cleaned' + filename_parts[1]
    new_path = os.path.join(check_md['working_folder'], new_filename)

    logging.debug("Writing cleaned metadata to file '%s'", new_path)
    with open(new_path, 'w') as out_file:
        json.dump(format_md, out_file, indent=2, skipkeys=True)

    result = \
        {
            'file': [{
                'path': new_path,
                'key': check_md['sensor']
            }],
            'code': 0
        }

    return result
