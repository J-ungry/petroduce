'''
Python 3.9.12
Flask 2.2.3
'''

import init
app = init.create_app()

if __name__ == '__main__':
    app.run(debug=True)