import re

def chunk_plsql_all(text):
    # Patterns for the main code block types
    patterns = [
        r"CREATE\s+(OR\s+REPLACE\s+)?(PROCEDURE|FUNCTION|TRIGGER|TYPE)\s+.*?END\s*;",  # Full PL/SQL units
        r"DECLARE\s+.*?END\s*;",  # Anonymous PL/SQL blocks
        r"BEGIN\s+.*?END\s*;",    # Standalone BEGIN blocks
        r"(CREATE\s+TABLE\s+.*?;)",     # DDL
        r"(ALTER\s+TABLE\s+.*?;)",      # Foreign keys
        r"(DROP\s+TABLE\s+.*?;)",       # Drop table
        r"(INSERT\s+INTO\s+.*?;)",      # Inserts
        r"(SELECT\s+.*?;)",             # Raw selects
        r"(SET\s+SERVEROUTPUT\s+ON\s*;)" # Server output
    ]

    combined_pattern = "|".join(f"({p})" for p in patterns)
    regex = re.compile(combined_pattern, re.IGNORECASE | re.DOTALL)

    matches = regex.findall(text)

    # Flatten regex match groups and filter out empty results
    raw_chunks = [item for group in matches for item in group if item.strip() != ""]
    clean_chunks = [chunk.strip() for chunk in raw_chunks]

    return clean_chunks