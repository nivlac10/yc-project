#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: COFFEE
# date: 2021-03-02
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=False)