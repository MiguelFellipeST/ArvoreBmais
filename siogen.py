#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
'''
SIOgen: Simple Insert Delete Dataset Generator
'''

import argparse
import csv
from random import randint, shuffle, seed

# Parameters
# Attributes number
ATT = 'att'
# Insertions number
INSERT = 'inssert'
# Deletions number
DELETE = 'delete'
# Searches number
SEARCH = 'search'
# Output file
FILE = 'file'

# Default parameter values
DEFAULT_ATT = 10
DEFAULT_INSERT = 2000
DEFAULT_DELETE = 500
DEFAULT_SEARCH = 3000
DEFAULT_SEED = 42
DEFAULT_FILE = 'output.csv'

def gen_insertions(rec_list, keys_list, key_set, par_dict):
    '''
    Generate insertions
    '''
    # Check if there are keys to insert
    if len(keys_list) == 0:
        return
    # Number of insertions
    ins_num = randint(1, len(keys_list))
    par_dict[INSERT] -= ins_num
    # List of keys to insert
    ins_list = keys_list[:ins_num]
    del keys_list[:ins_num]
    # Current set of keys
    key_set.update(ins_list)
    for key in ins_list:
        # New record
        new_record = {'OP': '+'}
        # List of attributes
        att_list = ['A' + str(number + 1) for number in range(par_dict[ATT])]
        # Generate each attribute value
        for att in att_list:
            new_record[att] = randint(0, 1000)
        # Attribute key
        new_record['A1'] = key
        # Append record to list
        rec_list.append(new_record)

def gen_deletions(rec_list, keys_set, par_dict):
    '''
    Generate deletions
    '''
    # Check if there are keys to delete
    if par_dict[DELETE] == 0:
        return
    # Number of deletions
    del_num = randint(1, par_dict[DELETE])
    # Check if there are enough keys to delete
    if del_num > len(keys_set):
        return
    # Compute keys to delete
    key_list = list(keys_set)
    shuffle(key_list)
    del_list = key_list[:del_num]
    par_dict[DELETE] -= del_num
    # Loop to create deletions
    for key in del_list:
        # New record
        new_record = {'OP': '-'}
        # List of attributes
        att_list = ['A' + str(number + 1) for number in range(par_dict[ATT])]
        # Generate each attribute value
        for att in att_list:
            new_record[att] = key
        # new_record['A1'] = key
        # Append record to list
        rec_list.append(new_record)
        # Update current key set
        keys_set.remove(key)

def gen_searches(rec_list, keys_set, par_dict):
    '''
    Generate deletions
    '''
    # Check if there are keys to search
    if par_dict[SEARCH] == 0:
        return
    # Number of searches
    searches_num = randint(1, par_dict[SEARCH])
    par_dict[SEARCH] -= searches_num
    # Loop to create searches
    for _ in range(searches_num):
        new_record = {'OP': '?'}
        # new_record['A1'] = randint(1, 2*len(keys_set))
        key = randint(1, 2*len(keys_set))
        # List of attributes
        att_list = ['A' + str(number + 1) for number in range(par_dict[ATT])]
        # Generate each attribute value
        for att in att_list:
            new_record[att] = key

        rec_list.append(new_record)

def store_records(rec_list, par_dict):
    '''
    Store a record list in into file
    '''
    # Check if record list is empty
    if len(rec_list) == 0:
        return
    # Build attribute list including operation flag
    att_list = ['OP'] + \
        ['A' + str(number + 1) for number in range(par_dict[ATT])]
    # Open file
    with open(par_dict[FILE], 'w', encoding='utf-8') as out_file:
        # Create csv writer
        out_write = csv.DictWriter(out_file, att_list)
        # Write file header
        out_write.writeheader()
        # Write records
        out_write.writerows(rec_list)
        # Close file
        out_file.close()

def gen_keys(par_dict):
    '''Generate keys'''
    key_list = list(range(par_dict[INSERT]))
    shuffle(key_list)
    return key_list

def gen_data(par_dict):
    '''
    Generate data
    '''
    if par_dict[DELETE] > par_dict[INSERT]:
        raise ValueError('Number of deletions must be less than insertions')
    # Generate keys to be inserted
    key_list = gen_keys(par_dict)
    # List of existing keys
    keys_set = set()
    # List of records
    rec_list = []
    # Loop to generate records
    while par_dict[INSERT] + par_dict[DELETE] + par_dict[SEARCH] > 0:
        gen_insertions(rec_list, key_list, keys_set, par_dict)
        gen_searches(rec_list, keys_set, par_dict)
        gen_deletions(rec_list, keys_set, par_dict)
    store_records(rec_list, par_dict)

def get_arguments(print_help=False):
    '''
    Get arguments
    '''
    parser = argparse.ArgumentParser('SIOGen')
    parser.add_argument('-a', '--attributes', action='store', type=int,
                        default=DEFAULT_ATT,
                        help='Number of attributes (default: ' +
                        str(DEFAULT_ATT) + ')')
    parser.add_argument('-i', '--insertions', action='store', type=int,
                        default=DEFAULT_INSERT,
                        help='Number of insertions (default: ' +
                        str(DEFAULT_INSERT) + ')')
    parser.add_argument('-d', '--deletions', action='store', type=int,
                        default=DEFAULT_DELETE,
                        help='Number of deletions (default: ' +
                        str(DEFAULT_DELETE) + ')')
    parser.add_argument('-s', '--searches', action='store', type=int,
                        default=DEFAULT_SEARCH,
                        help='Number of deletions (default: ' +
                        str(DEFAULT_SEARCH) + ')')
    parser.add_argument('-f', '--filename', action='store', type=str,
                        default=DEFAULT_FILE,
                        help='Output filename (default: ' +
                        DEFAULT_FILE + ')')
    parser.add_argument('-e', '--seed', action='store', type=int,
                        default=DEFAULT_SEED,
                        help='Seed (default: ' +
                        str(DEFAULT_SEED) + ')')
    args = parser.parse_args()
    if print_help:
        parser.print_help()
    return args

def main():
    '''
    Main routine
    '''
    # Get arguments
    args = get_arguments()
    # Set seed
    seed(args.seed)
    # Create dictionary of parameters
    par_dict = {
        ATT: args.attributes,
        INSERT: args.insertions,
        DELETE: args.deletions,
        SEARCH: args.searches,
        FILE: args.filename
        }
    # Generate data
    gen_data(par_dict)

if __name__ == '__main__':
    main()
