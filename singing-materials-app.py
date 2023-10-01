from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

bootstrap= Bootstrap(app)

class MPIDForm(FlaskForm):
    mp_id = StringField('What is the Materials Project ID?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def index():
    mp_id = None
    form = MPIDForm()
    if form.validate_on_submit():
        mp_id = form.mp_id.data
        form.mp_id.data = ''
        return redirect(url_for('audio', mp_id=mp_id))
    return render_template('index.html',form=form, mp_id=mp_id)


@app.route('/success/<int:result_id>')
def success(result_id):
     # replace this with a query from whatever database you're using
     result = get_result_from_database(result_id)
     # access the result in the tempalte, for example {{ result.name }}
     return render_template('success.html', result=result)


@app.route('/audio/<int:mp_id>')
def audio(mp_id):

    with sd.Stream(callback=print_sound):
        duration = 20
        sd.sleep(duration * 1000)

    return render_template('audio.html', mp_id=mp_id)

if __name__ == '__main__':
    app.run(debug=True)