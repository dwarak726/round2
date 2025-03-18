import { initializeApp } from "./firebase/firebase-app.js";
import { getDatabase, ref, onValue } from "./firebase/firebase-database.js";

// Firebase Configuration
const firebaseConfig = {
    apiKey: "AIzaSyBTaAXYTJSVw4Jx21j2YQemETiArZWQmEU",
    authDomain: "test-round2.firebaseapp.com",
    databaseURL: "https://test-round2-default-rtdb.firebaseio.com",
    projectId: "test-round2",
    storageBucket: "test-round2.firebasestorage.app",
    messagingSenderId: "449080673841",
    appId: "1:449080673841:web:ec87d2b0394c0790f9b710",
    measurementId: "G-5HZNTEFXLL"
};

//  Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

document.addEventListener("DOMContentLoaded", () => {
    const leaderboardRef = ref(database, "leaderboard");
    const leaderboardTable = document.getElementById("leaderboard");
    const searchBar = document.getElementById("searchBar");

    let leaderboardData = [];

    // Fetch and update leaderboard
    onValue(leaderboardRef, (snapshot) => {
        leaderboardData = Object.entries(snapshot.val())
            .sort((a, b) => b[1] - a[1]) // Sort in descending order by score
            .map(([name, score], index) => ({ rank: index + 1, name, score })); // Add actual rank

        renderLeaderboard(leaderboardData);
    });

    // Search Functionality with Correct Ranking
    searchBar.addEventListener("input", (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const filteredData = leaderboardData.filter(({ name }) => name.toLowerCase().includes(searchTerm));
        renderLeaderboard(filteredData, true); // Pass flag to indicate it's a search
    });

    function renderLeaderboard(data, isSearch = false) {
        leaderboardTable.innerHTML = "";

        data.forEach(({ rank, name, score }) => {
            const row = document.createElement("tr");

            let rankClass = "normal";
            let rankSymbol = rank;
            if (rank === 1) { rankSymbol = "🥇"; rankClass = "gold"; }
            else if (rank === 2) { rankSymbol = "🥈"; rankClass = "silver"; }
            else if (rank === 3) { rankSymbol = "🥉"; rankClass = "bronze"; }

            row.innerHTML = `<td class="${rankClass}">${rankSymbol}</td> 
                             <td>${name}</td> 
                             <td>${score}</td>`;
            leaderboardTable.appendChild(row);
        });
    }
});
