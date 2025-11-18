const mongoose = require('mongoose');

mongoose.connect("mongodb://localhost:27017/jsgenesis_dealers", {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

// Review schema
const reviewSchema = new mongoose.Schema({
    dealerId: String,
    reviewer: String,
    rating: Number,
    review: String,
    sentiment: String
});

const Review = mongoose.model("Review", reviewSchema);

async function seed() {
    // Replace with YOUR dealer ID
    const dealerId = "691bb2611dcddfd8b26878b2";

    await Review.deleteMany({ dealerId: dealerId });

    await Review.insertMany([
        {
            dealerId: dealerId,
            reviewer: "John Doe",
            rating: 5,
            review: "Excellent service and friendly staff!",
            sentiment: "positive"
        },
        {
            dealerId: dealerId,
            reviewer: "Jane Smith",
            rating: 4,
            review: "Great prices and quick service!",
            sentiment: "positive"
        }
    ]);

    console.log("Reviews added for dealer:", dealerId);
    process.exit();
}

seed();
