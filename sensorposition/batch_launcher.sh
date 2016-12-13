#!/bin/bash
# this script is called to invoke one instance of sensorposition extractor.

# Load necessary modules
module purge
module load python/2.7.10 pythonlibs/2.7.10 gdal-stack-2.7.10 gdal nco

# Activate python virtualenv
source /projects/arpae/terraref/shared/extractors/pyenv/bin/activate

# Run extractor script
python /projects/arpae/terraref/shared/extractors/extractors-metadata/sensorposition/terra_sensorposition.py
