from db import get_connection

def create_candidates_table():
    """
    Create candidates table.
    """

    connection = None

    try:
        connection = get_connection()
        cur = connection.cursor()

        # Candidates table
        candidate_query = """
        CREATE TABLE IF NOT EXISTS candidates (
            candidate_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            phone VARCHAR(15),
            qualification VARCHAR(100),
            specialization VARCHAR(100),
            net_subject VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        cur.execute(candidate_query)

        connection.commit()
        
        print("Database tables created successfully.")
    
    except Exception as error:
        print("Error creating tables:", error)

    finally:
        if connection:
            connection.close()