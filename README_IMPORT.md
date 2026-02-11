# Convert `courses_with_names.md` to SQL / import guide

1. Generate CSV and SQL using the included script:

```
python md_to_sql.py courses_with_names.md
```

This writes `courses.csv` and `courses.sql` in the current folder.

2. Import into SQLite (quick test):

```
sqlite3 courses.db 
.read courses.sql
```

3. Import into MySQL:

- Create table by running `courses.sql` (inspect it first).
- From shell:

```
mysql -u user -p your_database < courses.sql
```

4. Import into Postgres:

```
psql -U user -d your_database -f courses.sql
```

Notes:
- The script extracts rows from markdown tables and uses the closest preceding `##` heading as the `program` value.
- Some course names in the source markdown may be truncated or wrapped; verify entries you care about and edit `courses.csv` if you need manual cleanup before import.
- If you prefer a parameterized import, use `courses.csv` with your DB's bulk-import tool (`COPY` for Postgres, `LOAD DATA INFILE` for MySQL, or CSV import in SQLite). 
