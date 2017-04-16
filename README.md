# assignment-3-team_awesome
assignment-3-team_awesome created by GitHub Classroom

To run the code: 
python main.py [-h] -s N_PREV [-b K] [--greedy] [--viterbi] [--add1]
               [--linear] [--most-common] [--unknown-classes] -f FILENAME

optional arguments:
  -h, --help            show this help message and exit
  -s N_PREV, --states N_PREV
                        Number of states in the HMM
  -b K, --beam-width K  Width of the beam search (default: 2)
  --greedy              Flag that makes use of the Greedy algorithm
  --viterbi             Flag that makes use of the Viterbi algorithm
  --add1                Flag that makes use of the Add-1 smoothing
  --linear              Flag that makes use of the Linear Interpolation
  --most-common         Flag that uses Dictionary with the most common tag for
                        unknown
  --unknown-classes     Flag that uses the dictionary with classes for the
                        unknown words
  -f FILENAME, --output FILENAME
                        Filename to store the output
