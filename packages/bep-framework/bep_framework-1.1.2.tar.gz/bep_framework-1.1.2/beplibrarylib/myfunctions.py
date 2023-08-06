import psycopg2
import json

from flask import Response
from dateutil.parser import parse


def error_response(message, code):
    """
    Sends a JSON response with the error message

    :return: Response object with error response
    """
    return create_response({'error': {'code': code, 'message': message}}, code)


def create_response(input_data, status_code=200):
    """
    Create a default response with the status code in JSON format.

    :param input_data: the data to return
    :param status_code: the status code of the response, by default 200
    :return: Response object with data
    """
    data = json.dumps(input_data, indent=4, sort_keys=True, default=str)
    return Response(data, status=status_code, mimetype='application/json')


def insert_into_database(g, query, data):
    """
    Insert new data into the database.

    :param g: global variable of flask microservices
    :param query: query to be used for inserting data
    :param data: the data to insert
    :return: nothing, only raise an error if connection fails
    """
    try:
        g.cursor.execute(query, data)
        g.connection.commit()
    except psycopg2.OperationalError as e:
        raise ConnectionError(e)


def query_database(g, query, one=False):
    """
    Execute a given query that has no input parameters.

    :param g: global variable of flask microservices
    :param query: the SQL query to be executed
    :param one: when True the database only returns one record, otherwise multiple
    :return: result of query in format that can be converted to JSON
    """
    try:
        g.cursor.execute(query)
    except psycopg2.OperationalError as e:
        raise ConnectionError(e)
    rv = [dict((g.cursor.description[idx][0], value)
               for idx, value in enumerate(row)) for row in g.cursor.fetchall()]
    return (rv[0] if rv else None) if one else rv


def query_database_with_parameters(g, query, params, one=False):
    """
    Query a given query with parameters and return value

    :param g: global variable of flask microservices
    :param query: the SQL query to be executed
    :param params: the parameters for the query
    :param one: when True the database only returns one record, otherwise multiple
    :return: result of query in format that can be converted to JSON
    """
    try:
        g.cursor.execute(query, params)
    except psycopg2.OperationalError as e:
        raise ConnectionError(e)
    rv = [dict((g.cursor.description[idx][0], value)
               for idx, value in enumerate(row)) for row in g.cursor.fetchall()]
    return (rv[0] if rv else None) if one else rv


def execute_query_return_id(g, query, params):
    """
    Execute a given query that with input parameters.

    :param query: the SQL query to be executed
    :param params: the parameters to use in the query
    :return: the id of the new row
    """
    try:
        g.cursor.execute(query, params)
        res = g.cursor.fetchall()
        g.connection.commit()
    except psycopg2.OperationalError as e:
        raise ConnectionError(e)
    return res[0][0]


def string_is_date(string):
    """
    Check if a given string is in date format by using a
    data parsing library.

    :param string: the string to check
    :return: True if the given string is a date else False
    """
    try:
        parse(string, fuzzy=True)
        return True
    except ValueError:
        return False
