import flask
from flask import Flask, render_template, request
from python_files.get_recommendation import get_recommendation,get_suggestions,recommended_anime_detail
from python_files.anime_info import get_anime_details
from python_files.reviews import get_reviews
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

@app.route("/")
@app.route("/home")
def home():
    suggestions = get_suggestions()
    return render_template('home.html',ans=1, suggestions=suggestions)

@app.route("/recommend", methods=["POST","GET"])
def recommend():
    suggestions = get_suggestions()

    if flask.request.method == 'POST':
        anime = request.form['anime']
    else:
        anime = flask.request.args.get('anime')

    if anime == None:
        return render_template('home.html', ans=0, suggestions=suggestions)


    rc = get_recommendation(anime)
    if rc==None:
        return render_template('home.html',ans=0,suggestions=suggestions)

    # selected anime data
    title, title_japanese, \
    type, source, \
    studio, \
    genre, episodes, \
    status, duration, \
    rating, score, \
    rank, synopsis, \
    timeline, image_url,anime_id ,cast_details,voice_staff_details = get_anime_details(anime)

    #recommend anime data
    recommended_animes =recommended_anime_detail(rc)
    #reviews
    reviews = get_reviews(anime_id)
    return render_template('recommend.html', \
                           title=title, \
                           title_japanese=title_japanese, \
                           type=type, \
                           source=source, \
                           studio=studio, \
                           genre=genre, \
                           status=status, \
                           duration=duration, \
                           rating=rating, \
                           score=score, \
                           rank=rank, \
                           synopsis=synopsis, \
                           timeline=timeline, \
                           image_url=image_url, \
                           cast_details=cast_details, \
                           voice_staff_details=voice_staff_details, \
                           reviews=reviews, \
                           recommended_animes=recommended_animes)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
