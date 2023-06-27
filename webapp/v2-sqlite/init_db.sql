-- Delete old table, in case you run the script multiple times.
DROP TABLE IF EXISTS todos;

-- Define format for todos (id, text, and time it was created at).
-- Below, we define defaults for id and created_at
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Insert some todos. Only specify text, because id and created_at
-- are automatically populated.
INSERT INTO todos (text) VALUES ("laundry");
INSERT INTO todos (text) VALUES ("walk the dog");