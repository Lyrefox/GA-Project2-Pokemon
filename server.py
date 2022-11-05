from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)
@app.route('/')
def main():
    return render_template('index.html')







if __name__ == '__main__':
    # from dotenv import load_dot_env
    app.run(debug=True)
