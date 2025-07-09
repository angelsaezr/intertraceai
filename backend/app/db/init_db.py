import sqlite3

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect("intertraceai.db")
cursor = conn.cursor()

# Create a table named 'documents' if it does not already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

# Create a table named 'usuarios' if it does not already exist
docs = [
    ("Recibo.pdf",),
    ("Contrato.docx",),
    ("Informe.xlsx",),
]
cursor.executemany("INSERT INTO documents (name) VALUES (?)", docs)
conn.commit()

# Documents inserted
print("Documents in database:")
cursor.execute("SELECT * FROM documents")
for row in cursor.fetchall():
    print(row)

# Update the table to include 'edad' and 'email'
cursor.execute("UPDATE documents SET name = ? WHERE id = ?", ("Recibo actualizado.pdf", 1))
conn.commit()

# Delete a document
cursor.execute("DELETE FROM documents WHERE name = ?", ("Informe.xlsx",))
conn.commit()

# Show the updated documents
print("\nAfter update and delere:")
cursor.execute("SELECT * FROM documents")
for row in cursor.fetchall():
    print(row)

# Close the database connection
conn.close()