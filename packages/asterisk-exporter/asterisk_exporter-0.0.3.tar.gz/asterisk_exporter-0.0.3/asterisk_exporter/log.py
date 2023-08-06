import logging
from asterisk_exporter import __version__

logging.basicConfig()
log = logging.getLogger("{}@{}".format("doorstation_controller", __version__))
log.setLevel(logging.INFO)
