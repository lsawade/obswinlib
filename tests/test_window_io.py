import os
import inspect
from obspy import read, read_inventory, read_events
import pyflex
import obswinlib as owl


def _upper_level(path, nlevel=4):
    """
    Go the nlevel dir up
    """
    for i in range(nlevel):
        path = os.path.dirname(path)
    return path


# Most generic way to get the data folder path.
TESTBASE_DIR = _upper_level(os.path.abspath(__file__), 1)
DATA_DIR = os.path.join(TESTBASE_DIR, "data")
obsfile = os.path.join(DATA_DIR, "proc", "IU.KBL.obs.proc.mseed")
synfile = os.path.join(DATA_DIR, "proc", "IU.KBL.syn.proc.mseed")
staxml = os.path.join(DATA_DIR, "stationxml", "IU.KBL.xml")
quakeml = os.path.join(DATA_DIR, "quakeml", "C201009031635A.xml")
config_file_yaml = os.path.join(DATA_DIR, "window", "27_60.BHZ.config.yaml")
config_file_toml = os.path.join(DATA_DIR, "window", "27_60.BHZ.config.toml")

def test_load_window_config_yaml():

    config = owl.load_window_config_yaml(config_file_yaml)
    assert isinstance(config, pyflex.Config)
    assert config.max_period == 60.0
    assert config.min_period == 27.0
    assert config.stalta_waterlevel == 0.10


def test_load_window_config_toml():

    config = owl.load_window_config_toml(config_file_toml)
    assert isinstance(config, pyflex.Config)
    assert config.max_period == 60.0
    assert config.min_period == 27.0
    assert config.stalta_waterlevel == 0.10


class TestWrite:

    @staticmethod
    def get_windows():
        obs_tr = read(obsfile).select(channel="*R")[0]
        syn_tr = read(synfile).select(channel="*R")[0]


        config = owl.load_window_config_yaml(config_file_yaml)
        config = owl.load_window_config_toml(config_file_toml)

        cat = read_events(quakeml)

        inv = read_inventory(staxml)
        windows = owl.window_on_trace(obs_tr, syn_tr, config, station=inv,
                                      event=cat, _verbose=False,
                                      figure_mode=False)
        return windows

    def test_write_txtfile(self, tmpdir):
        windows = self.get_windows()
        filename = os.path.join(str(tmpdir), "window.txt")
        owl.write_txtfile(windows, filename)

    def test_write_jsonfile(self, tmpdir):
        windows = self.get_windows()
        filename = os.path.join(str(tmpdir), "window.json")
        owl.write_jsonfile(windows, filename)
