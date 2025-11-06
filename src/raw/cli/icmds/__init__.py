from .darwin.general import raw_init as raw_init_darwin
from .darwin.daemon import daemon_start as daemon_start_darwin
from .darwin.daemon import daemon_stop as daemon_stop_darwin
from .darwin.daemon import daemon_restart as daemon_restart_darwin

from .linux.general import raw_init as raw_init_linux
from .linux.daemon import daemon_start as daemon_start_linux
from .linux.daemon import daemon_stop as daemon_stop_linux
from .linux.daemon import daemon_restart as daemon_restart_linux
from .linux.daemon import daemon_enable as daemon_enable_linux
from .linux.daemon import daemon_disable as daemon_disable_linux
