from app import create_app
from app.db import *

app = create_app()

if __name__ == '__main__':
    app.run( debug=True )
#   with app.app_context():
#       check_password( "david", "foo".encode() )
#       print( (user := db.users.find_one( { "name": "david" } ) ) )

#       print( user["_id"] )
#       print( ObjectId( user["_id"] ) )
