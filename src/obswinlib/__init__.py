from .add_tapers import add_tapers
from .io import write_jsonfile, write_txtfile, \
    load_window_config_yaml, load_window_config_toml
from .multiqueue import multiwrapper
from .queue_multiwindow_stream import queue_multiwindow_stream
from .stream_cost_win import stream_cost_win
from .stream_grad_frechet_win import stream_grad_frechet_win
from .stream_grad_hess_win import stream_grad_hess_win
from .utils import split_stream_inv, Timer, read_toml, read_yaml, \
    sort_windows_on_channel, sort_windows_on_channel_and_location, \
    pick_location_with_more_windows, pick_channel_with_more_windows, \
    merge_instruments_window, merge_windows, generate_log_content, \
    merge_channels_window, merge_station_windows, stats_all_windows
from .window import window_on_stream, window_on_trace, update_user_levels, \
    plot_window_figure, merge_trace_windows

__all__ = [
    'add_tapers',
    'generate_log_content',
    'load_window_config_toml',
    'load_window_config_yaml',
    'multiwrapper',
    'merge_windows',
    'merge_channels_window',
    'merge_instruments_window',
    'merge_station_windows',
    'merge_trace_windows',
    'pick_location_with_more_windows',
    'pick_channel_with_more_windows',
    'plot_window_figure',
    'queue_multiwindow_stream',
    'read_toml',
    'read_yaml',
    'sort_windows_on_channel',
    'sort_windows_on_channel_and_location',
    'split_stream_inv',
    'stats_all_windows',
    'stream_cost_win',
    'stream_grad_frechet_win',
    'stream_grad_hess_win',
    'Timer',
    'update_user_levels',
    'window_on_stream',
    'window_on_trace',
    'write_jsonfile',
    'write_txtfile',
]

try:
    import mpi4py # noqa
    from .mpi import mpi_window
    __all__.append("mpi_window")
except ImportError as e:
    print(e)
