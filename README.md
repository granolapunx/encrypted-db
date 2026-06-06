# ENCRYPTED DATABASE PROJECT — ROADMAP

## PHASE 1 — Local encrypted notes CLI
Goal: a working command-line app that encrypts data before it hits disk.
Everything you build here carries forward to Phase 2.

### Steps:
  1. Key derivation
     - Install: pip install cryptography
     - Derive a Fernet key from a password using PBKDF2HMAC + SHA256
     - Generate a salt (random bytes, stored alongside encrypted data)
     - Understand: same password + same salt = same key every time

  2. Encrypt / decrypt
     - Use Fernet(key).encrypt() and .decrypt()
     - Handle bytes vs strings (common gotcha)
     - Test: encrypt a string, decrypt it back, confirm they match

  3. SQLite record store
     - Store encrypted blobs in a local .db file using sqlite3 or SQLAlchemy
     - Schema: id, encrypted_data, salt, created_at
     - Write insert and fetch functions

  4. CLI (click or typer)
     - Commands: add, view, search, delete
     - Prompt for password on launch, derive key, hold in memory for session
     - Wire commands to the database functions

Estimated time: 4-6 hours across a few sessions


## PHASE 2 — Cloud encrypted database
Goal: move the SQLite backend to a cloud Postgres instance (Supabase).
The encryption layer from Phase 1 stays exactly the same.

### Steps:
  1. Cloud backend
     - Sign up for Supabase (free tier)
     - Create a Postgres database and grab the connection string
     - Swap SQLite connection for SQLAlchemy + Postgres

  2. App-layer encryption
     - Confirm: data is encrypted in Python BEFORE being sent to Supabase
     - Supabase stores ciphertext blobs only — provider never sees plaintext
     - Test: check Supabase dashboard and confirm data is unreadable

  3. User auth + roles
     - Add a users table with bcrypt-hashed passwords
     - Implement role-based access control (RBAC)
     - Different users see different records based on role

  4. Audit logging
     - Log every read, write, failed access with timestamp + user ID
     - Use SQLAlchemy event listeners or a simple log table
     - Non-negotiable for HIPAA later


## PHASE 3 — HIPAA compliance layer
Goal: harden Phase 2 into something that could handle real client records.
Note: true HIPAA compliance also involves administrative/physical safeguards
beyond code — this covers the technical safeguards portion.

### Steps:
  1. Minimum necessary access
     - Field-level encryption: sensitive fields encrypted individually
     - Role permissions scoped to minimum required data per user

  2. Key management
     - Envelope encryption: data keys encrypted by a master key
     - Key rotation: ability to re-encrypt data with a new key
     - Never store plaintext keys alongside encrypted data

  3. Technical safeguards
     - TLS for all data in transit (Supabase handles this)
     - Integrity controls: detect tampering (Fernet HMAC covers this)
     - Session timeouts, failed login lockouts


## STACK
  cryptography     — Fernet encryption, PBKDF2 key derivation
  SQLAlchemy       — ORM, works with both SQLite and Postgres
  sqlite3          — Phase 1 local storage
  Supabase         — Phase 2 cloud Postgres hosting
  click or typer   — CLI framework
  bcrypt           — Password hashing for user auth
  python-dotenv    — Keep connection strings out of your code


## FRIDAY SESSION GOAL

Get Phase 1 Step 1 working end to end:
  - Password in → PBKDF2 → Fernet key out
  - Encrypt a test string, decrypt it back
  - Salt generated, stored, and reused correctly

Notes for gabe: 
- Install VS Code and Python 
