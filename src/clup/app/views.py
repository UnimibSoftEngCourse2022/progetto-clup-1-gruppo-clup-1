from app import app
from flask import render_template
from src.clup.basic_store_provider import BasicStoreProvider

@app.route('/')
def home():
    bsp = BasicStoreProvider()
    bsp.add_store('Esselunga')
    bsp.set_queue('Esselunga', ['cliente1', 'cliente2'])
    return render_template('home.html', bsp=bsp)


