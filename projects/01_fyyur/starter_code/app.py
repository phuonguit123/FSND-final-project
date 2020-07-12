#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
# DONE: added in the config file 
import logging
logging.basicConfig(level=logging.DEBUG)

from flask_migrate import Migrate
migrate = Migrate(app, db, compare_type=True) # this is specifically for falsk app and SQlAlchemy database 



#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500), default = "Not currently seeking talent")

    shows = db.relationship('Show', backref='Venue', lazy=True) # no shows needed on creation 
    
    # custom output/print 
    # def __dict__(self):

        # return {
            # 'id':self.id,
            # 'name' :self.name,
            # 'address': self.address,
            # 'city' :self.city,
            # 'state' :self.state,
            # 'phone' :self.phone,
            # 'genres' : self.genres,
            # 'website' :self.website,
            # 'facebook_link':self.facebook_link,
            # 'image-link' :self.image_link,
            # 'seeking_talent' :self.seeking_talent,
            # 'seeking_description' :self.seeking_description,
        # } 
        
        
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    
    genres = db.Column(db.ARRAY(db.String)) # this should be an array of string 
    
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500), default=' ')
    shows = db.relationship('Show', backref='Artist', lazy=True)
    
    # def __dict__(self):
        # return {
            # 'id' :self.id,
            # 'name' :self.name,
            # 'city' :self.city,
            # 'state': self.state,
            # 'phone' :self.phone,
            # 'genres' : self.genres,
            # 'website' :self.website,
            # 'facebook_link':self.facebook_link,
            # 'image-link' :self.image_link,
            # 'seeking_venue' :self.seeking_venue,
            # 'seeking_description' :self.seeking_description,
            
        # }


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    # child table, has foreign keys 
    __tablename__ = 'Show'
    
    id = db.Column(db.Integer, primary_key = True )
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable = False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable = False)
    start_time = db.Column(db.DateTime, nullable = False)
    # artist image_link
    # artist name 
    # venue name
    
    def __repr__(self):
        return '<Show: {} at {}>'.format(self.artist_id, self.venue_id)



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    
    return render_template('pages/home.html')


#----------------------------------------------------------------------------#
#  Venues
#----------------------------------------------------------------------------#
@app.route('/venues')
def venues(): # missing the #shows calculation, 

    """
    
    return:
        result: a list of dictionary, city, state, venues(a list of dictionary, id, name, num of upcoming shows )
    """
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    
    # data=[{
    # "city": "San Francisco",
    # "state": "CA",
    # "venues": [{
        # "id": 1,
        # "name": "The Musical Hop",
        # "num_upcoming_shows": 0,
    # }, {
        # "id": 3,
        # "name": "Park Square Live Music & Coffee",
        # "num_upcoming_shows": 1,
    # }]
    # }, {
    # "city": "New York",
    # "state": "NY",
    # "venues": [{
        # "id": 2,
        # "name": "The Dueling Pianos Bar",
        # "num_upcoming_shows": 0,
    # }]
    # }]
    
    # get data from database 
    data = Venue.query.all()
    result = {} # use city+state as keys, to construct the venues list 
    
    for v in data: 
        logging.info(v)
        # print(type(v))
        
        location = v.city.strip() + ' ' +v.state.strip()
        if not location in result:
            result[location] = {
                'city': v.city,
                'state': v.state,
                'venues': [],
                }
                
        result[location]['venues'].append({
                'id': v.id,
                'name': v.name,
                'num_upcoming_shows': 'not implemented',
                },)

    return render_template('pages/venues.html', areas=list(result.values()))


