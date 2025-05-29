## Web Of Influence Research Project
**Current Progress** <br>
The code currently is able to load the Overviews of Candidate Donation for election in '11, '14, '17 and '23 from the data provided to us, has an API defined for local querying of the database and a functional React-based front end that allows for searching and filtering of the database. There is also the ability to export the results of the search to a _.csv_ file.


#### How to run the code
1. Update the user and password access in ```loader.py```
2. Change into the directory _TestDbLoader_
3. In _entities_loading.py_ run ```full_load_entities()```
4. In _overview_loading.py_ run ```full_load_overview()```
5. Run _database_api.py_
6. In a new terminal, go back to the main directory, change into the directory _demo-cand_, then use the command **npm run dev**
