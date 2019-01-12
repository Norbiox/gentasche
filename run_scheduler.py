import argparse
from pathlib import Path

from gentasche import Dataset, GeneticTaskScheduler

parser = argparse.ArgumentParser(
    description="Run GeneticTaskScheduler against dataset"
)
parser.add_argument('dataset_file', type=str, help='dataset file path')
parser.add_argument('-p', '--population_size', type=int, default=10)
parser.add_argument('-m', '--mutation_ratio', type=float, default=5.0)
parser.add_argument('-r', '--max_repeats', type=int, default=100)

args = parser.parse_args()

dataset = Dataset.read(args.dataset_file)
gts = GeneticTaskScheduler(args.population_size, args.mutation_ratio,
                           args.max_repeats)
gts.schedule(dataset)
fig = gts.plot_statistics()
p = Path('images')
p.mkdir(parents=True, exist_ok=True)
fig.savefig(p / ('_'.join([
    args.dataset_file.split('/')[-1] , str(args.population_size), 
    str(args.mutation_ratio).replace('.', '_'), str(args.max_repeats)
]) + '.png'))
