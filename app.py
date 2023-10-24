from flask import Flask, render_template, request, flash
import pandas as pd
import plotly.express as px
from io import BytesIO
from flask_wtf import FlaskForm
from wtforms import SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_EXTENSIONS'] = ['.csv']

class UploadForm(FlaskForm):
    submit = SubmitField('Upload CSV and Generate Pivot Chart')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    plot_div = ""

    if form.validate_on_submit():
        uploaded_file = request.files['file']

        if uploaded_file.filename != '':
            file_ext = os.path.splitext(uploaded_file.filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                flash('Invalid file type!')
                return redirect(request.url)

            df = pd.read_csv(BytesIO(uploaded_file.read()))

            # Example: Pivot table with sum of 'value' column, indexed by 'date' and columns as 'category'
            pivot_df = df.pivot_table(values='value', index='date', columns='category', aggfunc='sum')

            fig = px.line(pivot_df, x=pivot_df.index, y=pivot_df.columns)
            plot_div = fig.to_html(full_html=False)

    return render_template('index.html', form=form, plot_div=plot_div)

if __name__ == '__main__':
    app.run(debug=True)