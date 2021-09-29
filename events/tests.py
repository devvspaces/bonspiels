# from django.test import TestCase

# # Create your tests here.


import traceback

try:
    raise TypeError("Oups!")
except Exception as err:
    try:
        raise TypeError("Again !?!")
    except:
        pass

    traceback.print_tb(err.__traceback__)