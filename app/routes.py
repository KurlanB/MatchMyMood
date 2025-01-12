from flask import render_template, request, redirect, session, url_for
from app import app
import json
from urllib.request import urlopen
import random

# Dictionary mapping moods to genres
mood_to_genre = {
    "Unmotivated/Lazy": [
        "Motivational", 
        "Self-help", 
        "Poetry", 
        "Short stories"
    ],
    "Stressed/Overwhelmed": [
        "Cozy fiction", 
        "Light romance", 
        "Mindfulness"
    ],
    "Sad/Heartbroken": [
        "Happy endings", 
        "Inspirational memoirs", 
    ],
    "Happy/Excited": [
        "Adventure", 
        "Comedies"
    ],
    "Curious/Intellectual": [
        "Science", 
        "History", 
        "Philosophy", 
        "Mystery", 
        "Thriller", 
    ],
    "Angry/Frustrated": [
        "Action-packed thrillers", 
        "Revenge stories", 
    ],
    "Bored/Restless": [
        "Graphic novels", 
    ],
    "Romantic/Dreamy": [
        "Romance novels", 
        "Fantasy romance", 
        "Poetry"
    ],
    "Inspired/Creative": [
        "Creativity", 
        "Art", 
        "Fantasy", 
        "Biographies"
    ],
    "Nostalgic/Reflective": [
        "Historical fiction", 
        "Memoirs"
    ]
}

def recommend_book_by_mood(mood):
    # Check if the mood exists
    if mood not in mood_to_genre:
        return None  # Return None if the mood is not valid

    # Select a random genre from the mood list
    selected_genre = random.choice(mood_to_genre[mood])

    try:
        api = "https://www.googleapis.com/books/v1/volumes?q=subject:"
        resp = urlopen(api + selected_genre.replace(" ", "+"))
        book_data = json.load(resp)
        

        if "items" not in book_data or not book_data["items"]:
            return None  # No books found

        # Select a random book
        random_index = random.randint(0, len(book_data["items"]) - 1)
        volume_info = book_data["items"][random_index]["volumeInfo"]

        return {
            "title": volume_info.get("title", "Unknown Title"),
            "author": ", ".join(volume_info.get("authors", ["Unknown Author"])),
            "description": volume_info.get("description", "No description available."),
            "link": volume_info.get("infoLink", "#"),
            "page_count": volume_info.get("pageCount", "Unknown"),
            "published_date": volume_info.get("publishedDate", "Unknown"),
            "cover_image": volume_info.get("imageLinks", {}).get("thumbnail", ""),
        }
    except Exception as e:
        print(f"Error fetching data for genre '{selected_genre}': {e}")
        return None  # Return None on error

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/page2', methods=['GET'])
def page2():
    mood = request.args.get('mood')
    
    if mood in mood_to_genre:  # Validate the mood
        session['mood'] = mood
        book_details = recommend_book_by_mood(mood)
        
        if book_details:  # Check if a valid book was recommended
            return render_template(
                'page2.html',
                title=book_details["title"],
                author=book_details["author"],
                description=book_details["description"],
                link=book_details["link"],
                count=book_details["page_count"],
                date=book_details["published_date"],
                cover=book_details["cover_image"]
            )
        else:
            return render_template('page2.html', error="No book recommendations available for this mood.")
    else:
        return redirect(url_for('index'))