
import sys
sys.path.insert(0, '/opt/kayrad')
sys.path.insert(0, '/opt/kayrad/.venv/lib/python3.10/site-packages')

from app import create_app

application = create_app()

