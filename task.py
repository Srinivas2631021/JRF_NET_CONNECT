from db import get_connection

# ==========================================================
# CREATE - NEW CANDIDATE REGISTRATION
# ==========================================================

def add_candidate():

    connection = None

    try:
        print("\n========== New Candidate Registration ==========")

        name = input("Enter candidate name: ")
        email = input("Enter email: ")
        phone = input("Enter phone number: ")
        qualification = input("Enter qualification: ")
        specialization = input("Enter specialization: ")
        net_subject = input("Enter NET subject: ")

        connection = get_connection()
        cur = connection.cursor()

        query = """
        INSERT INTO candidates
        (
            name,
            email,
            phone,
            qualification,
            specialization,
            net_subject
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cur.execute(
            query,
            (
                name,
                email,
                phone,
                qualification,
                specialization,
                net_subject
            )
        )

        connection.commit()

        print("\nCandidate registered successfully.")

    except psycopg2.errors.UniqueViolation:
        if connection:
            connection.rollback()

        print("\nError: Email already exists.")

    except Exception as error:

        if connection:
            connection.rollback()

        print("Error:", error)

    finally:
        if connection:
            connection.close()


# ==========================================================
# READ - VIEW ALL CANDIDATES
# ==========================================================

def show_candidates():

    connection = None

    try:

        connection = get_connection()
        cur = connection.cursor()

        query = """
        SELECT
            candidate_id,
            name,
            email,
            phone,
            qualification,
            specialization,
            net_subject,
            created_at
        FROM candidates
        ORDER BY candidate_id
        """

        cur.execute(query)

        records = cur.fetchall()

        if records:

            print("\n========== Registered Candidates ==========")

            for record in records:

                print("----------------------------------------")

                print(f"Candidate ID   : {record[0]}")
                print(f"Name           : {record[1]}")
                print(f"Email          : {record[2]}")
                print(f"Phone          : {record[3]}")
                print(f"Qualification  : {record[4]}")
                print(f"Specialization : {record[5]}")
                print(f"NET Subject    : {record[6]}")
                print(f"Registered On  : {record[7]}")

        else:

            print("\nNo candidates found.")

    except Exception as error:

        print("Error:", error)

    finally:

        if connection:
            connection.close()


# ==========================================================
# SEARCH CANDIDATE
# ==========================================================

def search_candidate():

    connection = None

    try:

        search_value = input(
            "\nEnter candidate name or email to search: "
        )

        connection = get_connection()
        cur = connection.cursor()

        query = """
        SELECT
            candidate_id,
            name,
            email,
            phone,
            qualification,
            specialization,
            net_subject
        FROM candidates
        WHERE name ILIKE %s
           OR email LIKE %s
        ORDER BY candidate_id
        """

        search_pattern = f"%{search_value}%"

        cur.execute(
            query,
            (search_pattern, search_pattern)
        )

        records = cur.fetchall()

        if records:

            print("\n========== Search Results ==========")

            for record in records:

                print("----------------------------------------")

                print(f"Candidate ID   : {record[0]}")
                print(f"Name           : {record[1]}")
                print(f"Email          : {record[2]}")
                print(f"Phone          : {record[3]}")
                print(f"Qualification  : {record[4]}")
                print(f"Specialization : {record[5]}")
                print(f"NET Subject    : {record[6]}")

        else:

            print("\nNo candidate found.")

    except Exception as error:

        print("Error:", error)

    finally:

        if connection:
            connection.close()


# ==========================================================
# UPDATE CANDIDATE
# ==========================================================

def update_candidate():

    connection = None

    try:

        candidate_id = int(
            input("\nEnter candidate ID to update: ")
        )

        print("\nEnter new candidate details.")

        name = input("Enter name: ")
        email = input("Enter email: ")
        phone = input("Enter phone number: ")
        qualification = input("Enter qualification: ")
        specialization = input("Enter specialization: ")
        net_subject = input("Enter NET subject: ")

        connection = get_connection()
        cur = connection.cursor()

        query = """
        UPDATE candidates
        SET
            name = %s,
            email = %s,
            phone = %s,
            qualification = %s,
            specialization = %s,
            net_subject = %s
        WHERE candidate_id = %s
        """

        cur.execute(
            query,
            (
                name,
                email,
                phone,
                qualification,
                specialization,
                net_subject,
                candidate_id
            )
        )

        if cur.rowcount == 0:

            print("\nCandidate not found.")

        else:

            connection.commit()

            print("\nCandidate updated successfully.")

    except ValueError:

        print("\nCandidate ID must be an integer.")

    except Exception as error:

        if connection:
            connection.rollback()

        print("Error:", error)

    finally:

        if connection:
            connection.close()


# ==========================================================
# DELETE CANDIDATE
# ==========================================================

def delete_candidate():

    connection = None

    try:

        candidate_id = int(
            input("\nEnter candidate ID to delete: ")
        )

        connection = get_connection()
        cur = connection.cursor()

        query = """
        DELETE FROM candidates
        WHERE candidate_id = %s
        """

        cur.execute(
            query,
            (candidate_id,)
        )

        if cur.rowcount == 0:

            print("\nCandidate not found.")

        else:

            connection.commit()

            print("\nCandidate deleted successfully.")

    except ValueError:

        print("\nCandidate ID must be an integer.")

    except Exception as error:

        if connection:
            connection.rollback()

        print("Error:", error)

    finally:

        if connection:
            connection.close()