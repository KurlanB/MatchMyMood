from flask import render_template, request, redirect, session, url_for
from app import app
from backend import recommend_book_by_mood

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/page2', methods=['GET'])
def page2():
    mood = request.args.get('mood')
    
    if mood:
        session['mood'] = mood
        book_details = recommend_book_by_mood(mood)
        
        return render_template('page2.html')
    else:
        return redirect(url_for('home'))