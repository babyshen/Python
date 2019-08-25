#!/usr/bin/env python

from sys import argv
import requests


def help_text():
    text = '''
    {0} -- list all tags and full_size for a Docker image on a remote registry.
    EXAMPLE:
        - list all tags and full_size for centos:
           {0} centos
    '''.format(argv[0])
    print(text)


def get_json(url):
    results = requests.get(url).json()
    return results


def get_results():
    results = get_json(url)
    for i in results["results"]:
        print("%-20s %.2fMB" % (i["name"], i["full_size"] / 1000000))

    next_url = results["next"]
    while next_url:
        results = get_json(next_url)
        for n in results["results"]:
            print("%-20s %.2fMB" % (n["name"], n["full_size"] / 1000000))
        next_url = results["next"]

def check_if_in_any(string, iterable):
    return any(map(lambda item: item == string, iterable))


if __name__ == '__main__':
    if len(argv) < 2 or any([check_if_in_any(x, ['-h', '--help']) for x in argv]):
        help_text()
        exit(1)

    image = argv[1] if '/' in argv[1] else 'library/' + argv[1]
    url = "https://hub.docker.com/v2/repositories/" + image + "/tags/?page_size=100"
    try:
        get_results()
    except KeyError:
        exit('Please enter the correct image name! ')
