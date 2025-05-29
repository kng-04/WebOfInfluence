from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app) 

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Engr4892025",
    )
    return connection

@app.route('/candidates', methods=['GET'])
def get_candidates():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Entities.People")
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/party', methods=['GET'])
def get_parties():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Entities.Parties")
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/electorate', methods=['GET'])
def get_electorates():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Entities.Electorates")
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/donor/search-id', methods=['GET'])
def get_donor_by_id():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    donor_id = request.args.get('donor_id')
    query = """
        SELECT * FROM Entities.Donors
        WHERE id = %s
    """
    cursor.execute(query, (donor_id,))
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/party/search-id', methods=['GET'])
def get_parties_by_id():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    party_id = request.args.get('party_id')
    query = """
        SELECT * FROM Entities.Parties
        WHERE id = %s
    """
    cursor.execute(query, (party_id,))
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/electorate/search-id', methods=['GET'])
def get_electorates_by_id():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    electorate_id = request.args.get('electorate_id')
    query = """
        SELECT * FROM Entities.Electorates
        WHERE id = %s
    """
    cursor.execute(query, (electorate_id,))
    rows = cursor.fetchone()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)


@app.route('/candidates/search-id', methods=['GET'])
def get_candidate_by_id():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    people_id = request.args.get('people_id')
    query = """
        SELECT * FROM Entities.People
        WHERE id = %s 
    """
    cursor.execute(query, (people_id, ))
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)


@app.route('/party/search', methods=['GET'])
def get_parties_by_name():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    party_name = request.args.get('party_name')
    query = """
        SELECT * FROM Entities.Parties
        WHERE party_name = %s
    """
    cursor.execute(query, (party_name,))
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/electorate/search', methods=['GET'])
def get_electorates_by_name():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    party_name = request.args.get('electorate_name')
    query = """
        SELECT * FROM Entities.Electorates
        WHERE electorate_name = %s
    """
    cursor.execute(query, (party_name,))
    rows = cursor.fetchone()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)


