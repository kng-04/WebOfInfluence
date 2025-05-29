import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage'; 
import App from './App.jsx'; 
import CandidateOverview from './CandidateOverview.jsx';
import MeetingsSearch from './MeetingsSearch.jsx';
import PersonProfile from './PersonProfile.jsx';

createRoot(document.getElementById('root')).render(
  <Router>
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/candidate-overview" element={<CandidateOverview />} />
      <Route path="/meetings" element={<MeetingsSearch />} />
      <Route path="/person/:firstName/:lastName" element={<PersonProfile />} />
    </Routes>
  </Router>
);
     
        
          
