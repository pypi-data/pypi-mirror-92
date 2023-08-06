# from . import AlgorithmDaemon, ArtifactInputDirectory, ArtifactOutputDirectory
from daemon import AlgorithmDaemon
from config import ArtifactInputDirectory, ArtifactOutputDirectory
import time
import logging
import os
import glob
import json
import random


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler()
    ]
)

daemon = AlgorithmDaemon.get_instance()


def execute():
    # if not os.path.exists(ArtifactOutputDirectory):
    #     raise IOError("directory of output is not exists")
    result = {}
    score = random.uniform(0, 1)
    result['positive'] = score > 0.5
    result['score'] = score
    # result_filename = os.path.join(ArtifactOutputDirectory, 'result.json')
    # with open(result_filename, 'w') as outfile:
    #     json.dump(result, outfile)


if __name__ == "__main__":
    try:
        execute()
        # ensure 100% progress
        daemon.report_progress(1)
        daemon.shutdown()

    except Exception as exception:
        daemon.on_failed(exception)
