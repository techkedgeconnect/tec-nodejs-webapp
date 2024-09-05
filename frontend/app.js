const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();

// Hardcoded values for port and backend service URL
const port = 3000;
const backendServiceUrl = 'http://backend:5000';

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Route to handle API requests
app.get('/api/message', async (req, res) => {
    try {
        const response = await axios.get(backendServiceUrl);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ message: 'Failed to fetch message from backend.' });
    }
});

// Serve the main HTML file on the root route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start the server
app.listen(port, () => {
    console.log(`Frontend is running on http://localhost:${port}`);
});
