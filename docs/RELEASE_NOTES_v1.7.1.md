# AOS v1.7.1 Release Notes

## Fixed
- Removed unsupported `readonly=True` argument from NiceGUI textarea.
- Evidence preview now uses `.props('readonly')`.

## Affected error
`TypeError: got an unexpected keyword argument 'readonly'`
