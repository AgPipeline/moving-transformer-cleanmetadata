"""Class instance for Transformer
"""

import argparse
import os
import logging

import configuration

#pylint: disable=unused-argument
class Transformer():
    """Generic class for supporting transformers
    """
    def __init__(self, **kwargs):
        """Performs initialization of class instance
        Arguments:
            kwargs: additional parameters passed into Transformer instance
        """
        self.args = None

    # pylint: disable=no-self-use
    def add_parameters(self, parser: argparse.ArgumentParser) -> None:
        """Adds processing parameters to existing parameters
        Arguments:
            parser: instance of argparse
        """
        parser.add_argument('--logging', '-l', nargs='?', default=os.getenv("LOGGING"),
                            help='file or url or logging configuration (default=None)')

        parser.add_argument('sensor', type=str, help='the name of the sensor associated with the metadat')

        parser.add_argument('userid', type=str, nargs='?',
                            help='an optional user identification string to be added to the metadata')

        parser.epilog = configuration.TRANSFORMER_NAME + ' version ' + configuration.TRANSFORMER_VERSION + \
                        ' author ' + configuration.AUTHOR_NAME + ' ' + configuration.AUTHOR_EMAIL


    #pylint: disable=no-self-use
    def get_transformer_params(self, args: argparse.Namespace, metadata: dict) -> dict:
        """Returns a parameter list for processing data
        Arguments:
            args: result of calling argparse.parse_args
            metadata: the loaded metadata
        """
        self.args = args

        logging.debug("Transforming args to metadata: %s", str(args))
        check_md = {
            'trigger_name': args.metadata,
            'working_folder': args.working_space,
            'sensor': args.sensor,
            'userid': args.userid
        }

        logging.debug("Request metadata: %s", str(check_md))
        return {'check_md': check_md,
                'transformer_md': None,
                'full_md': metadata
               }
