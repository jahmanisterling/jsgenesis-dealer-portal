const mongoose = require('mongoose');

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

const Dealer = mongoose.model("Dealer", dealerSchema);

async function seed() {
    await Dealer.deleteMany({});

    await Dealer.insertMany([
        {
            name: "Sunrise Toyota",
            city: "Kansas City",
            state: "Kansas",
            details: "Family-owned Toyota dealership"
        },
        {
            name: "Metro Honda",
            city: "Wichita",
            state: "Kansas",
            details: "Certified Honda dealer with service center"
        },
        {
            name: "Ford Auto Plaza",
            city: "Denver",
            state: "Colorado",
            details: "Full Ford sales & service"
        },
        {
            name: "Jeep Adventure Motors",
            city: "Houston",
            state: "Texas",
            details: "Specializes in off-road Jeep customizations"
        }
    ]);

    console.log("Dealers inserted!");
    process.exit();
}

seed();
