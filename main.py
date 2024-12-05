from flask import Flask, send_from_directory, render_template, request

from src.weather_model import make_response


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "GET":
        return render_template('index.html', from_inf={"show_data": False}, to_inf={"show_data": False})

    elif request.method == 'POST':
        try:
            from_ = make_response(request.form.get('from'))
            to_ = make_response(request.form.get('to'))

            return render_template('index.html', from_inf=from_, to_inf=to_)

        except Exception as e:
            print(e)
            response = {'status': 'Данные недоступны', 'is_correct': False}
            return render_template('index.html', from_inf=response, to_inf=response)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
