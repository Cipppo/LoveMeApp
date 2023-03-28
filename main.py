from random import random
from glob import glob



def retrieveToken(filename):
    token = open(filename, 'r').read()
    return token


token = retrieveToken("token.txt")

updater = Updater(token)