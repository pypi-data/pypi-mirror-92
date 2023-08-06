import re

# Default pattern matches most version strings for final versions, such as
# v.1.0.0, v1.0.0, 1.0.0, version-1.0.0, release-1.0.0
DEFAULT_VERSION_PATTERN = r"^.*?(\d+\.\d+\.\d+)$"