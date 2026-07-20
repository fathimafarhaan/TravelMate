const API = "http://127.0.0.1:5000";

const form = document.getElementById("noteForm");

const tripSelect = document.getElementById("tripSelect");

const notesTable = document.getElementById("notesTable");

const noteText = document.getElementById("noteText");

const submitButton =
    form.querySelector('button[type="submit"]');

let editingNoteId = null;

/* ---------------- Load Trips ---------------- */

async function loadTrips() {

    try {

        const response = await fetch(`${API}/trips`);

        if (!response.ok) {

            throw new Error("Unable to load trips");

        }

        const trips = await response.json();

        tripSelect.innerHTML = `
            <option selected disabled>
                Select Trip
            </option>
        `;

        trips.forEach((trip) => {

            tripSelect.innerHTML += `

                <option value="${trip.id}">
                    ${trip.destination}
                </option>

            `;

        });

    }

    catch (error) {

        console.error(error);

        alert("Unable to load trips.");

    }

}

/* ---------------- Create / Update Note ---------------- */

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const tripId = tripSelect.value;

    const body = {

        note_text: noteText.value

    };

    try {

        let response;

        if (editingNoteId === null) {

            response = await fetch(

                `${API}/trips/${tripId}/planning_notes`,

                {

                    method: "POST",

                    headers: {

                        "Content-Type": "application/json"

                    },

                    body: JSON.stringify(body)

                }

            );

        }

        else {

            response = await fetch(

                `${API}/planning_notes/${editingNoteId}`,

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

            throw new Error("Unable to save note");

        }

        if (editingNoteId === null) {

            alert("Note created successfully.");

        }

        else {

            alert("Note updated successfully.");

        }

        editingNoteId = null;

        form.reset();

        tripSelect.value = tripId;

        submitButton.innerHTML = `
            <i class="fa-solid fa-note-sticky"></i>
            Add Note
        `;

        await loadNotes(tripId);

        noteText.focus();

    }

    catch (error) {

        console.error(error);

        alert("Unable to save note.");

    }

});

/* ---------------- Load Notes ---------------- */

async function loadNotes(tripId) {

    try {

        const response = await fetch(

            `${API}/trips/${tripId}/planning_notes`

        );

        if (!response.ok) {

            throw new Error("Unable to load notes");

        }

        const notes = await response.json();

        notesTable.innerHTML = "";

        notes.forEach((note) => {

            notesTable.innerHTML += `

                <tr>

                    <td>
                        ${tripSelect.options[tripSelect.selectedIndex].text}
                    </td>

                    <td>${note.note_text}</td>

                    <td>${note.created_at ?? "-"}</td>

                    <td class="actions">

                        <button
                            type="button"
                            class="action-btn edit-btn"
                            onclick="editNote(${note.id})"
                        >
                            <i class="fa-solid fa-pen"></i>
                        </button>

                        <button
                            type="button"
                            class="action-btn delete-btn"
                            onclick="deleteNote(${note.id})"
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

        alert("Unable to load notes.");

    }

}

/* ---------------- Load Notes When Trip Changes ---------------- */

tripSelect.addEventListener("change", async () => {

    await loadNotes(tripSelect.value);

});

/* ---------------- Edit Note ---------------- */

async function editNote(id) {

    try {

        const tripId = tripSelect.value;

        const response = await fetch(

            `${API}/trips/${tripId}/planning_notes`

        );

        if (!response.ok) {

            throw new Error("Unable to load notes");

        }

        const notes = await response.json();

        const note = notes.find((n) => n.id === id);

        if (!note) {

            throw new Error("Note not found");

        }

        editingNoteId = id;

        noteText.value = note.note_text;

        submitButton.innerHTML = `
            <i class="fa-solid fa-floppy-disk"></i>
            Update Note
        `;

        noteText.focus();

    }

    catch (error) {

        console.error(error);

        alert("Unable to load note.");

    }

}

/* ---------------- Delete Note ---------------- */

async function deleteNote(id) {

    if (!confirm("Delete this note?")) return;

    try {

        const response = await fetch(

            `${API}/planning_notes/${id}`,

            {

                method: "DELETE"

            }

        );

        if (!response.ok) {

            throw new Error("Delete failed");

        }

        alert("Note deleted successfully.");

        await loadNotes(tripSelect.value);

    }

    catch (error) {

        console.error(error);

        alert("Unable to delete note.");

    }

}

/* ---------------- Start ---------------- */

loadTrips();