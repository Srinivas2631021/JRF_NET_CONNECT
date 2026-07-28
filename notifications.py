from db import get_connection

def create_notifications_table():
    """
    Create notifications table.
    """

    connection = None

    try:
        connection = get_connection()
        cur = connection.cursor()
        # Notifications table
        notification_query = """
        CREATE TABLE IF NOT EXISTS notifications (
            notification_id SERIAL PRIMARY KEY,
            university VARCHAR(200) NOT NULL,
            title TEXT NOT NULL,
            notification_date DATE,
            notification_url TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        cur.execute(notification_query)

        connection.commit()

        print("Database tables created successfully.")
    
    except Exception as error:
        print("Error creating tables:", error)

    finally:
        if connection:
            connection.close()