import argparse
import yaml

import likelihood_combiner as lklcom

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            description=("Combining likelihoods from different experiments."))
    parser.add_argument(
            'config_file',
            help="path to YAML configuration file with combining options")
    parser.add_argument(
            '--channel',
            default='bb')
    parser.add_argument(
            '--input',
            default=None,
            help="path to input file or directory")
    parser.add_argument(
            '--output',
            default=None,
            help="path to output directory")
    parser.add_argument(
            '--simulation',
            default=0,
            type=int,
            help="number of the simulation")
    args = parser.parse_args()

    with open(args.config_file, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    lklcom.cluster.run_cluster(settings=config, channel=args.channel, input=args.input, output=args.output, simulation=args.simulation)
