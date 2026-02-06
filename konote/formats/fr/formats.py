# French (Canadian) date and number formatting.
#
# Canada uses ISO 8601 dates (YYYY-MM-DD) in both official languages.
# French Canadian uses comma as decimal separator and space as
# thousands separator: 1 234,56 $.
# Reference: Government of Canada editorial style guide (French).

# Date formats — ISO 8601 for both languages
DATE_FORMAT = "Y-m-d"                   # 2026-02-05
SHORT_DATE_FORMAT = "Y-m-d"             # 2026-02-05
DATETIME_FORMAT = "Y-m-d H:i"          # 2026-02-05 14:30
SHORT_DATETIME_FORMAT = "Y-m-d H:i"    # 2026-02-05 14:30
DATE_INPUT_FORMATS = [
    "%Y-%m-%d",     # 2026-02-05 (ISO 8601 — primary)
    "%d/%m/%Y",     # 05/02/2026 (EU-style — common in Quebec)
    "%m/%d/%Y",     # 02/05/2026 (US-style fallback)
]

# Number formatting — French Canadian style: 1 234,56 $
DECIMAL_SEPARATOR = ","
THOUSAND_SEPARATOR = "\N{NARROW NO-BREAK SPACE}"  # Unicode thin space (U+202F)
NUMBER_GROUPING = 3
