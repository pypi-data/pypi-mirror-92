# The only reason recorder is "recorder/__init__.py" instead of recorder.py is
# so that sardana RecorderPath points only to this file and not the
# parent directory which prevents sardana from trying to load the other files
# looking for recorders
