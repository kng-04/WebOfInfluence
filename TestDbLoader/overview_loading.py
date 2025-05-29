import mysql.connector
from mysql.connector.errors import InterfaceError
import loader as ld
import pandas 
connection = mysql.connector.connect(
    host="localhost",
    user = "root",
    passwd = "Engr4892025"
)
mycursor = connection.cursor()
# Remove below if havent created
#ld.use_db(mycursor, "Overviews_Candidate_Donations_By_Year")

def clean_dollar_value(dollar_str):
    try:
        return float(dollar_str.replace("$", "").replace(",", "").strip())
    except ValueError:
        print(f"Invalid dollar value: {dollar_str}")


def create_election_year_candidates_table(table_name):
    column_dict = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "total_donations": "FLOAT",
        "total_expenses": "FLOAT",
        "people_id": "INT",
        "party_id": "INT",
        "electorate_id": "INT",
        "part_a": "FLOAT",
        "part_b": "FLOAT",
        "part_c": "FLOAT",
        "part_d": "FLOAT",
        "part_f": "FLOAT",
        "part_g": "FLOAT",
        "part_h": "FLOAT",
        "year": "VARCHAR(4)",
        "original_id": "INT"
    }
    
    foreign_keys = [
        ("people_id", "Entities", "People", "id"),
        ("party_id", "Entities", "Parties", "id"),
        ("electorate_id", "Entities", "Electorates", "id")
    ]
    
    ld.create_tb(mycursor, table_name, column_dict, foreign_keys)

def load_csv_candidate_donations_23(file_name, year):
    file = pandas.read_csv(file_name)
    for index, row in file.iterrows():
        if pandas.isna(row['Electorate']) or pandas.isna(row['Party']) or pandas.isna(row['CandidateName_First']) or pandas.isna(row['CandidateName_Last']):
            print(f"Skipping row {index} due to missing value.")
            continue
        party_id = ld.get_id_match(mycursor, "Entities",  "Parties", {"party_name": ld.map_party_names(row['Party'].upper())})
        person_id = ld.get_id_match(mycursor,  "Entities",  "People", {"first_name": (row['CandidateName_First']).upper(), "last_name": row['CandidateName_Last'].upper()})
        electorate_id = ld.get_id_match(mycursor, "Entities",  "Electorates", {"electorate_name": row['Electorate'].upper()})
        part_a = clean_dollar_value(row['TotalPartA'])
        part_b = clean_dollar_value(row['TotalPartB'])
        part_c = clean_dollar_value(row['TotalPartC'])
        part_d = clean_dollar_value(row['TotalPartD'])
        part_f = clean_dollar_value(row['TotalPartFCandidateOnlyExpenses'])
        part_g = clean_dollar_value(row['TotalPartGSharedExpenses'])
        part_h = clean_dollar_value(row['TotalPartH'])
        total_donations = clean_dollar_value(row['TotalDonationsACD'])
        total_expenses = clean_dollar_value(row['TotalExpensesFG'])
        original_id = row['CandidateDonations2023Test_Id']
        ld.import_data(connection, mycursor, f"{year}_Candidate_Donation_Overview", ["total_donations", "total_expenses", "people_id", "party_id", "electorate_id", "part_a", "part_b", "part_c", "part_d", "part_f", "part_g", "part_h", "year", "original_id"], (total_donations, total_expenses, person_id, party_id, electorate_id, part_a, part_b, part_c, part_d, part_f, part_g, part_h, year, original_id))

def load_csv_candidate_donations_17(file_name, year):
    file = pandas.read_csv(file_name)
    for index, row in file.iterrows():
        if pandas.isna(row['Electorate']) or pandas.isna(row['Party']) or pandas.isna(row['CandidateName_First']) or pandas.isna(row['CandidateName_Last']):
            print(f"Skipping row {index} due to missing value.")
            continue
        party_id = ld.get_id_match(mycursor, "Entities",  "Parties", {"party_name": ld.map_party_names(row['Party'].upper())})
        person_id = ld.get_id_match(mycursor,  "Entities",  "People", {"first_name": (row['CandidateName_First']).upper(), "last_name": row['CandidateName_Last'].upper()})
        electorate_id = ld.get_id_match(mycursor, "Entities",  "Electorates", {"electorate_name": row['Electorate'].upper()})
        part_a = clean_dollar_value(row['TotalPartA'])
        part_b = clean_dollar_value(row['TotalPartB'])
        part_c = clean_dollar_value(row['TotalPartC'])
        part_d = clean_dollar_value(row['TotalPartD'])
        part_f = clean_dollar_value(row['TotalPartFCandidateOnlyExpenses'])
        part_g = clean_dollar_value(row['TotalPartGSharedExpenses'])
        part_h = clean_dollar_value(row['TotalPartH'])
        total_donations = clean_dollar_value(row['TotalDonationsACD'])
        total_expenses = clean_dollar_value(row['TotalExpensesFG'])
        original_id = row['_2017CandidateDonations_Id']
        ld.import_data(connection, mycursor, f"{year}_Candidate_Donation_Overview", ["total_donations", "total_expenses", "people_id", "party_id", "electorate_id", "part_a", "part_b", "part_c", "part_d", "part_f", "part_g", "part_h", "year", "original_id"], (total_donations, total_expenses, person_id, party_id, electorate_id, part_a, part_b, part_c, part_d, part_f, part_g, part_h, year, original_id))