@app.route('/venues/search', methods=['POST'])
def search_venues():
    """
        partial string search for venues, case insensitive
        
    """

    target = request.form['search_term'].lower()
    search = f"%{target}%"
    data = Venue.query.filter(Venue.name.ilike(search)).all() # ilike is case insensitive
    # eg. lower(a) LIKE lower(other)
    
    result = []
    for v in data:
        result.append({
            'id': v.id,
            'name': v.name,
            'num_upcoming_shows': 'not implemented'
            })
    response = {
        'count': len(result),
        'data': result
        }
 
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    """a venue detail page, use venue_id 
    """
    result = []
    venue = Venue.query.get(venue_id)
    if venue:
        logging.info(f"Venue {venue_id} found.")
        data = venue.__dict__
        
        # calculate the upcoming and past 
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        shows = Show.query.options(db.joinedload(Show.Venue)).filter(Show.venue_id == venue_id)
        
        new_shows = shows.filter(Show.start_time > current_time).all()
        new_shows_list = []
        for s in new_shows:
            cur = {}
            cur['artist_id'] = s.artist_id
            cur['artist_name'] = s.Artist.name
            cur['artist_image_link'] = s.Artist.image_link
            cur['start_time'] = str(s.start_time)
            new_shows_list += cur,
        data['upcoming_shows']  = new_shows_list
        data['upcoming_shows_count'] = len(new_shows_list)
        
        old_shows = shows.filter(Show.start_time <= current_time).all()
        old_shows_list = []
        for s in old_shows:
            cur = {}
            cur['artist_id'] = s.artist_id
            cur['artist_name'] = s.Artist.name
            cur['artist_image_link'] = s.Artist.image_link
            cur['start_time'] = str(s.start_time)
            old_shows_list += cur,
        data['past_shows']  = old_shows_list
        data['past_shows_count'] = len(old_shows_list)    
    
    else: # no artist found
        logging.error(f"Venue {venue_id} NOT found.")
        abort(404)

    return render_template('pages/show_venue.html', venue=data)


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    
    # this form is not quite right 
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    """create a venue using form, and save in database """
    try:
        data = request.form   

        # check seeking_talent
        if not 'seeking_talent' in data:
            seeking_talent = False
        elif data['seeking_talent'] == 'y':
            seeking_talent = True 
        
        
        venue = Venue(
                    name = data['name'],     
                    city = data['city'],
                    state = data['state'],
                    address = data['address'],
                    phone = data['phone'],
                    genres = data.getlist('genres'),
                    facebook_link = data['facebook_link'],
                    image_link = data['image_link'],
                    website = data['website'], 
                    seeking_talent = seeking_talent, 
                    seeking_description = data['seeking_description'],
                    )
        # logging.info( 'seeking_talent' in data )
        
        db.session.add(venue)
        db.session.commit()
        
        logging.info('Venue ' + data['name'] + ' was successfully listed!')
        flash('Venue ' + data['name'] + ' was successfully listed!')
        
    except Exception as e:
        logging.error(f"error is :{e}")
        # logging.error(sys.exc_info)
        db.session.rollback()
        flash('An error occurred. Venue ' + data['name'] + ' could not be listed.')
        
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    
    try: 
        # venue = Venue.query.get(venue_id)
        venue = Venue.query.filter_by(id = venue_id).first()
        db.session.delete(venue)
        db.session.commit()

        logging.info(f"venue {venue_id} is successfully deleted")
        flash('An error occurred. Venue ' + data['name'] + ' could not be deleted.')
    except: 
    
        db.session.rollback()
        flash('An error occurred. Venue ' + data['name'] + ' could not be deleted.')
    finally: 
        db.session.close()
    
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None

# UPDATE venue 
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))




#----------------------------------------------------------------------------#
#  Artists
#----------------------------------------------------------------------------#
@app.route('/artists')
def artists():
    """display a list of artists """
    
    data = Artist.query.all()
    result = [] 
    for a in data:
        result.append({
            'id': a.id,
            'name': a.name
            })
    return render_template('pages/artists.html', artists=result)


