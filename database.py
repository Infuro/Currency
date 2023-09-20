import psycopg2


def connect():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres",
        port="5432"
    )
    return conn


def create_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS policy_map;")
    cursor.execute('''create table policy_map
    ( id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      description VARCHAR(255),
      config json,
      port_channel_id INTEGER,
      max_frame_size INTEGER);
    ''')


def insert_policies(cursor, policies):
    for policy_map in policies:
        insert_data = "INSERT INTO policy_map (id, name, description, config, port_channel_id, max_frame_size) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(
            insert_data,
            (policy_map.id,
             policy_map.name,
             policy_map.description,
             policy_map.config,
             policy_map.port_channel_id,
             policy_map.max_frame_size)
        )
