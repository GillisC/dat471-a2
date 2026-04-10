import os
import argparse
import sys
import time
import multiprocessing as mp
from multiprocessing import Process, Queue


global_counts = dict()

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
    #print(f"[DEBUG] Process {os.getpid()} entered count_words_in_file", flush=True)
    exit_process = False

    while True:
        batch = []
        for _ in range(batch_size):
            #print(f"[DEBUG] Process {os.getpid()} waiting for filename...", flush=True)
            filename = filename_queue.get()
            #print(f"[DEBUG] Process {os.getpid()} got {filename}", flush=True)
            if filename is None: 
                #print(f"[DEBUG] Process {os.getpid()} got None", flush=True)
                exit_process = True
                break
            batch.append(filename)


        counts = {}
        for name in batch:
            file = get_file(name)
            for word in file.split():
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
        wordcount_queue.put(counts)

        if exit_process: 
            break

    wordcount_queue.put(None)


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

    while nones_seen < num_workers:
        dict_from = wordcount_queue.get()
        if dict_from is None: 
            nones_seen += 1
            continue

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
    print("starting now")
    start = time.time()
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


    #print(f"[DEBUG] number of workers: {num_workers}", flush=True)

    # construct workers and queues
    filename_queue = Queue()
    out_queue = Queue()
    wordcount_queue = Queue()

    # we provisioon workers - 2 so that we leave space for the main and merger process
    workers = [Process(target=count_words_in_file, args=(filename_queue,wordcount_queue,batch_size)) for _ in range(num_workers - 2)]
    merger = Process(target=merge_counts, args=(out_queue,wordcount_queue,num_workers))

    # construct a single special merger process
    merger.start()

    for worker in workers:
        worker.start()

    # put filenames into the input queue
    for name in get_filenames(path): 
        filename_queue.put(name)
    for _ in range(num_workers):
        filename_queue.put(None)

    # workers then put dictionaries for the merger

    # the merger shall return the checksum and top 10 through the out queue
    while (result_dict := out_queue.get()) is not None:
        print(result_dict["top_10"])
        print(result_dict["checksum"])

    end = time.time()
    t_total = end - start
    print(f"total time: {t_total}")

    # join the workers up
    merger.join()
    for worker in workers:
        worker.join()
