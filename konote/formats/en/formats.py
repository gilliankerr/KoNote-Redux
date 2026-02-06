# English (Canadian) date and number formatting.
#
# Canada uses ISO 8601 dates (YYYY-MM-DD) and dollar currency with
# comma as thousands separator and period as decimal separator.
# Reference: Government of Canada editorial style guide.

# Date formats — ISO 8601 preferred in both official languages
DATE_FORMAT = "Y-m-d"                   # 2026-02-05
SHORT_DATE_FORMAT = "Y-m-d"             # 2026-02-05
DATETIME_FORMAT = "Y-m-d H:i"          # 2026-02-05 14:30
SHORT_DATETIME_FORMAT = "Y-m-d H:i"    # 2026-02-05 14:30
DATE_INPUT_FORMATS = [
    "%Y-%m-%d",     # 2026-02-05 (ISO 8601 — primary)
    "%m/%d/%Y",     # 02/05/2026 (US-style fallback)
    "%d/%m/%Y",     # 05/02/2026 (EU-style fallback)
]

# Number formatting — English Canadian style: $1,234.56
DECIMAL_SEPARATOR = "."
THOUSAND_SEPARATOR = ","
NUMBER_GROUPING = 3
