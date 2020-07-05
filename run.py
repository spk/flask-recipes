#!/usr/bin/env python
from app import create_app

App = create_app()

if __name__ == "__main__":
    App.run()
