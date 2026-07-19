const API = "http://127.0.0.1:5000";

const form = document.getElementById("tripForm");
const table = document.getElementById("tripTable");

const submitButton = form.querySelector("button");

let editingTripId = null;

/* ---------------- Load Trips ---------------- */

async function loadTrips() {

    try {

        const response = await fetch(`${API}/trips`);

        if (!response.ok) {
            throw new Error("Unable to load trips");
        }

        const trips = await response.json();

        table.innerHTML = "";

        trips.forEach((trip) => {

            table.innerHTML += `

            <tr>

                <td>${trip.destination}</td>

                <td>${trip.country}</td>

                <td>${trip.travel_type}</td>

                <td>₹${trip.estimated_budget}</td>

                <td>${trip.status}</td>

                <td>${trip.rating ?? "-"}</td>

                <td>

                    <button
                        type="button"
                        class="action-btn edit-btn"
                        onclick="editTrip(${trip.id})"
                    >
                        <i class="fa-solid fa-pen"></i>
                    </button>

                    <button
                        type="button"
                        class="action-btn delete-btn"
                        onclick="deleteTrip(${trip.id})"
                    >
                        <i class="fa-solid fa-trash"></i>
                    </button>

                </td>

            </tr>

            `;

        });

    }

    catch (error) {

        console.error(error);
        alert("Unable to load trips.");

    }

}

/* ---------------- Create / Update Trip ---------------- */

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const body = {

        destination:
            document.getElementById("destination").value,

        country:
            document.getElementById("country").value,

        travel_type:
            document.getElementById("travelType").value,

        estimated_budget:
            Number(document.getElementById("budget").value),

        status:
            document.getElementById("status").value,

        rating:
            document.getElementById("rating").value
                ? Number(document.getElementById("rating").value)
                : null,

        experience_notes:
            document.getElementById("notes").value || null

    };

    let response;

    try {

        if (editingTripId === null) {

            response = await fetch(`${API}/trips`, {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify(body)

            });

        }

        else {

            response = await fetch(`${API}/trips/${editingTripId}`, {

                method: "PUT",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify(body)

            });

        }

        if (!response.ok) {

    throw new Error("Save failed");

}

if (editingTripId === null) {

    alert("Trip created successfully.");

}

else {

    alert("Trip updated successfully.");

}

form.reset();

editingTripId = null;

submitButton.innerHTML = `
    <i class="fa-solid fa-plus"></i>
    Add Trip
`;

 await loadTrips();

    }

    catch (error) {

        console.error(error);

        alert("Unable to save trip.");

    }

});

/* ---------------- Delete Trip ---------------- */

async function deleteTrip(id) {

    if (!confirm("Delete this trip?")) return;

    try {

        const response = await fetch(`${API}/trips/${id}`, {

            method: "DELETE"

        });

        if (!response.ok) {

    throw new Error("Delete failed");

}

alert("Trip deleted successfully.");

await loadTrips();

    }

    catch (error) {

        console.error(error);

        alert("Unable to delete trip.");

    }

}

/* ---------------- Edit Trip ---------------- */

async function editTrip(id) {

    try {

        const response = await fetch(`${API}/trips/${id}`);

        if (!response.ok) {

            throw new Error("Unable to load trip");

        }

        const trip = await response.json();

        editingTripId = id;

        document.getElementById("destination").value =
            trip.destination;

        document.getElementById("country").value =
            trip.country;

        document.getElementById("travelType").value =
            trip.travel_type;

        document.getElementById("budget").value =
            trip.estimated_budget;

        document.getElementById("status").value =
            trip.status;

        document.getElementById("rating").value =
            trip.rating ?? "";

        document.getElementById("notes").value =
            trip.experience_notes ?? "";

        submitButton.innerHTML = `
            <i class="fa-solid fa-floppy-disk"></i>
            Update Trip
        `;

    }

    catch (error) {

        console.error(error);

        alert("Unable to load trip.");

    }

}

/* ---------------- Start ---------------- */

loadTrips();