@app.route('/artists/search', methods=['POST'])
def search_artists():    
    # search for an artist by name
    target = request.form['search_term'].lower()
    search = f"%{target}%"
    data = Artist.query.filter(Artist.name.ilike(search)).all() # ilike is case insensitive
    
    result = []
    for a in data:
        logging.info(a.name)
        result.append({
            'id': a.id,
            'name': a.name,
            'num_upcoming_shows': 'not implemented'
            })
    response = {
        'count': len(result),
        'data': result
        }
    # return jsonify(response)
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # show artist detail page by artist id 
    # include the upcoming shows and past shows 
    result = []
    artist = Artist.query.get(artist_id)
    if artist:
        logging.info(f"Artist {artist_id} found.")
        data = artist.__dict__
        
        # calculate the upcoming and past 
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        shows = Show.query.options(db.joinedload(Show.Artist)).filter(Show.artist_id == artist_id)
        
        new_shows = shows.filter(Show.start_time > current_time).all()
        new_shows_list = []
        for s in new_shows:
            cur = {}
            cur['venue_id'] = s.venue_id
            cur['venue_name'] = s.Venue.name
            cur['venue_image_link'] = s.Venue.image_link
            cur['start_time'] = str(s.start_time)
            new_shows_list += cur,
        data['upcoming_shows']  = new_shows_list
        data['upcoming_shows_count'] = len(new_shows_list)
        
        old_shows = shows.filter(Show.start_time <= current_time).all()
        old_shows_list = []
        for s in old_shows:
            cur = {}
            cur['venue_id'] = s.venue_id
            cur['venue_name'] = s.Venue.name
            cur['venue_image_link'] = s.Venue.image_link
            cur['start_time'] = str(s.start_time)
            old_shows_list += cur,
        data['past_shows']  = old_shows_list
        data['past_shows_count'] = len(old_shows_list)    
    
    else: # no artist found
        logging.error(f"Artist {artist_id} NOT found.")
        abort(404)
    
    
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    # get method, pre-populate the page with content 
    
    artist = Artist.query.get(artist_id)# .first()
    form = ArtistForm(request.form) # this is on the front page 
    
    if artist:
        logging.info(f"artist {artist_id} found.")
        # logging.info(artist)
        # logging.info(artist.__dict__)
        data = artist.__dict__ 
        

        form.name.data = data['name']
        form.city.data = data['city']
        form.state.data = data['state']
        
        form.genres.data = data['genres']
        form.phone.data = data['phone']
        form.website.data = data['website']
        form.facebook_link.data = data['facebook_link']
        form.image_link.data = data['image_link']
        
        form.seeking_description = data['seeking_description']
        form.seeking_venue = data['seeking_venue']
    else: 
        logging.info(f"artist {artist_id} not found.")
        
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    
    artist = Artist.query.get(artist_id)# .first()
    form = ArtistForm(request.form) # this is on the front page
    
    if artist: 
        if form.validate():
            # check seeking_talent
            if not 'seeking_talent' in data:
                seeking_talent = False
            elif data['seeking_talent'] == 'y':
                seeking_talent = True 
                
            artist['name'] = request.form['name']
            artist['city'] = request.form['city']
            artist['state'] = request.form['state']
            artist['phone'] = request.form['phone']
            artist['genres'] = request.form['genres']
            artist['facebook_link'] = request.form['facebook_link']
            artist['image_link'] = request.form['image_link']
            artist['website'] = request.form['website']
            artist['seeking_venue'] = request.form['seeking_venue']
            artist['seeking_description'] = request.form['seeking_description']
            
            # update using the new form information 
            try: 
                db.session.commit()
                logging.info(f"artist {artist['name']} updated.")
                
            except Error: 
                logging.error(Error)
                logging.error(form.errors)
                db.session.rollback()
                abort(404)
                
            finally: 
                db.session.close()
            
            
    # problem: show artist page NOT IMPLEMENTED
    return jsonify(artist.__dict__)
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    
    try:
        data = request.form   
        # check seeking_venue
        if not 'seeking_venue' in data:
            seeking_venue = False
        elif data['seeking_venue'] == 'y':
            seeking_venue = True 
        
        for d in data:
            logging.info(d)
            
        artist = Artist(
                    name = data['name'],     
                    city = data['city'],
                    state = data['state'],
                    phone = data['phone'],
                    genres = data['genres'],
                    facebook_link = data['facebook_link'],
                    image_link = data['image_link'],
                    website = data['website'], 
                    seeking_venue = seeking_venue, 
                    seeking_description = data['seeking_description'],
                    )
        
        db.session.add(artist)
        db.session.commit()
        
        logging.info('Artist ' + data['name'] + ' was successfully listed!')
        flash('Artist ' + data['name']+ ' was successfully listed!')
          
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        flash('An error occurred. Artist ' + data['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')



#----------------------------------------------------------------------------#
#  Shows
#----------------------------------------------------------------------------#
@app.route('/shows')
def shows():
    # displays list of shows at /shows
    shows = Show.query.options(
            db.joinedload(Show.Venue), 
            db.joinedload(Show.Artist),
        ).all()
    
    result = []
    for s in shows:
        cur = {}
        cur['venue_id'] = s.venue_id
        cur['venue_name'] = s.Venue.name
        cur['artist_id'] = s.artist_id
        cur['artist_name'] = s.Artist.name
        cur['artist_image_link'] = s.Artist.image_link
        cur['start_time'] = str(s.start_time)
        
        result.append(cur)
        # logging.info(cur)
    # return jsonify(result)
    return render_template('pages/shows.html', shows=result)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try: 
        show = Show(
            venue_id = request.form['venue_id'],
            artist_id = request.form['artist_id'],
            start_time = request.form['start_time'],
            )
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
        
    except:
        logging.error(sys.exc_info())
        db.session.rollback()
        flash('An error occured. Show could not be listed.')
    finally:
        db.session.close()
        
    return render_template('pages/home.html')





#----------------------------------------------------------------------------#
# Error Code Handler
#----------------------------------------------------------------------------#
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
