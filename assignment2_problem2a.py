import os
import argparse
import sys
import time
import multiprocessing as mp

def get_filenames(path):
    """
    A generator function: Iterates through all .txt files in the path and
    returns the full names of the files

    Parameters:
    - path : string, path to walk through

    Yields:
    The full filenames of all files ending in .txt
    """
    for (root, dirs, files) in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                yield f'{root}/{file}'

def get_file(path):
    """
    Reads the content of the file and returns it as a string.

    Parameters:
    - path : string, path to a file

    Return value:
    The content of the file in a string.
    """
    with open(path,'r') as f:
        return f.read()

def count_words_in_file(file):
    """
    Counts the number of occurrences of words in the file
    Whitespace is ignored

    Parameters:
    - file, string : the content of a file

    Returns: Dictionary that maps words (strings) to counts (ints)
    """
    counts = dict()
    for word in file.split():
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts



def get_top10(counts):
    """
    Determines the 10 words with the most occurrences.
    Ties can be solved arbitrarily.

    Parameters:
    - counts, dictionary : a mapping from words (str) to counts (int)
    
    Return value:
    A list of (count,word) pairs (int,str)
    """
    counts_tuples = []
    for word in counts.keys():
        counts_tuples.append( (counts[word], word) )

    counts_tuples = sorted(counts_tuples, key=lambda counts: counts[0])[-10::]
    counts_tuples.reverse()

    return counts_tuples


def merge_counts(dict_to, dict_from):
    """
    Merges the word counts from dict_from into dict_to, such that
    if the word exists in dict_to, then the count is added to it,
    otherwise a new entry is created with count from dict_from

    Parameters:
    - dict_to, dictionary : dictionary to merge to
    - dict_from, dictionary : dictionary to merge from

    Return value: None
    """
    for (k,v) in dict_from.items():
        if k not in dict_to:
            dict_to[k] = v
        else:
            dict_to[k] += v



def compute_checksum(counts):
    """
    Computes the checksum for the counts as follows:
    The checksum is the sum of products of the length of the word and its count

    Parameters:
    - counts, dictionary : word to count dictionary

    Return value:
    The checksum (int)
    """
    sum = 0
    for i in counts.keys():
        sum += len(i) * counts[i]

    return sum


if __name__ == '__main__':

    start = time.time()
    
    # 1. Parse arguments
    parser = argparse.ArgumentParser(description='Counts words of all the text files in the given directory')
    parser.add_argument('-w', '--num-workers', help = 'Number of workers', default=1, type=int)
    parser.add_argument('-b', '--batch-size', help = 'Batch size', default=1, type=int)
    parser.add_argument('path', help = 'Path that contains text files')
    args = parser.parse_args()

    path = args.path

    if not os.path.isdir(path):
        sys.stderr.write(f'{sys.argv[0]}: ERROR: `{path}\' is not a valid directory!\n')
        quit(1)

    num_workers = args.num_workers
    if num_workers < 1:
        sys.stderr.write(f'{sys.argv[0]}: ERROR: Number of workers must be positive (got {num_workers})!\n')
        quit(1)

    batch_size = args.batch_size
    if batch_size < 1:
        sys.stderr.write(f'{sys.argv[0]}: ERROR: Batch size must be positive (got {batch_size})!\n')
        quit(1)

    t1 = time.time()

    # 2. Get the content of all files (Parallelizable)
    files = [get_file(fn) for fn in get_filenames(path)]
    t2 = time.time()

    # 3. Count the word occurences for each file (Parallelizable)
    file_counts = list()
    for file in files:
        file_counts.append(count_words_in_file(file))
    t3 = time.time()

    # 4. Merge the word occurences into a single dict (Sequential)
    global_counts = dict()
    for counts in file_counts:
        merge_counts(global_counts,counts)

    end = time.time()

    t_total = end - start
    t_parallel = t3 - t1
    t_sequential = (end - t3) + (t1 - start)

    print(f"total time: {t_total}")
    print(f"parallel time: {t_parallel}")
    print(f"sequential time: {t_sequential}")
    print(f"parallel portion: {t_parallel/t_total}")
    print(f"sequential portion: {t_sequential/t_total}")

    print(f"block 1 (parse arguments)     : {t1 - start}")
    print(f"block 1 (get content of files): {t2 - t1}")
    print(f"block 2 (count the occurences): {t3 - t2}")
    print(f"block 3 (merge the occurences): {end - t3}")

    top_10 = get_top10(global_counts)
    print("Top10 words (occurence)")
    for t in top_10:
        print(f"{t[1]}: {t[0]}")

    print(f"Checksum: {compute_checksum(global_counts)}")
