MySQL helper for Python
========================================

A helper for working with mysql written in python, with
connection-pooling feature


Installation
------------

It is possible to install the tool with `pip`::

    pip install sc-mysqlhelper

Features
--------

* Connection pooling


Configuration
-------------

The script itself is currently configuration free.


Dependencies
------------

* PyMySQL
* DBUtils


Usage
-------
Sample usage::

    from mysqlhelper import MySQLHelper

    helper = MySQLHelper(host="localhost", port=3306, user="test", password="test", database="test")
    rs = helper.select_one(sql="select count(*) from users")
    print(rs[0])

Changes
-------

Version 0.1
    * Initial version

License
-------

The script is released under the MIT License.  The MIT License is registered
with and approved by the Open Source Initiative [1]_.

.. [1] https://opensource.org/licenses/MIT
