## Installation
pip install cloudant
pip install twarc
pip install tweepy
mkdir data

## Automatic Execution
### Streamer
./streamer.sh
### Timeline
./timeline.sh

## Manual Execution
### Streamer
python twitter_streamer.py
    -a [username] -c [config_file] -q [query**] -d [data_directory]
** if query matches one of six keywords (fastfood, fruits, grains, meat, seafood, vegetables)
**     stream tweets around the world via selected keyword
** else
**     stream tweets with a bounding box around Australia
### Timeline
python twitter_timeline.py
    -a [username] -c [config_file] -i [in_usernames_file] -o [out_file] -o2 [out_usernames_file]
### Hydrator
python twitter_hydrator.py
    -a [username] -c [config_file] -i [input_dataset] -o [output_dataset]
