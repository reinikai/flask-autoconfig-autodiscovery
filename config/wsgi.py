import sys
sys.path.append('..')

from autoconfig import app as application

# Simply using "app" as name will not work in import.

if __name__ == "__main__":
    application.run()
