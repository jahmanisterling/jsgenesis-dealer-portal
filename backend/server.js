const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

mongoose.connect("mongodb://localhost:27017/jsgenesis_dealers", {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

// Dealer schema
const dealerSchema = new mongoose.Schema({
    name: String,
    city: String,
    state: String,
    details: String
});

// Review schema
const reviewSchema = new mongoose.Schema({
    dealerId: String,
    reviewer: String,
    rating: Number,
    review: String,
    sentiment: String
});

const Dealer = mongoose.model("Dealer", dealerSchema);
const Review = mongoose.model("Review", reviewSchema);

// GET all dealers
app.get('/dealers', async (req, res) => {
    const dealers = await Dealer.find();
    res.json(dealers);
});

// GET dealer details
app.get('/dealers/details', async (req, res) => {
    const dealers = await Dealer.find();
    res.json({ dealers });
});

// GET dealers by state
app.get('/dealers/state/:state', async (req, res) => {
    const dealers = await Dealer.find({ state: req.params.state });
    res.json(dealers);
});

// GET reviews for a dealer
app.get('/reviews/dealer/:id', async (req, res) => {
    const reviews = await Review.find({ dealerId: req.params.id });
    res.json(reviews);
});

// POST review
app.post('/reviews', async (req, res) => {
    const review = new Review(req.body);
    await review.save();
    res.json({ status: "ok" });
});

app.listen(3000, () => console.log("JSGenesis API running on port 3000"));