def load_csv_candidate_donations_14(file_name, year):
    file = pandas.read_csv(file_name)
    for index, row in file.iterrows():
        if pandas.isna(row['Electorate']) or pandas.isna(row['Party']) or pandas.isna(row['CandidateName_First']) or pandas.isna(row['CandidateName_Last']):
            print(f"Skipping row {index} due to missing value.")
            continue
        party_id = ld.get_id_match(mycursor, "Entities",  "Parties", {"party_name": ld.map_party_names(row['Party'].upper())})
        person_id = ld.get_id_match(mycursor,  "Entities",  "People", {"first_name": (row['CandidateName_First']).upper(), "last_name": row['CandidateName_Last'].upper()})
        electorate_id = ld.get_id_match(mycursor, "Entities",  "Electorates", {"electorate_name": row['Electorate'].upper()})
        part_a = clean_dollar_value(row['TotalPartA'])
        part_b = clean_dollar_value(row['TotalPartB'])
        part_c = clean_dollar_value(row['TotalPartC'])
        part_d = clean_dollar_value(row['TotalPartD'])
        total_donations = clean_dollar_value(row['TotalDonationsACD'])
        total_expenses = clean_dollar_value(row['TotalExpenses'])
        original_id = row['_2014CandidateDonations_Id']
        ld.import_data(connection, mycursor, f"{year}_Candidate_Donation_Overview", ["total_donations", "total_expenses", "people_id", "party_id", "electorate_id", "part_a", "part_b", "part_c", "part_d", "year", "original_id"], (total_donations, total_expenses, person_id, party_id, electorate_id, part_a, part_b, part_c, part_d, year, original_id))

def load_csv_candidate_donations_11(file_name, year):
    file = pandas.read_csv(file_name)
    for index, row in file.iterrows():
        if pandas.isna(row['Electorate']) or pandas.isna(row['Party']) or pandas.isna(row['CandidateName_First']) or pandas.isna(row['CandidateName_Last']):
            print(f"Skipping row {index} due to missing value.")
            continue
        party_id = ld.get_id_match(mycursor, "Entities",  "Parties", {"party_name": ld.map_party_names(row['Party'].upper())})
        person_id = ld.get_id_match(mycursor,  "Entities",  "People", {"first_name": (row['CandidateName_First']).upper(), "last_name": row['CandidateName_Last'].upper()})
        electorate_id = ld.get_id_match(mycursor, "Entities",  "Electorates", {"electorate_name": row['Electorate'].upper()})
        part_a = clean_dollar_value(row['TotalPartA'])
        part_b = clean_dollar_value(row['TotalPartB'])
        part_c = clean_dollar_value(row['TotalPartC'])
        part_d = clean_dollar_value(row['TotalPartD'])
        total_donations = clean_dollar_value(row['TotalDonationsACD'])
        total_expenses = clean_dollar_value(row['TotalCandidateExpensesPartsABCD'])
        original_id = row['_2011CandidateDonations_Id']   
        ld.import_data(connection, mycursor, f"{year}_Candidate_Donation_Overview", ["total_donations", "total_expenses", "people_id", "party_id", "electorate_id", "part_a", "part_b", "part_c", "part_d","year", "original_id"], (total_donations, total_expenses, person_id, party_id, electorate_id, part_a, part_b, part_c, part_d, year, original_id))

def create_db():
    ld.create_db(mycursor, "Overviews_Candidate_Donations_By_Year")
    connection.commit()
    
def full_load_overview():
    create_db()
    connection.commit()
    ld.use_db(mycursor, "Overviews_Candidate_Donations_By_Year")
    create_election_year_candidates_table("2023_Candidate_Donation_Overview")
    create_election_year_candidates_table("2017_Candidate_Donation_Overview")
    create_election_year_candidates_table("2014_Candidate_Donation_Overview")
    create_election_year_candidates_table("2011_Candidate_Donation_Overview")
    load_csv_candidate_donations_23("candidate_csv/2023_candidate_donations.csv", "2023")
    load_csv_candidate_donations_17("candidate_csv/2017_candidate_donations.csv", "2017")
    load_csv_candidate_donations_14("candidate_csv/2014_candidate_donations.csv", "2014")
    load_csv_candidate_donations_11("candidate_csv/2011_candidate_donations.csv", "2011")
    connection.commit()
