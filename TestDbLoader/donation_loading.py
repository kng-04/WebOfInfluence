import mysql.connector
from mysql.connector.errors import InterfaceError
import loader as ld
import pandas 
import re
from datetime import datetime
import requests
import json 
import ministerial_load as ml

connection = mysql.connector.connect(
    host="localhost",
    user = "root",
    passwd = "Engr4892025"
)
mycursor = connection.cursor()

def create_donation_table(year):
    ld.use_db(mycursor, f"Donations_Individual")
    column_dict = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "date": "DATE",
        "amount": "INT",
        "MoneyOrGoodsServices": "VarChar(255)",
        "location": "VARCHAR(255)",
        "notes": "VARCHAR(255)",
        "original_id": "INT",
        "donor_id": "INT",
        "minister_donated": "INT"
    }
    
    foreign_keys = [  
        ("donor_id", "Entities", "Donors", "id"),
        ("minister_donated", "Entities", "People", "id")
    ]

    
    
    ld.create_tb(mycursor, f"Donations_Log_{year}", column_dict, foreign_keys)


def load_donation(date, amount, MoneyOrGoodsServices, location, notes, donor_id, minister_donated_id, year):
    ld.use_db(mycursor, f"Donations_Individual")
    ld.import_data(connection, mycursor, f"Donations_Log_{year}", ("date", "amount", "MoneyOrGoodsServices", "location", "notes", "donor_id", "minister_donated"), (date, amount, MoneyOrGoodsServices, location, notes, donor_id, minister_donated_id))
    connection.commit()

def convert_to_mysql_date(date_str):
    if not date_str or pandas.isna(date_str):
        return None
    try:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return None
    
import overview_loading as ol
def read_donations_table(year):
    ld.use_db(mycursor, "Donations_Individual")
    file = pandas.read_csv(f"donations_csv/{year}_donor_information_for_candidate.csv")
    for index, row in file.iterrows():
        date = convert_to_mysql_date(row['DateReceived'])
        amount = ol.clean_dollar_value(row['DonationAmount']) if pandas.notna(row['DonationAmount']) else 0
        MoneyOrGoodsServices = row['MoneyOrGoodsServices'] if pandas.notna(row['MoneyOrGoodsServices']) else ""
        notes = row['OtherDetail'] if pandas.notna(row['OtherDetail']) else ""
        location = " ".join(filter(None, [
            str(row['Address_Line1']) if not pandas.isna(row['Address_Line1']) else '',
            str(row['Address_Line2']) if not pandas.isna(row['Address_Line2']) else '',
            str(row['Address_City']) if not pandas.isna(row['Address_City']) else '',
            str(row['Address_Country']) if not pandas.isna(row['Address_Country']) else ''
        ]))        
        first_name = row['DonorName_First'] if pandas.notna(row['DonorName_First']) else ""
        last_name = row['DonorName_Last'] if pandas.notna(row['DonorName_Last']) else ""
        donor_name_first = str(first_name).strip() if first_name else ""
        donor_name_last = str(last_name).strip() if last_name else ""
        donor_id = check_donor_id(donor_name_first.upper(), donor_name_last.upper())
        minister_donated_id = row[f'_{year}CandidateDonations_Id'] if pandas.notna(row[f'_{year}CandidateDonations_Id']) else ""
        mycursor.execute(f"SELECT * FROM Overviews_Candidate_Donations_By_Year.{year}_Candidate_Donation_Overview WHERE original_id = {minister_donated_id}")
        result_id = mycursor.fetchone()
        if not result_id:
            continue
        mycursor.execute(f"SELECT * FROM Overviews_Candidate_Donations_By_Year.{year}_Candidate_Donation_Overview WHERE original_id = {minister_donated_id}")
        result = mycursor.fetchall()
        if not result:
            continue
        minister_id = result[0][0]
        load_donation(date, amount, MoneyOrGoodsServices, location, notes, donor_id, minister_id, year)
       

def read_donations_table_23():
    year = "2023"
    ld.use_db(mycursor, "Donations_Individual")
    file = pandas.read_csv(f"donations_csv/{year}_donor_information_for_candidate.csv")
    for index, row in file.iterrows():
        date = convert_to_mysql_date(row['DateReceived'])
        amount = ol.clean_dollar_value(row['DonationAmount']) if pandas.notna(row['DonationAmount']) else 0
        MoneyOrGoodsServices = row['MoneyOrGoodsServices'] if pandas.notna(row['MoneyOrGoodsServices']) else ""
        notes = row['OtherDetail'] if pandas.notna(row['OtherDetail']) else ""
        location = " ".join(filter(None, [
            str(row['Address_Line1']) if not pandas.isna(row['Address_Line1']) else '',
            str(row['Address_Line2']) if not pandas.isna(row['Address_Line2']) else '',
            str(row['Address_City']) if not pandas.isna(row['Address_City']) else '',
            str(row['Address_Country']) if not pandas.isna(row['Address_Country']) else ''
        ]))        
        first_name = row['DonorName_First'] if pandas.notna(row['DonorName_First']) else ""
        last_name = row['DonorName_Last'] if pandas.notna(row['DonorName_Last']) else ""
        donor_name_first = str(first_name).strip() if first_name else ""
        donor_name_last = str(last_name).strip() if last_name else ""
        donor_id = check_donor_id(donor_name_first.upper(), donor_name_last.upper())
        minister_donated_id = row[f'CandidateDonations2023Test_Id'] if pandas.notna(row[f'CandidateDonations2023Test_Id']) else ""
        mycursor.execute(f"SELECT * FROM Overviews_Candidate_Donations_By_Year.{year}_Candidate_Donation_Overview WHERE original_id = {minister_donated_id}")
        result = mycursor.fetchall()
        if not result:
            continue
        minister_id = result[0][0]
        load_donation(date, amount, MoneyOrGoodsServices, location, notes, donor_id, minister_id, year)
       
def check_donor_id(first_name, last_name):
    ld.use_db(mycursor, "Entities")
    donor_id = ld.get_id_match(mycursor, "Entities",  "Donors", {"first_name": first_name, "last_name": last_name})
    if donor_id:
        return donor_id
    else:
        ld.import_data(connection, mycursor, "Donors", ("first_name", "last_name"), (first_name, last_name))
        connection.commit()
        return (ld.check_tb(mycursor, "Donors ORDER BY id DESC LIMIT 1"))[0][0]

def create_db():
    ld.create_db(mycursor, "Ministerial_Meetings")
    connection.commit()

def create_db_2():
    ld.create_db(mycursor, "donations_individual")
    connection.commit()

def create_donation_db_and_tables():
    create_db()
    create_db_2()
    create_donation_table("2023")
    create_donation_table("2017")
    create_donation_table("2014")
    create_donation_table("2011")
    read_donations_table("2017")
    read_donations_table("2014")
    read_donations_table("2011")
    read_donations_table_23()


