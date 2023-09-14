"""

This will not be executed as part of the pytest suite, but can be invoked by

.. code:: bash

    mpirun -np 4 python test_process_mpi.py

"""

import os
import obspy
import obswinlib as owl


SCRIPT = os.path.abspath(__file__)
SCRIPTDIR = os.path.dirname(__file__)
TESTDATABASE = os.path.join(SCRIPTDIR, "testdatabase")
DATADIR = os.path.join(TESTDATABASE, "data")
CMTFILE = os.path.join(TESTDATABASE, "C200811240902A")
OBSERVED = os.path.join(DATADIR, "processed_observed.mseed")
SYNTHETIC = os.path.join(DATADIR, "processed_synthetic.mseed")
STATIONS = os.path.join(TESTDATABASE, "stations.xml")
WINDOWFILE = os.path.join(TESTDATABASE, "window.yml")


def test_queue_multiwindow():

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

    # Window the thing
    windowed_stream = owl.queue_multiwindow_stream(
        observed, synthetic, wrapwindowdict, nproc=4)

    # Check windowing
    for tr in windowed_stream:
        print(len(tr.stats.windows))


if __name__ == "__main__":

    test_queue_multiwindow()
