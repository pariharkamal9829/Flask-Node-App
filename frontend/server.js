const express = require("express");
const axios = require("axios");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.get("/", (req, res) => {
    res.send(`
        <form action="/submit" method="post">
            <input type="text" name="name" placeholder="Item Name" required />
            <input type="text" name="description" placeholder="Item Description" required />
            <button type="submit">Submit</button>
        </form>
    `);
});

app.post("/submit", async (req, res) => {
    try {
        const response = await axios.post("http://backend:5000/submit", req.body);
        res.send("<h1>Data submitted successfully</h1>");
    } catch (error) {
        res.send(`<h1>Error: ${error.message}</h1>`);
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Frontend running on http://localhost:${PORT}`);
});
