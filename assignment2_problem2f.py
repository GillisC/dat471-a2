import os
import argparse
import sys
import time
import multiprocessing as mp
from multiprocessing import Process
from queue import Queue

global_dict = dict()

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

def count_words_in_file(filename_queue,wordcount_queue,batch_size):
    """
    Counts the number of occurrences of words in the file
    Performs counting until a None is encountered in the queue
    Counts are stored in wordcount_queue
    Whitespace is ignored

    Parameters:
    - filename_queue, multiprocessing queue :  will contain filenames and None as a sentinel to indicate end of input
    - wordcount_queue, multiprocessing queue : (word,count) dictionaries are put in the queue, and end of input is indicated with a None
    - batch_size, int : size of batches to process

    Returns: None
    """
    running = True
    while running:
        batch = []
        for _ in range(batch_size):
            filename = filename_queue.get()
            if filename is None: 
                wordcount_queue.put(None)
                running = False
                break
            batch.append(filename)


        for filename in batch:
            counts = dict()
            file = get_file(filename)
            for word in file.split():
                if word in counts:
                    counts[word] += 1
                else:

                    counts[word] = 1

            print(counts)
            wordcount_queue.put(counts)


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



def merge_counts(out_queue,wordcount_queue,num_workers):
    """
    Merges the counts from the queue into the shared dict global_counts. 
    Quits when num_workers Nones have been encountered.

    Parameters:
    - global_counts, manager dict : global dictionary where to store the counts
    - wordcount_queue, manager queue : queue that contains (word,count) pairs and Nones to signal end of input from a worker
    - num_workers, int : number of workers (i.e., how many Nones to expect)

    Return value: None
    """

    nones_seen = 0

    while nones_seen < 4:
        dict_from = wordcount_queue.get()
        if dict_from is None: nones_seen += 1

        for (k,v) in dict_from.items():
            if k not in global_counts:
                global_counts[k] = v
            else:
                global_counts[k] += v

    
    out_queue.put({
        "top_10": get_top10(global_counts),
        "checksum": compute_checksum(global_counts)
    })
    out_queue.put(None)

    return None



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

    # construct workers and queues
    filename_queue = Queue()
    out_queue = Queue()
    wordcount_queue = Queue()

    workers = [Process(target=count_words_in_file, args=(filename_queue,wordcount_queue,batch_size)) for _ in range(num_workers)]
    # construct a single special merger process
    merger = Process(target=merge_counts, args=(out_queue,wordcount_queue,1))

    # put filenames into the input queue
    for name in get_filenames(path): 
        filename_queue.put(name)
    for _ in range(num_workers):
        filename_queue.put(None)

    print("queue e.t.c done")

    # workers then put dictionaries for the merger
    for worker in workers:
        worker.start()

    # the merger shall return the checksum and top 10 through the out queue
    merger.start()

    print("merger done")

    while (result_dict := out_queue.get()) is not None:
        print(result_dict["top_10"])
        print(result_dict["checksum"])

