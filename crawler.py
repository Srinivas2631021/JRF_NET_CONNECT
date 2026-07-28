import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

from db import get_connection


# JNTUH notifications page
JNTUH_URL = "https://jntuh.ac.in/notifications"

# Base URL
BASE_URL = "https://jntuh.ac.in"


def crawl_jntuh_notifications():

    connection = None

    try:

        print("\n==========================================")
        print("      JRF_NET - JNTUH NOTIFICATION CRAWLER")
        print("==========================================")

        # -------------------------------------------------
        # STEP 1: Fetch JNTUH website
        # -------------------------------------------------

        print("\nConnecting to JNTUH website...")

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(
            JNTUH_URL,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        print(
            "JNTUH website accessed successfully."
        )

        print(
            f"Response status: {response.status_code}"
        )

        # -------------------------------------------------
        # STEP 2: Parse HTML
        # -------------------------------------------------

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # -------------------------------------------------
        # STEP 3: Find all links
        # -------------------------------------------------

        all_links = soup.find_all("a")

        print(
            f"\nTotal links found on page: "
            f"{len(all_links)}"
        )

        notifications = []

        # -------------------------------------------------
        # STEP 4: Extract notification links
        # -------------------------------------------------

        for link in all_links:

            title = link.get_text(
                " ",
                strip=True
            )

            href = link.get("href")

            # Skip invalid links
            if not title or not href:
                continue

            # Convert relative URL to absolute URL
            notification_url = urljoin(
                BASE_URL,
                href
            )

            # -------------------------------------------------
            # Identify possible notification links
            # -------------------------------------------------

            lower_title = title.lower()
            lower_url = notification_url.lower()

            if (
                "notification" in lower_title
                or "recruitment" in lower_title
                or "jrf" in lower_title
                or "project" in lower_title
                or "research" in lower_title
                or "faculty" in lower_title
                or "assistant professor" in lower_title
                or "associate professor" in lower_title
                or "professor" in lower_title
                or "walk-in" in lower_title
                or "contract" in lower_title
                or "pdf" in lower_url
                or "uploads" in lower_url
            ):

                notifications.append(
                    {
                        "title": title,
                        "url": notification_url
                    }
                )

        # -------------------------------------------------
        # Remove duplicate URLs
        # -------------------------------------------------

        unique_notifications = {}

        for notification in notifications:

            unique_notifications[
                notification["url"]
            ] = notification["title"]

        notifications = [
            {
                "title": title,
                "url": url
            }
            for url, title
            in unique_notifications.items()
        ]

        print(
            f"\nPossible notifications found: "
            f"{len(notifications)}"
        )

        # -------------------------------------------------
        # If no notifications found
        # -------------------------------------------------

        if not notifications:

            print(
                "\nNo notifications found."
            )

            print(
                "Please check the JNTUH website HTML "
                "structure."
            )

            return

        # -------------------------------------------------
        # STEP 5: Connect to PostgreSQL
        # -------------------------------------------------

        print(
            "\nConnecting to PostgreSQL..."
        )

        connection = get_connection()

        cur = connection.cursor()

        print(
            "PostgreSQL connection successful."
        )

        # -------------------------------------------------
        # STEP 6: Insert notifications
        # -------------------------------------------------

        inserted_count = 0

        duplicate_count = 0

        for notification in notifications:

            title = notification["title"]

            notification_url = notification["url"]

            query = """
            INSERT INTO notifications
            (
                university,
                title,
                notification_date,
                notification_url
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            ON CONFLICT (notification_url)
            DO NOTHING
            """

            cur.execute(
                query,
                (
                    "JNTUH",
                    title,
                    datetime.now().date(),
                    notification_url
                )
            )

            if cur.rowcount == 1:

                inserted_count += 1

                print(
                    f"\n[INSERTED]"
                )

                print(
                    f"Title : {title}"
                )

                print(
                    f"URL   : {notification_url}"
                )

            else:

                duplicate_count += 1

        # -------------------------------------------------
        # STEP 7: Commit database changes
        # -------------------------------------------------

        connection.commit()

        # -------------------------------------------------
        # STEP 8: Final result
        # -------------------------------------------------

        print(
            "\n=========================================="
        )

        print(
            "      CRAWLING COMPLETED"
        )

        print(
            "=========================================="
        )

        print(
            f"New notifications inserted : "
            f"{inserted_count}"
        )

        print(
            f"Duplicate notifications    : "
            f"{duplicate_count}"
        )

        print(
            f"Total processed             : "
            f"{len(notifications)}"
        )

    except requests.exceptions.RequestException as error:

        print(
            "\nError while accessing JNTUH website:"
        )

        print(error)

    except Exception as error:

        if connection:

            connection.rollback()

        print(
            "\nCrawler error:"
        )

        print(error)

    finally:

        if connection:

            connection.close()

            print(
                "\nPostgreSQL connection closed."
            )


if __name__ == "__main__":

    crawl_jntuh_notifications()