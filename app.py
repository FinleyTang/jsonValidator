
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
import json


app = Flask(__name__)
app.secret_key = 'secret'

class JSONForm(FlaskForm):
    json_data = StringField('JSON Data', validators=[InputRequired()], render_kw={'size': 50, 'maxlength': 1000})
    submit = SubmitField('Validate')

def validate_json(data):
    try:
        json.dumps(data)
    except ValueError as e:
        return {'success': False, 'error': str(e)}
    return {'success': True}


@app.route('/', methods=['GET', 'POST'])
def index():
    form = JSONForm()
    if form.validate_on_submit():
        try:
            data = json.loads(form.json_data.data)
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid JSON'})
        result = validate_json(data)
        return jsonify(result)
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
