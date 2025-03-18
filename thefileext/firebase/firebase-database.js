export function getDatabase(app) {
    return { app };
}

export function ref(database, path) {
    return `${database.app.config.databaseURL}/${path}.json`;
}

export function onValue(reference, callback) {
    fetch(reference)
        .then(response => response.json())
        .then(data => callback({ val: () => data }))
        .catch(error => console.error("Firebase Error:", error));
}
