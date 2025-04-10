const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

// Database Connection
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'ProductSalesDB'
});

db.connect(err => {
    if (err) throw err;
    console.log('Connected to MySQL Database');
});

// Get all products
app.get('/products', (req, res) => {
    db.query('SELECT * FROM Products', (err, results) => {
        if (err) return res.status(500).send(err);
        res.json(results);
    });
});

// Add a new product
app.post('/products', (req, res) => {
    const { name, sales, price } = req.body;
    db.query('INSERT INTO Products (name, sales, price) VALUES (?, ?, ?)', [name, sales, price], 
    (err, result) => {
        if (err) return res.status(500).send(err);
        res.json({ message: 'Product added!', productId: result.insertId });
    });
});

// Delete a product
app.delete('/products/:id', (req, res) => {
    db.query('DELETE FROM Products WHERE product_id = ?', [req.params.id], (err, result) => {
        if (err) return res.status(500).send(err);
        res.json({ message: 'Product deleted!' });
    });
});

// Start server
app.listen(3000, () => console.log('Server running on port 3000'));
