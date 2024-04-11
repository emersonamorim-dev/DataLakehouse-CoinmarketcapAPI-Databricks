# Databricks notebook source
#!/usr/bin/env python
import sys
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def etl_process(input_path, output_path):
    """
    ETL process that reads data from a source, transforms it, and writes to a destination.

    :param input_path: Path to the input data file.
    :param output_path: Path to the output data file.
    """
    try:
        # Read data
        with open(input_path, 'r') as infile:
            data = json.load(infile)
            logger.info(f"Loaded data from {input_path}")

        # Process data 
        transformed_data = data  

        # Write data
        with open(output_path, 'w') as outfile:
            json.dump(transformed_data, outfile)
            logger.info(f"Written transformed data to {output_path}")

    except Exception as e:
        logger.error(f"ETL process failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logger.error("Usage: my_etl_script.py <input_path> <output_path>")
        sys.exit(1)

    input_file_path, output_file_path = sys.argv[1], sys.argv[2]
    
    # Verify that the input file exists
    if not Path(input_file_path).is_file():
        logger.error(f"Input file {input_file_path} does not exist.")
        sys.exit(1)

    etl_process(input_file_path, output_file_path)
