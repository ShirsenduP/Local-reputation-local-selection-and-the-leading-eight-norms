#!/bin/bash -l

# Force bash as executing shell
#$ -S /bin/bash

# Request x  minutes (h:m:s)
#$ -l h_rt=72:00:0

# Request xGB memory (x = int)
#$ -l mem=1G

# Request XGB TMPDIR space (default - 10GB)
#$ -l tmpfs=10G

# Name of job
#$ -N E_12C3

# Set working dir
#$ -wd /home/ucabpod/Scratch/TestOutput

# go to tempdir (mandatory)
cd $TMPDIR

# run application
module load python3/recommended
source /home/ucabpod/Scratch/CodeEvolution/env2/bin/activate
/usr/bin/time --verbose python /home/ucabpod/Scratch/CodeEvolution/Experiments/Exp12/12C_3.py

# archive all files to scratch
tar zcvf $HOME/Scratch/files_from_job_$JOB_ID.tar.gz $TMPDIR