@app.route('/candidates/search', methods=['GET'])
def get_candidate_by_name():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    query = "SELECT * FROM Entities.People WHERE"
    values = []
    if first_name and last_name:
        query += " first_name = %s AND last_name = %s"
        values.append(first_name)
        values.append(last_name)
    elif last_name:
        query+= " last_name = %s"
        values.append(last_name)
    elif first_name:
        query+= " first_name = %s"
        values.append(first_name)
    else:
        return jsonify({"error": "At least one parameter (first_name or last_name) is required"}), 400
    cursor.execute(query, values)
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/candidates/election-overview/<year>', methods=['GET'])
def get_candidates_by_election_23(year):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM Overviews_Candidate_Donations_By_Year.{year}_Candidate_Donation_Overview"
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/candidates/election-overview/<year>/search/electorate', methods=['GET'])
def get_candidates_by_electorate(year):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    electorate = request.args.get('electorate_name')
    cursor.execute("SELECT id FROM Entities.Electorates WHERE electorate_name = %s", (electorate,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Electorate not found"}), 404
    electorate_id = result['id']
    query = f"SELECT * FROM Overviews_Candidate_Donations_By_Year.{year}_Candidate_Donation_Overview WHERE electorate_id = %s"
    cursor.execute(query, (electorate_id,))
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/candidates/election-overview/<year>/search/party', methods=['GET'])
def get_candidates_by_party(year):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    party = request.args.get('party_name')
    cursor.execute("SELECT id FROM Entities.Parties WHERE party_name = %s", (party,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "party not found"}), 404
    party_id = result['id']
    query = f"SELECT * FROM Overviews_Candidate_Donations_By_Year.{year}_Candidate_Donation_Overview WHERE party_id = %s"
    cursor.execute(query, (party_id,))
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/candidates/election-overview/<year>/search/name', methods=['GET'])
def get_candidates_by_name(year):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    cursor.execute("SELECT id FROM Entities.People WHERE first_name = %s AND last_name = %s", (first_name, last_name, ))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Name not found "}), 404
    people_id = result['id']
    query = f"SELECT * FROM Overviews_Candidate_Donations_By_Year.{year}_Candidate_Donation_Overview WHERE people_id = %s"
    cursor.execute(query, (people_id,))
    rows = cursor.fetchall()
    if not rows:  
        return jsonify({"error": "not found"}), 404
    return jsonify(rows)

@app.route('/candidates/election-overview/<year>/search/combined', methods=['GET'])
def get_candidates_combined_search(year):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    party_name = request.args.get('party_name')
    electorate_name = request.args.get('electorate_name')
    
    query = f"""
        SELECT * FROM Overviews_Candidate_Donations_By_Year.{year}_Candidate_Donation_Overview overview
    """
    
    conditions = []
    params = []
    
    if first_name or last_name:
        name_conditions = []
        if first_name:
            name_conditions.append("first_name = %s")
            params.append(first_name)
        if last_name:
            name_conditions.append("last_name = %s")
            params.append(last_name)
            
        conditions.append(f"""
            overview.people_id IN (
                SELECT id FROM Entities.People 
                WHERE {' AND '.join(name_conditions)}
            )
        """)
    
    if party_name:
        conditions.append("""
            overview.party_id IN (
                SELECT id FROM Entities.Parties 
                WHERE party_name = %s
            )
        """)
        params.append(party_name)
    
    if electorate_name:
        conditions.append("""
            overview.electorate_id IN (
                SELECT id FROM Entities.Electorates 
                WHERE electorate_name = %s
            )
        """)
        params.append(electorate_name)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    try:
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        if not rows:
            return jsonify({"error": "No results found"}), 404
        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/donations/<year>', methods=['GET'])
def get_candidate_donations_list_by_year(year):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    query1 = "SELECT * FROM Entities.People where first_name = %s AND last_name = %s"
    cursor.execute(query1, (first_name, last_name))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Candidate not found"}), 404
    people_id = result['id']
    query2 = f"SELECT * FROM Donations_Individual.Donations_Log_{year} WHERE minister_donated = %s"
    cursor.execute(query2, (people_id,))
    rows = cursor.fetchall()
    return jsonify(rows)

from datetime import timedelta
def convert_timedelta(obj):
    """Convert timedelta objects to a string format."""
    if isinstance(obj, timedelta):
        return str(obj)  # Example output: "1:30:00"
    return obj

@app.route('/ministerial_diaries/search-cand', methods=['GET'])
def get_candidate_meetings():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    query1 = "SELECT * FROM Entities.People where first_name = %s AND last_name = %s"
    cursor.execute(query1, (first_name, last_name))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Candidate not found"}), 404
    people_id = result['id']
    query2 = f"SELECT * FROM Ministerial_Meetings.Meetings_Log WHERE minister_logged_id = %s"
    cursor.execute(query2, (people_id,))
    rows = cursor.fetchall()
    for row in rows:
        for key, value in row.items():
            row[key] = convert_timedelta(value)
    return jsonify(rows)

@app.route('/ministerial_diaries/search-cand-filter', methods=['GET'])
def search_ministerial_diaries():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not first_name or not last_name:
        return jsonify({"error": "Both first name and last name are required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Query to get the candidate by name
    query1 = "SELECT * FROM Entities.People WHERE first_name = %s AND last_name = %s"
    cursor.execute(query1, (first_name, last_name))
    result = cursor.fetchone()

    if not result:
        return jsonify({"error": "Candidate not found"}), 404

    people_id = result['id']

    # Start building the query for the meetings
    query2 = "SELECT * FROM Ministerial_Meetings.Meetings_Log WHERE minister_logged_id = %s"
    params = [people_id]

    if start_date and end_date:
        query2 += " AND (date BETWEEN %s AND %s)"
        params.extend([start_date, end_date])

    cursor.execute(query2, params)
    rows = cursor.fetchall()

    # Convert timedelta if necessary
    for row in rows:
        for key, value in row.items():
            row[key] = convert_timedelta(value)

    cursor.close()
    connection.close()

    if rows:
        return jsonify(rows), 200
    else:
        return jsonify({"error": "No meetings found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
