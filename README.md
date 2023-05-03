# vstcheck

If you're trying to run your DAW in Apple Silicon Native mode and not under Rosetta, you'll probably need to update your plugins. This script will list every VST you have installed that needs to be updated to work in Native mode.

## Usage

Download the script and run it:

`python vstcheck.py`

It will output all the VSTs that are not Apple Silicon compatible.

You can add more directories to the `vst_directories` list in the script if you have any non-standard places that you keep VSTs.