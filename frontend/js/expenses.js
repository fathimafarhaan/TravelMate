const API = "http://127.0.0.1:5000";

const form = document.getElementById("expenseForm");

const tripSelect = document.getElementById("tripSelect");

const expensesTable =
    document.getElementById("expensesTable");

const category =
    document.getElementById("category");

const amount =
    document.getElementById("amount");

const expenseDate =
    document.getElementById("expenseDate");

const description =
    document.getElementById("description");

const submitButton =
    form.querySelector('button[type="submit"]');

let editingExpenseId = null;

/* ---------------- Load Trips ---------------- */

async function loadTrips() {

    try {

        const response =
            await fetch(`${API}/trips`);

        if (!response.ok) {

            throw new Error(
                "Unable to load trips"
            );

        }

        const trips =
            await response.json();

        tripSelect.innerHTML = `

            <option
                selected
                disabled
            >
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

/* ---------------- Create / Update Expense ---------------- */

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const tripId = tripSelect.value;

    const body = {

        category: category.value,

        amount: Number(amount.value),

        description: description.value,

        expense_date: expenseDate.value

    };

    try {

        let response;

        if (editingExpenseId === null) {

            response = await fetch(

                `${API}/trips/${tripId}/expenses`,

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

                `${API}/expenses/${editingExpenseId}`,

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

            throw new Error("Unable to save expense");

        }

        if (editingExpenseId === null) {

            alert("Expense created successfully.");

        }

        else {

            alert("Expense updated successfully.");

        }

        editingExpenseId = null;

        form.reset();

        tripSelect.value = tripId;

        submitButton.innerHTML = `
            <i class="fa-solid fa-wallet"></i>
            Add Expense
        `;

        await loadExpenses(tripId);

        amount.focus();

    }

    catch (error) {

        console.error(error);

        alert("Unable to save expense.");

    }

});

/* ---------------- Load Expenses ---------------- */

async function loadExpenses(tripId) {

    try {

        const response = await fetch(

            `${API}/trips/${tripId}/expenses`

        );

        if (!response.ok) {

            throw new Error("Unable to load expenses");

        }

        const expenses = await response.json();

        expensesTable.innerHTML = "";

        expenses.forEach((expense) => {

            expensesTable.innerHTML += `

                <tr>

                    <td>
                        ${tripSelect.options[tripSelect.selectedIndex].text}
                    </td>

                    <td>${expense.category}</td>

                    <td>₹${expense.amount}</td>

                    <td>${expense.expense_date}</td>

                    <td class="actions">

                        <button
                            type="button"
                            class="action-btn edit-btn"
                            onclick="editExpense(${expense.id})"
                        >
                            <i class="fa-solid fa-pen"></i>
                        </button>

                        <button
                            type="button"
                            class="action-btn delete-btn"
                            onclick="deleteExpense(${expense.id})"
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

        alert("Unable to load expenses.");

    }

}

/* ---------------- Load Expenses When Trip Changes ---------------- */

tripSelect.addEventListener("change", async () => {

    await loadExpenses(tripSelect.value);

});

/* ---------------- Edit Expense ---------------- */

async function editExpense(id) {

    try {

        const tripId = tripSelect.value;

        const response = await fetch(

            `${API}/trips/${tripId}/expenses`

        );

        if (!response.ok) {

            throw new Error("Unable to load expenses");

        }

        const expenses = await response.json();

        const expense = expenses.find((e) => e.id === id);

        if (!expense) {

            throw new Error("Expense not found");

        }

        editingExpenseId = id;

        category.value =
            expense.category;

        amount.value =
            expense.amount;

        expenseDate.value =
            expense.expense_date;

        description.value =
            expense.description ?? "";

        submitButton.innerHTML = `
            <i class="fa-solid fa-floppy-disk"></i>
            Update Expense
        `;

        amount.focus();

    }

    catch (error) {

        console.error(error);

        alert("Unable to load expense.");

    }

}

/* ---------------- Delete Expense ---------------- */

async function deleteExpense(id) {

    if (!confirm("Delete this expense?")) return;

    try {

        const response = await fetch(

            `${API}/expenses/${id}`,

            {

                method: "DELETE"

            }

        );

        if (!response.ok) {

            throw new Error("Delete failed");

        }

        alert("Expense deleted successfully.");

        await loadExpenses(tripSelect.value);

    }

    catch (error) {

        console.error(error);

        alert("Unable to delete expense.");

    }

}

/* ---------------- Start ---------------- */

loadTrips(); 