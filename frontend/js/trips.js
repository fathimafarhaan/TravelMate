const API = "http://127.0.0.1:5000";

const form = document.getElementById("tripForm");
const table = document.getElementById("tripTable");

/* ---------------- Load Trips ---------------- */

async function loadTrips() {

    const response = await fetch(`${API}/trips`);

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
                    class="action-btn edit-btn"
                    onclick="editTrip(${trip.id})"
                >
                    Edit
                </button>

                <button
                    class="action-btn delete-btn"
                    onclick="deleteTrip(${trip.id})"
                >
                    Delete
                </button>

            </td>

        </tr>

        `;

    });

}

/* ---------------- Create Trip ---------------- */

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
            Number(document.getElementById("rating").value) || null,

        experience_notes:
            document.getElementById("notes").value

    };

    await fetch(`${API}/trips`, {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(body)

    });

    form.reset();

    loadTrips();

});

/* ---------------- Delete ---------------- */

async function deleteTrip(id) {

    if (!confirm("Delete this trip?")) return;

    await fetch(`${API}/trips/${id}`, {

        method: "DELETE"

    });

    loadTrips();

}

/* ---------------- Edit ---------------- */

async function editTrip(id) {

    const response = await fetch(`${API}/trips/${id}`);

    const trip = await response.json();

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
        trip.rating;

    document.getElementById("notes").value =
        trip.experience_notes;

    form.onsubmit = async (e) => {

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
                Number(document.getElementById("rating").value),

            experience_notes:
                document.getElementById("notes").value

        };

        await fetch(`${API}/trips/${id}`, {

            method: "PUT",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(body)

        });

        form.reset();

        form.onsubmit = null;

        location.reload();

    };

}

/* ---------------- Start ---------------- */

loadTrips();