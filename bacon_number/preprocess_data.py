import argparse
import os
import zipfile
import csv
import ast


def download_zip_file(data_dir):
    """
    Check that the zip file has been downloaded from kaggle
    :param data_dir: directory where the zip file is stored
    :raise Exception: if the zip file is no in the data_dir
    """
    zip_file = os.path.join(data_dir, 'the-movies-dataset.zip')
    if os.path.exists(zip_file):
        return
    raise Exception("Please download the movies dataset from "
                    "https://www.kaggle.com/rounakbanik/the-movies-dataset")


def uncompress_zip_file(data_dir):
    """
    Uncompress the zip file from the data_dir into the data_dir if the credits.csv does not
    exists in the directory.
    :param data_dir: directory where the zip file is stored and the files will be uncompressed
    """
    credits_csv_filename = os.path.join(data_dir, 'credits.csv')
    if os.path.exists(credits_csv_filename):
        return
    zip_file = os.path.join(data_dir, 'the-movies-dataset.zip')
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(data_dir)


def process_metadata(data_dir):
    """
    Process the credits.csv file in the data_dir and creates a bacon_numbrs.txt file in the data_dir
    with the bacon numbers of all the actors. This method uses the dijstra algorithm to browse the
    graph of actors in order to calculate the bacon number.
    :param data_dir: directory where the data is stored
    """
    bacon_number_filename = os.path.join(data_dir, 'bacon_numbers.txt')
    if os.path.exists(bacon_number_filename):
        return
    credits_csv_filename = os.path.join(data_dir, 'credits.csv')
    actor_connections = {}
    all_actors = set()
    with open(credits_csv_filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            cast = ast.literal_eval(row['cast'])  # because the internal data is not a valid json
            actors = []
            for c in cast:
                actor_name = c['name'].strip()
                actors.append(actor_name)
                all_actors.add(actor_name)
            # create the first degree connections among actors
            for actor in actors:
                if actor not in actor_connections:
                    actor_connections[actor] = set()
                for a in actors:
                    if a != actor:
                        actor_connections[actor].add(a)
    # calculate the degree of separation using disjtra algorithm starting in Kevin Bacon
    actors_degree = dict([actor, -1] for actor in all_actors)
    kevin_bacon = 'Kevin Bacon'
    actors_degree[kevin_bacon] = 0
    to_parse_actors = [[kevin_bacon, 0]]
    parsed_actors = set()
    parsed_actors.add(kevin_bacon)
    with open(bacon_number_filename, mode='w') as f:
        while len(to_parse_actors) > 0:
            actor, degree = to_parse_actors[0]
            to_parse_actors = to_parse_actors[1:]
            f.write('{} ### {}\n'.format(actor.replace('"', ''), degree))
            for a in actor_connections[actor]:
                if actors_degree[a] == -1 and a not in parsed_actors:
                    to_parse_actors.append([a, degree + 1])
                    parsed_actors.add(a)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='./data',
                        help='Directory where the data will be stored')
    params = parser.parse_args()

    download_zip_file(params.data_dir)
    uncompress_zip_file(params.data_dir)
    process_metadata(params.data_dir)
