import logging
from systemd import journal

log = logging.getLogger('yas')
log.addHandler(journal.JournaldLogHandler())
log.setLevel(logging.INFO)
