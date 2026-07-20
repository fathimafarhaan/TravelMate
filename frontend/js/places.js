const API = "http://127.0.0.1:5000";

const form = document.getElementById("placeForm");
const tripSelect = document.getElementById("tripSelect");
const placesTable = document.getElementById("placesTable");
const submitButton =
    form.querySelector('button[type="submit"]');

let editingPlaceId = null;

/* ---------------- Load Trips ---------------- */

async function loadTrips() {
  try {
    const response = await fetch(`${API}/trips`);

    if (!response.ok) {
      throw new Error("Unable to load trips");
    }

    const trips = await response.json();

    tripSelect.innerHTML = `<option disabled selected>Select Trip</option>`;

    trips.forEach((trip) => {
      tripSelect.innerHTML += `

                <option value="${trip.id}">
                    ${trip.destination}
                </option>

            `;
    });
  } catch (error) {
    console.error(error);

    alert("Unable to load trips.");
  }
}

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const tripId = tripSelect.value;

    const body = {

        place_name: document.getElementById("placeName").value,

        visited: Number(document.getElementById("visited").value)

    };

    try {

        let response;

        if (editingPlaceId === null) {

            response = await fetch(
                `${API}/trips/${tripId}/places_to_visit`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(body)
                }
            );

        } else {

            response = await fetch(
                `${API}/places_to_visit/${editingPlaceId}`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(body)
                }
            );

        }

        if (!response.ok) {

            throw new Error("Unable to save place");

        }

        if (editingPlaceId === null) {

            alert("Place created successfully.");

        } else {

            alert("Place updated successfully.");

        }

        editingPlaceId = null;

        form.reset();

tripSelect.value = tripId;

        submitButton.innerHTML = `
            <i class="fa-solid fa-plus"></i>
            Add Place
        `;

         await loadPlaces(tripId);
         document.getElementById("placeName").focus();

    }

    catch (error) {

        console.error(error);

        alert("Unable to save place.");

    }

});




async function loadPlaces(tripId) {
  try {
    const response = await fetch(`${API}/trips/${tripId}/places_to_visit`);

    if (!response.ok) {
      throw new Error("Unable to load places");
    }

    const places = await response.json();

    placesTable.innerHTML = "";

    places.forEach((place) => {
      placesTable.innerHTML += `

            <tr>

                <td>${tripSelect.options[tripSelect.selectedIndex].text}</td>

                <td>${place.place_name}</td>

                <td>${place.visited ? "Visited" : "Not Visited"}</td>

<td class="actions">

    <button
        type="button"
        class="action-btn edit-btn"
        onclick="editPlace(${place.id})"
    >
        <i class="fa-solid fa-pen"></i>
    </button>

    <button
        type="button"
        class="action-btn delete-btn"
        onclick="deletePlace(${place.id})"
    >
        <i class="fa-solid fa-trash"></i>
    </button>

</td>

            </tr>

            `;
    });
  } catch (error) {
    console.error(error);

    alert("Unable to load places.");
  }
}

tripSelect.addEventListener("change", async () => {
    await loadPlaces(tripSelect.value);
});


/* ---------------- Edit Place ---------------- */

async function editPlace(id) {

    try {

        const tripId = tripSelect.value;

        const response = await fetch(
            `${API}/trips/${tripId}/places_to_visit`
        );

        if (!response.ok) {
            throw new Error("Unable to load places");
        }

        const places = await response.json();

        const place = places.find((p) => p.id === id);

        if (!place) {
            throw new Error("Place not found");
        }

        editingPlaceId = id;

        document.getElementById("placeName").value =
            place.place_name;

        document.getElementById("visited").value =
            place.visited ? 1 : 0;

        submitButton.innerHTML = `
            <i class="fa-solid fa-floppy-disk"></i>
            Update Place
        `;

    }

    catch (error) {

        console.error(error);

        alert("Unable to load place.");

    }

}


/* ---------------- Delete Place ---------------- */

async function deletePlace(id) {

    if (!confirm("Delete this place?")) return;

    try {

        const response = await fetch(

            `${API}/places_to_visit/${id}`,

            {

                method: "DELETE"

            }

        );

        if (!response.ok) {

            throw new Error("Delete failed");

        }

        alert("Place deleted successfully.");

        await loadPlaces(tripSelect.value);

    }

    catch (error) {

        console.error(error);

        alert("Unable to delete place.");

    }

}


/* ---------------- Start ---------------- */

loadTrips();
