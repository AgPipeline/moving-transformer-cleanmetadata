# Transformer: Metadata Cleaner
Cleans LemnaTec Metadata to allow easier processing by other transformers

## Overview
This transformer is different than most in that it's specialized for cleaning the Gantry metadata.
This requires the transformer to also have its own transformer_class.Transformer instance for special parameter handling.

## Parameters
There are two additional parameters for this transformer: **sensor**, and **userid**.

The **sensor** parameter is *required* and refers to the gantry sensor the metadata is associated with.

The **userid** parameter is *optional* and allows additional identification information to be stored with the cleaned metadata.

## Sample Docker Command line
Below is a sample command line that shows how the metadata cleaner Docker image could be run.
An explanation of the command line options used follows.
Be sure to read up on the [docker run](https://docs.docker.com/engine/reference/run/) command line for more information.

```docker run --rm --mount "src=/home/test,target=/mnt,type=bind" -e "BETYDB_URL=https://terraref.ncsa.illinois.edu/bety/" -e "BETYDB_KEY=<key value>" agpipeline/cleanmetadata:2.0 --working_space "/mnt" --metadata "/mnt/08f445ef-b8f9-421a-acf1-8b8c206c1bb8_metadata.json" "stereoRGB" ```

This example command line assumes the source files are located in the `/home/test` folder of the local machine.
The name of the image to run is `agpipeline/cleanmetadata:2.0`.

We are using the same folder for the source metadata and the cleaned metadata.
By using multiple `--mount` options, the source and output files can be separated.

**Docker commands** \
Everything between 'docker' and the name of the image are docker commands.

- `run` indicates we want to run an image
- `--rm` automatically delete the image instance after it's run
- `--mount "src=/home/test,target=/mnt,type=bind"` mounts the `/home/test` folder to the `/mnt` folder of the running image
- `-e "BETYDB_URL=https://terraref.ncsa.illinois.edu/bety/"` the URL to the BETYdb instance to fetch experiment, and other data, from
- `-e "BETYDB_KEY=<key value>"` the key associated with the BETYdb URL (replace `<key value>` with value of your key)

We mount the `/home/test` folder to the running image to make available the file to the software in the image.

**Image's commands** \
The command line parameters after the image name are passed to the software inside the image.
Note that the paths provided are relative to the running image (see the --mount option specified above).

- `--working_space "/mnt"` specifies the folder to use as a workspace
- `--metadata "/mnt/08f445ef-b8f9-421a-acf1-8b8c206c1bb8_metadata.json"` is the name of the source metadata to be cleaned
- `"stereoRGB"` is the name of the sensor the metadata is associated with
