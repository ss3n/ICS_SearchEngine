#!/bin/bash
module load sge
qsub -q 15day.q -M shiladis@ics.uci.edu -m beas -o ~/crawler.$JOB_ID.out -e ~/errcrawler.$JOB_ID.err Script.sh

