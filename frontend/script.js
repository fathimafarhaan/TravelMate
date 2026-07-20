const API_URL = "http://127.0.0.1:5000";

/* ---------------- Load Dashboard ---------------- */

async function loadDashboard() {
    try {

        const response = await fetch(`${API_URL}/analytics`);
        const data = await response.json();

        document.getElementById("totalTrips").textContent =
            data.total_trips;

        document.getElementById("completedTrips").textContent =
            data.completed_trips;

        document.getElementById("plannedTrips").textContent =
            data.planned_trips;

        document.getElementById("totalExpense").textContent =
            "₹" + data.total_expense;

        createTravelChart(data.travel_type_summary);

        createExpenseChart(data.expense_summary);

        loadBudgetTable(data.budget_vs_expense);

    } catch (error) {

        console.error("Dashboard Error:", error);

    }
}

/* ---------------- Budget Table ---------------- */

function loadBudgetTable(budgetData) {

    const tableBody =
        document.querySelector("#budgetTable tbody");

    tableBody.innerHTML = "";

    budgetData.forEach(item => {

        const row = `

        <tr>

            <td>${item.destination}</td>

            <td>₹${item.budget}</td>

            <td>₹${item.actual_expense}</td>

        </tr>

        `;

        tableBody.innerHTML += row;

    });

}

/* ---------------- Travel Type Chart ---------------- */

function createTravelChart(data) {

    new Chart(

        document.getElementById("travelTypeChart"),

        {

            type: "bar",

            data: {

                labels: data.map(item => item.travel_type),

                datasets: [

                    {

                        label: "Trips",

                        data: data.map(item => item.count)

                    }

                ]

            }

        }

    );

}

/* ---------------- Expense Chart ---------------- */

function createExpenseChart(data) {

    new Chart(

        document.getElementById("expenseChart"),

        {

            type: "pie",

            data: {

                labels: data.map(item => item.category),

                datasets: [

                    {

                        data: data.map(item => item.total_amount)

                    }

                ]

            }

        }

    );

}

/* ---------------- Start ---------------- */

loadDashboard();