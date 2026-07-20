CREATE TABLE IF NOT EXISTS trips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    destination VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    travel_type ENUM(
        'Solo',
        'Friends',
        'Family',
        'Business',
        'Other'
    ) NOT NULL,
    estimated_budget DECIMAL(10,2) NOT NULL,
    status ENUM(
        'Planned',
        'Completed'
    ) NOT NULL DEFAULT 'Planned',
    rating INT,
    experience_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS places_to_visit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL,
    place_name VARCHAR(255) NOT NULL,
    visited BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (trip_id)
        REFERENCES trips(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS planning_notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL,
    note_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id)
        REFERENCES trips(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL,
    category ENUM(
        'Flight',
        'Hotel',
        'Food',
        'Shopping',
        'Transport',
        'Other'
    ) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    expense_date DATE NOT NULL,
    FOREIGN KEY (trip_id)
        REFERENCES trips(id)
        ON DELETE CASCADE
);
