from flask import Flask, render_template, request, redirect
import pandas as pd
import json

app = Flask(__name__)
df = None

@app.route('/', methods=['GET', 'POST'])
def index():
    error=None
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename.endswith('csv'):
            global df
            df = pd.read_csv(uploaded_file)
            return redirect('/dashboard')
        else:
            error = "Only CSV files are allowed. Please upload a valid CSV file."
    return render_template('index.html', error= error)

@app.route('/dashboard', methods=['GET','POST'])
def form():
    global df
    print("Form data:", request.form)
    if request.method == 'POST':
        action = request.form['action']
        if action == 'display_charts':
            return redirect('/charts')
        if action == 'display_dataframe':
            return render_template('dashboard.html', df=df.to_html() if df is not None else None)
        if action == 'calculate_correlation':
            return redirect('/correlation')
    return render_template('dashboard.html', df = None)


@app.route('/charts', methods =['GET', 'POST'])
def charts():
    global df
    print("columns:",df.columns.tolist())
    if request.method == 'POST':
        x_axis_column = request.form['x_axis_column']
        y_axis_column = request.form['y_axis_column']
        chart_type = request.form['chart_type']
        print(request.form['x_axis_column'])

        labels = df[x_axis_column].tolist()
        values = df[y_axis_column].tolist()
        
        if chart_type == 'line_chart':
            return render_template('line_chart.html', labels=json.dumps(labels), values=json.dumps(values), df=df.to_html() if df is not None else None)
        elif chart_type == 'bar_chart':
            return render_template('bar_chart.html', labels=json.dumps(labels), values=json.dumps(values), df=df.to_html() if df is not None else None)
        elif chart_type == 'pie_chart':
            return render_template('pie_chart.html', labels=json.dumps(labels), values=json.dumps(values), df=df.to_html() if df is not None else None)
    return render_template('charts.html', columns=df.columns.to_list())

@app.route('/correlation', methods =['GET','POST'])
def correlation():
    global df
    corr = None
    if request.method == 'POST':
        x_axis_column = request.form['x_axis_column']
        y_axis_column = request.form['y_axis_column']
        df[x_axis_column] = pd.to_numeric(df[x_axis_column], errors='coerce')
        df[y_axis_column] = pd.to_numeric(df[y_axis_column], errors='coerce')
        clean_data = df.dropna(subset=[x_axis_column, y_axis_column], inplace=False)
        correlation = clean_data[x_axis_column].corr(clean_data[y_axis_column])

        corr = f"The correlation between {x_axis_column} and {y_axis_column} is: {correlation}"
    else:
        x_axis_column = None
        y_axis_column = None # setting these so that the selected columns can be displayed in the same template if they were previously selected
    return render_template('correlation.html', columns = df.columns.to_list(), x_axis_column=x_axis_column, y_axis_column=y_axis_column, corr = corr)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
