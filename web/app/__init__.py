# COMP90055 Computing Project, Semester 1 2016
# Author: Huabin Liu (ID. 658274)

from flask import Flask

app = Flask(__name__)
from app import views
