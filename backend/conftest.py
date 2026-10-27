import os

os.environ.setdefault("PGHOST", "localhost")
os.environ.setdefault("PGPORT", "5432")
os.environ.setdefault("PGUSER", "postgres")
os.environ.setdefault("PGPASSWORD", "postgres")
os.environ.setdefault("PGDATABASE", "profound_interview")
os.environ.setdefault("PROFOUND_API_BEARER_TOKEN", "test-token")
