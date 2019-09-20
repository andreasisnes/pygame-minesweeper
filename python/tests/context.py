from os.path import abspath, join, dirname
from sys import path

path.insert(0, abspath(join(dirname(__file__), '..')))
import app