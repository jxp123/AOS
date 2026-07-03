
# AOS v0.6 Architecture

## Rule
UI -> Services/Repository -> Database

No UI screen should directly own or duplicate database state.

## AI workflow
SQLite -> Repository -> Validation -> apiary_state.json -> ChatGPT

## Next
v0.6.1 restores full CRUD on top of the repository layer.
