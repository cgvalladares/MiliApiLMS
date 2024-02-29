import os
from flask import render_template
from . import index_bp

@index_bp.route('/')
def root():
    
    return render_template('index.html')
    #return 'index'
