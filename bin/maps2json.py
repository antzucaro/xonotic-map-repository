#!/usr/bin/env python3
# Description: Xonotic Map Repository tools help create and manage a map repository.
# Author: Tyler "-z-" Mulligan
# Contact: z@xnz.me

import argparse
import json
import time
import os
import datetime
from xmr.packages import Library
from xmr.packages import MapPackage
from xmr.config import config
from xmr.util import ObjectEncoder


def main():

    start_time = time.monotonic()
    errors = False
    args = parse_args()

    library = Library()

    if args.all:

        # Process all the files
        for file in sorted(os.listdir(config['output_paths']['packages'])):
            if file.endswith('.pk3'):
                mypk3 = MapPackage(pk3_file=file)
                pk3, category, errors = mypk3.process_package()

                print(pk3.pk3_file)

                library.add_map_package(pk3=pk3, category=category)

                # if status['errors']:
                #     errors = True

        # Write error.log

        all_maps = library.to_json()

        fo = open(config['output_paths']['data'] + 'maps.json', 'w')
        fo.write(all_maps)
        fo.close()

    if args.add:

        file = args.add

        if file.endswith('.pk3') and os.path.isfile(config['output_paths']['packages'] + file):
            status = MapPackage(pk3_file=file)

            # if status['errors']:
            #     errors = True

        else:
            print('Not found or not pk3.')
            raise SystemExit

    end_time = time.monotonic()
    print('Operation took: ' + str(datetime.timedelta(seconds=end_time - start_time)))


def parse_args():

    parser = argparse.ArgumentParser(description='Xonotic Map Repository tools help create and manage a map repository.')

    parser.add_argument('--add', '-a', nargs='?', type=str, help='Add a package to the repositories JSON')
    parser.add_argument('--all', '-A', action='store_true',
                        help='Add all maps to the repositories JSON. (overwrites existing maps.json)')

    return parser.parse_args()


if __name__ == "__main__":
    main()
