"""

This will not be executed as part of the pytest suite, but can be invoked by

.. code:: bash

    mpirun -np 4 python test_process_mpi.py

"""

import os
import obspy
import obswinlib as owl

try:
    import mpi4py
    mpimode = True
except ImportError as e:
    print(e)
    mpimode = False

SCRIPT = os.path.abspath(__file__)
SCRIPTDIR = os.path.dirname(__file__)
TESTDATABASE = os.path.join(SCRIPTDIR, "testdatabase")
DATADIR = os.path.join(TESTDATABASE, "data")
CMTFILE = os.path.join(TESTDATABASE, "C200811240902A")
OBSERVED = os.path.join(DATADIR, "processed_observed.mseed")
SYNTHETIC = os.path.join(DATADIR, "processed_synthetic.mseed")
STATIONS = os.path.join(TESTDATABASE, "stations.xml")
WINDOWFILE = os.path.join(TESTDATABASE, "window.yml")


def manual_test_mpiwindowing():

    if mpimode:

        # Initialize MPIprocess class
        WC = owl.MPIWindowStream()

        if WC.rank == 0:
            print("MPI MODE")
            print(f"RANK: {WC.rank}")

            # Loading and fixing the processin dictionary
            windowdict = owl.read_yaml(WINDOWFILE)

            # Wrap window dictionary
            wrapwindowdict = dict(
                station=obspy.read_inventory(STATIONS),
                event=obspy.read_events(CMTFILE)[0],
                config_dict=windowdict,
                _verbose=False
            )

            # Load waveforms
            observed = obspy.read(OBSERVED)
            synthetic = obspy.read(SYNTHETIC)

            # Print stuff
            WC.get_streams_and_windowdict(observed, synthetic, wrapwindowdict)

        WC.window()

        # if WC.rank == 0:
        #     for _tr in WC.windowed_stream:
        #         print(_tr.id)
        #         try:
        #             print(len(_tr.stats.windows))
        #         except Exception:
        #             print(_tr.stats)

    else:
        print("NOT MPI MODE")
        return


if __name__ == "__main__":

    manual_test_mpiwindowing()
