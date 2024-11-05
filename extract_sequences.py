from pathlib import Path
import shutil
import sys
import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
import os


log_level = logging.INFO
logger = logging.getLogger(__name__)
logger.setLevel(log_level)
logging_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(name)-15s %(message)s",
                                      datefmt="%Y-%m-%d %H:%M:%S")
stream_handler = StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging_formatter)
logger.addHandler(stream_handler)

file_handler = RotatingFileHandler(filename=Path(__file__).with_suffix(".log"),
                                   mode="a",
                                   maxBytes=50000000,
                                   backupCount=5)
file_handler.setLevel(log_level)
file_handler.setFormatter(logging_formatter)
logger.addHandler(file_handler)

####################### INPUT DEFINITIONS ##############################################################################
# create paths according to this variable ex. /forehand
hit_type = "serve"   # backhand, serve

# where all the source images are located. This path contains the subfolders /forehand, /backhand, etc.
image_source_path = Path(r"C:\Users\simu_\OneDrive\Dokumente\Studium Weiterbildung\2023 MAS Data Science FHNW\04_Projektarbeiten\20241102_CAS_Deep_Learning\Tennis_classifier\original_images\images")

# where all the target sequences are located. This path contains the subfolders /forehand, backhand, etc. containing the
# sequences
image_target_path = Path(r"C:\Users\simu_\OneDrive\Dokumente\Studium Weiterbildung\2023 MAS Data Science FHNW\04_Projektarbeiten\20241102_CAS_Deep_Learning\Tennis_classifier\images")

# the .txt file path containing the indexes to extract sequences from
index_file_path = Path(r"C:\Users\simu_\OneDrive\Dokumente\Studium Weiterbildung\2023 MAS Data Science FHNW\04_Projektarbeiten\20241102_CAS_Deep_Learning\Tennis_classifier\images\serve\S_indexes.txt")

num_files_per_sequence = 5

##################### END INPUT DEFINITIONS ############################################################################

if __name__ == "__main__":
    logger.info("start script")
    try:
        if hit_type == "forehand":
            file_prefix = "F"
        elif hit_type == "backhand":
            file_prefix = "B"
        elif hit_type == "serve":
            file_prefix = "S"
        else:
            raise ValueError(f"{hit_type} is not a valid hit_type")

        with open(index_file_path, "r") as f:
            lines = f.readlines()
            indexes = [int(x.strip("\n")) for x in lines if len(x.strip("\n"))>0]

        source_files_path = image_source_path.joinpath(hit_type)
        target_files_path = image_target_path.joinpath(hit_type)
        for sequence_index, file_index in enumerate(indexes):
            seq_dir = target_files_path.joinpath(f"seq_{sequence_index:03}")
            if not seq_dir.exists():
                os.mkdir(seq_dir)

            for seq_file_index, i in enumerate(range(file_index - num_files_per_sequence + 1, file_index + 1)):
                source_file = source_files_path.joinpath(f"{file_prefix}_{i:03}.jpeg")
                target_file = seq_dir.joinpath(f"{file_prefix}_{sequence_index:03}_{seq_file_index:03}.jpeg")
                shutil.copyfile(source_file, target_file)

            logger.info(f"copied sequence {sequence_index + 1} of {len(indexes)}")
    except:
        logger.exception("exception occurred", exc_info=True)
    finally:
        logger.info(f"finished copying {hit_type} sequences")
