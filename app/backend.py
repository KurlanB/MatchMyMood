import json
from urllib.request import urlopen
import random

# Dictionary mapping moods to genres
mood_to_genre = {
    "Unmotivated / Lazy": [
        "Motivational", 
        "Self-help", 
        "Poetry", 
        "Short stories"
    ],
    "Stressed / Overwhelmed": [
        "Cozy fiction", 
        "Light romance", 
        "Mindfulness"
    ],
    "Sad / Heartbroken": [
        "Happy endings", 
        "Inspirational memoirs", 
    ],
    "Happy / Excited": [
        "Adventure", 
        "Comedies"
    ],
    "Curious / Intellectual": [
        "Science", 
        "History", 
        "Philosophy", 
        "Mystery", 
        "Thriller", 
    ],
    "Angry / Frustrated": [
        "Action-packed thrillers", 
        "Revenge stories", 
    ],
    "Bored / Restless": [
        "Graphic novels", 
    ],
    "Romantic / Dreamy": [
        "Romance novels", 
        "Fantasy romance", 
        "Poetry"
    ],
    "Inspired / Creative": [
        "Creativity", 
        "Art", 
        "Fantasy", 
        "Biographies"
    ],
    "Nostalgic / Reflective": [
        "Historical fiction", 
        "Memoirs"
    ]
}

def recommend_book_by_mood(mood):
    # Check if the mood exists
    if mood not in mood_to_genre:
        print(f"Mood '{mood}' not found. Please choose from the provided list.")
        return

    # Select a random genre from the mood list
    selected_genre = random.choice(mood_to_genre[mood])
    print(f"\nSelected Genre for '{mood}': {selected_genre}")

    # Send API request for a book from the selected genre
    try:
        api = "https://www.googleapis.com/books/v1/volumes?q=subject:"
        resp = urlopen(api + selected_genre.replace(" ", "+"))
        book_data = json.load(resp)

        # Check if any books were returned
        if "items" not in book_data:
            print(f"No books found for genre: {selected_genre}")
            return

        # Select a random book from the genre
        random_index = random.randint(0, len(book_data["items"]) - 1)
        volume_info = book_data["items"][random_index]["volumeInfo"]
        
        # Extract and display book details
        title = volume_info.get("title", "Unknown Title")
        author = volume_info.get("authors", ["Unknown Author"])
        prettify_author = ", ".join(author)
        description = volume_info.get("description", "No description available.")
        link = volume_info.get("infoLink", "No link available.")
        
        print("\nYour Book Recommendation:")
        print(f"Title: {title}")
        print(f"Author(s): {prettify_author}")
        print(f"Description: {description}")
        print(f"More Info: {link}\n")

    except Exception as e:
        print(f"Error fetching data for genre '{selected_genre}': {e}")

# Example usage
mood_input = input("Enter your mood from the list (e.g., Happy / Excited): ").strip()
recommend_book_by_mood(mood_input)