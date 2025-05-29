import React, { useState } from 'react';
import Output from './Output.jsx';
import { useNavigate } from 'react-router-dom';
import BarChart from './BarChart.jsx';

function CandidateOverview() {
    const [searchQuery, setSearchQuery] = useState({
        firstName: '',
        lastName: '',
        party: '',
        electorate: '',
    });
    const [selectedYears, setSelectedYears] = useState({
        2023: true,
        2017: false,
        2014: false,
        2011: false
    });
    const [results, setResults] = useState([]);
    const [processsedResults, setProcessedResults] = useState( []);

    const handleSearchChange = (event) => {
        const { name, value } = event.target;
        setSearchQuery(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleYearChange = (year) => {
        setSelectedYears(prevYears => ({
            ...prevYears,
            [year]: !prevYears[year]
        }));
    };

    const handleSearchSubmit = async () => {
        const activeYears = Object.keys(selectedYears).filter(year => selectedYears[year]);

        if (activeYears.length === 0) {
            setResults(['No results found']);
            return;
        }

        const hasCriteria =
            searchQuery.firstName ||
            searchQuery.lastName ||
            searchQuery.party ||
            searchQuery.electorate;

        if (!hasCriteria) {
            setResults(['No results found']);
            return;
        }

        let allResults = [];

        for (let year of activeYears) {
            try {
                const params = new URLSearchParams();
                if (searchQuery.firstName) params.append('first_name', searchQuery.firstName);
                if (searchQuery.lastName) params.append('last_name', searchQuery.lastName);
                if (searchQuery.party) params.append('party_name', searchQuery.party);
                if (searchQuery.electorate) params.append('electorate_name', searchQuery.electorate);

                const response = await fetch(
                    `http://127.0.0.1:5000/candidates/election-overview/${year}/search/combined?${params.toString()}`
                );

                if (response.ok) {
                    const data = await response.json();
                    console.log(data);
                    const resultsWithYear = data.map(item => ({
                        ...item,
                        election_year: year,
                    }));
                    allResults = [...allResults, ...resultsWithYear];
                }
            } catch (err) {
                console.error(`Error fetching data for ${year}:`, err);
            }
        }

        if (allResults.length === 0) {
            setResults(['No results found']);
        } else {
            setResults(allResults);
        }
    };

    const handleExportCSV = (processedResults) => {
        if (!processedResults || processedResults.length === 0) {
            alert('No data to export');
            return;
        }

        const defaultName = 'election_candidates';
        const filename = prompt('Enter a name for your CSV file:', defaultName) || defaultName;

        const finalFilename = filename.endsWith('.csv') ? filename : `${filename}.csv`;

        const headers = ['Name', 'Party', 'Electorate', 'Election Year', 'Total Expenses', 'Total Donations'];

        const csvRows = [
            headers.join(','),
            ...processedResults.map(row => [
                `${row.firstName} ${row.lastName}`,
                row.party,
                row.electorate,
                row.election_year,
                row.total_expenses,
                row.total_donations
            ].join(','))
        ];

        const csvContent = csvRows.join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', finalFilename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    // Processed results and setProcessedResults
    const processedResultsForChart = (results) => {
        if (results && results.length > 0 ) {
            const processedData = results.map(result => ({
                firstName: result.firstName || 'Unknown',
                lastName: result.lastName || 'Unknown', 
                total_donations: result.total_donations || 0,
            }));
            setProcessedResults(processedData);
        }
    };

    return (
        <div className="flex">
            <div className="w-64 p-4 bg-gray-100 h-screen">
                <h2 className="text-xl font-bold mb-4">Filter by Year</h2>
                {Object.keys(selectedYears).map(year => (
                    <div key={year} className="mb-2">
                        <label className="inline-flex items-center">
                            <input
                                type="checkbox"
                                checked={selectedYears[year]}
                                onChange={() => handleYearChange(year)}
                                className="form-checkbox"
                            />
                            <span className="ml-2">{year}</span>
                        </label>
                    </div>
                ))}

                <div className="mt-6">
                    <h3 className="text-lg font-semibold mb-2">Search Filters</h3>
                    <input
                        type="text"
                        name="firstName"
                        placeholder="First Name"
                        value={searchQuery.firstName}
                        onChange={handleSearchChange}
                        className="w-full mb-2 p-1 border"
                    />
                    <input
                        type="text"
                        name="lastName"
                        placeholder="Last Name"
                        value={searchQuery.lastName}
                        onChange={handleSearchChange}
                        className="w-full mb-2 p-1 border"
                    />
                    <input
                        type="text"
                        name="party"
                        placeholder="Party"
                        value={searchQuery.party}
                        onChange={handleSearchChange}
                        className="w-full mb-2 p-1 border"
                    />
                    <input
                        type="text"
                        name="electorate"
                        placeholder="Electorate"
                        value={searchQuery.electorate}
                        onChange={handleSearchChange}
                        className="w-full mb-2 p-1 border"
                    />
                </div>

                <div className="mt-4 space-y-2">
                    <button
                        onClick={handleSearchSubmit}
                        className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
                    >
                        Search
                    </button>
                </div>
            </div>

            <div className="flex-1 p-4">
                <h1
                    style={{
                        fontSize: '2rem',
                        fontWeight: 'bold',
                        marginBottom: '1rem',
                        textAlign: 'center',
                        color: '#ffffff',
                        borderBottom: '2px solid #ecf0f1',
                        paddingBottom: '0.5rem',
                        fontFamily: 'Arial, sans-serif',
                    }}
                >
                    Election Candidates Overiew Database Search & Filter
                </h1>

                {/* Pass processed results to BarChart */}
                {results && results.length > 0 && results[0] !== 'No results found' && (
                    <Output
                    results={results}
                    onExportCSV={handleExportCSV}
                />
                    
                )}

                {/* Pass processed results to BarChart */}

                <BarChart results={results} /> 
            </div>
        </div>
    );
}

export default CandidateOverview;