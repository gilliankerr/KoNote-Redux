"""Canadian localisation validators and normalisers for client fields.

Provides validation and normalisation for:
- Canadian postal codes (I18N5)
- Canadian phone numbers (I18N5b)

These are used by the custom field save logic to clean data on save.
Each CustomFieldDefinition has a `validation_type` field that determines
which validator/normaliser to apply (I18N-FIX2).
"""
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# ---------------------------------------------------------------------------
# Keywords for auto-detecting validation type from field names (I18N-FIX2)
# ---------------------------------------------------------------------------
POSTAL_KEYWORDS = ["postal", "code postal", "zip"]
PHONE_KEYWORDS = ["phone", "téléphone", "tel"]


def detect_validation_type(field_name):
    """Auto-detect validation type from a field name.

    Used when creating new custom fields to set a sensible default
    for validation_type based on the field name.

    Returns one of: "postal_code", "phone", or "none".
    """
    name_lower = field_name.lower()
    if any(kw in name_lower for kw in POSTAL_KEYWORDS):
        return "postal_code"
    if any(kw in name_lower for kw in PHONE_KEYWORDS):
        return "phone"
    return "none"


# ---------------------------------------------------------------------------
# I18N5: Canadian Postal Code
# ---------------------------------------------------------------------------
# Format: A1A 1A1 (letter-digit-letter space digit-letter-digit)
# Accepts with or without space; normalises to uppercase with space.
POSTAL_CODE_RE = re.compile(r'^[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d$')


def validate_postal_code(value):
    """Validate a Canadian postal code.

    Accepts "A1A 1A1" or "A1A1A1" (case-insensitive).
    Raises ValidationError if the format is invalid.
    """
    if not value:
        return  # Empty is OK (field may be optional)
    value = value.strip()
    if not POSTAL_CODE_RE.match(value):
        raise ValidationError(
            _("Enter a valid Canadian postal code (e.g., A1A 1A1)."),
            code="invalid_postal_code",
        )


def normalize_postal_code(value):
    """Normalise a Canadian postal code to 'A1A 1A1' format.

    - Strips whitespace
    - Converts to uppercase
    - Inserts space after the third character if missing
    - Returns empty string for empty input
    """
    if not value:
        return ""
    value = value.strip().upper().replace(" ", "")
    if len(value) == 6:
        return f"{value[:3]} {value[3:]}"
    # If it doesn't match expected length, return as-is (validation catches it)
    return value


# ---------------------------------------------------------------------------
# I18N5b: Canadian Phone Numbers
# ---------------------------------------------------------------------------
# Accepts: (613) 555-1234, 613-555-1234, 6135551234, 613.555.1234,
#           +1 613 555 1234, +16135551234, 1-613-555-1234
# Normalises to: (613) 555-1234
PHONE_DIGITS_RE = re.compile(r'[^\d]')


def validate_phone_number(value):
    """Validate a Canadian/North American phone number.

    Accepts many common formats. The number must contain exactly
    10 digits (or 11 if starting with country code 1).
    Raises ValidationError if invalid.
    """
    if not value:
        return  # Empty is OK (field may be optional)
    digits = PHONE_DIGITS_RE.sub('', value.strip())
    # Strip leading country code '1'
    if len(digits) == 11 and digits[0] == '1':
        digits = digits[1:]
    if len(digits) != 10:
        raise ValidationError(
            _("Enter a valid phone number with 10 digits (e.g., (613) 555-1234)."),
            code="invalid_phone",
        )


def normalize_phone_number(value):
    """Normalise a phone number to '(613) 555-1234' format.

    - Strips all non-digit characters
    - Removes leading country code '1' if present
    - Formats as (XXX) XXX-XXXX
    - Returns empty string for empty input
    - Returns the original value (stripped) if it cannot be normalised
    """
    if not value:
        return ""
    digits = PHONE_DIGITS_RE.sub('', value.strip())
    # Strip leading country code '1'
    if len(digits) == 11 and digits[0] == '1':
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    # Can't normalise — return stripped original
    return value.strip()


# ---------------------------------------------------------------------------
# Field name matching helpers (DEPRECATED — kept for backward compatibility)
# ---------------------------------------------------------------------------
# These are superseded by CustomFieldDefinition.validation_type (I18N-FIX2).
# Use field_def.validation_type == "postal_code" or "phone" instead.

# Field names that contain postal code data
POSTAL_CODE_FIELD_NAMES = {"Postal Code"}

# Field names that contain phone numbers
PHONE_FIELD_NAMES = {
    "Primary Phone",
    "Secondary Phone",
    "Emergency Contact Phone",
    "Parent/Guardian Phone",
    "Secondary Parent/Guardian Phone",
}


def is_postal_code_field(field_name):
    """Check if a custom field name represents a postal code.

    DEPRECATED: Use field_def.validation_type == "postal_code" instead.
    """
    return field_name in POSTAL_CODE_FIELD_NAMES


def is_phone_field(field_name):
    """Check if a custom field name represents a phone number.

    DEPRECATED: Use field_def.validation_type == "phone" instead.
    """
    return field_name in PHONE_FIELD_NAMES
