# bengali-g2p
Python based G2P module for Bangla

```
usage: stitch.py [-h] [-i] [-f FILEPATH] [-t] [--ipa] [--xsampa]


optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     read tokens from standard input (type "stop" or "ctrl+c" to stop)
  -f FILEPATH, --file FILEPATH
                        path to file containing tokens in Bengali
  -t, --run-tests       Specify whether unit tests should be run. This is set
                        to true by default if input file is not specified.
  --ipa                 return IPA transcriptions
  --xsampa              return XSAMPA transcriptions. If neither --ipa nor
                        --xsampa flags are specified, xipa transcriptions are
                        returned by default
```

This is a work in progress. The script maps graphemes to an intermediate xipa notation 
I've made up, along with a few archiphonemes which should ultimately be resolved to 
actual phonemes once the rules are all in place. The xipa will be post-processed to actual IPA
and XSAMPA notations in a secondary step (not yet implemented).



Current accuracy metrics: 38/52 = 73% 