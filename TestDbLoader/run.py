import entities_loading 
import overview_loading
import ministerial_load
import donation_loading
entities_loading.full_load_entities()
overview_loading.full_load_overview()
ministerial_load.create_db()
ministerial_load.load_meetings()
#Run for all - Only have Andrew Hoggard but can write a function to run for all
ministerial_load.read_meeting_file("ANDREW_HOGGARD", "APROCT24")
donation_loading.create_donation_db_and_tables()