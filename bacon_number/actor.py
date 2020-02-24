from flask import abort
import os

BACON_NUMBERS = None


def load_bacons_number(data_dir):
    """
    Loads the bacon_numbers.txt file into the global variable
    :param data_dir: the data where the file is
    """
    data_file = os.path.join(data_dir, 'bacon_numbers.txt')
    if not os.path.exists(data_file):
        raise Exception('Datafile {} does not exists. Create it with the '
                        'preprocess_data.py script'.format(data_file))
    degrees = {}
    with open(data_file) as f:
        for l in f.readlines():
            s = l.strip().split(' ### ')
            actor = s[0].strip()
            degree = int(s[1].strip())
            if actor in degrees:
                raise Exception(actor)
            degrees[actor] = degree
    global BACON_NUMBERS
    BACON_NUMBERS = degrees


def show_all(offset=0, limit=-1):
    actors = sorted(BACON_NUMBERS.keys())
    if offset > 0:
        actors = actors[offset:]
    if limit > -1:
        actors = actors[:limit]
    return actors


def bacon_number(actorName):
    if actorName not in BACON_NUMBERS:
        abort(404)
    return {'degrees': BACON_NUMBERS[actorName]}
