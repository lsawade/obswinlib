import obspy
from .utils import Timer
from .utils import split_stream_inv
from .window import window_on_stream
try:
    from mpi4py import MPI
except ImportError as e:
    print(e)
    raise ImportError("MPI4PY not installed. Please install it to use MPI.")



def mpi_window(obsd: obspy.Stream | None, synt: obspy.Stream | None,
               windowdict: dict | None, verbose: bool = False):


    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:

        t = Timer()
        t.start()

        # Split the stream into different chunks
        obsdlist, syntlist, _ = split_stream_inv(
            obsd, windowdict['station'],
            synt=synt, nprocs=size)

    else:
        obsdlist = None
        syntlist = None

    # Scatter stream chunks
    obsdlist = comm.scatter(obsdlist, root=0)
    syntlist = comm.scatter(syntlist, root=0)

    # Broadcast process dictionary
    windowdict = comm.bcast(windowdict, root=0)

    if verbose:

        print(
            f"-> R/S: {rank}/{size} -- "
            f"Obs: {len(obsdlist)} -- Syn: {len(syntlist)} -- "
            f"Inv: {len(windowdict['station'].get_contents()['channels'])}",
            flush=True)

    # Process
    results = []
    result = window_on_stream(obsdlist, syntlist, **windowdict)

    if verbose:
        print(f"-> Rank: {rank}/{size} -- Done.", flush=True)

    results.append(result)

    if verbose and rank == 0:
            print("-> Gathering results")

    results = comm.gather(results, root=0)

    # Sort
    if rank == 0:
        # Flatten list of lists.
        resultst = obspy.Stream()
        for _result in results:
            resultst += _result[0]

        t.stop()

        windowed_stream = resultst

        return windowed_stream

    else:

        return None


