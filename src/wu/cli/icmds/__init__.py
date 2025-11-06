from .darwin.general import wu_init as wu_init_darwin
from .darwin.daemon import daemon_start as daemon_start_darwin
from .darwin.daemon import daemon_stop as daemon_stop_darwin
from .darwin.daemon import daemon_load as daemon_load_darwin
from .darwin.daemon import daemon_unload as daemon_unload_darwin
from .darwin.daemon import daemon_restart as daemon_restart_darwin
from .darwin.daemon import daemon_remove as daemon_remove_darwin

from .linux.general import wu_init as wu_init_linux
from .linux.daemon import daemon_start as daemon_start_linux
from .linux.daemon import daemon_stop as daemon_stop_linux
from .linux.daemon import daemon_restart as daemon_restart_linux
from .linux.daemon import daemon_enable as daemon_enable_linux
from .linux.daemon import daemon_disable as daemon_disable_linux
