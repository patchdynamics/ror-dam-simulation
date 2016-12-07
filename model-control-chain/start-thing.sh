rm slurm*
./scripts/clear.sh
sbatch --job-name=THING --mail-type=END,FAIL  --mail-user=shultzm@stanford.edu  scripts/run.thing.cluster.sh
