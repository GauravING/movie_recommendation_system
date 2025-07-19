const API_URL = "http://127.0.0.1:8000";

async function fetchMovies() {
    const response = await fetch(`${API_URL}/movies`);
    const data = await response.json();
    
    const movieDropdown = document.getElementById("movieDropdown");
    movieDropdown.innerHTML = '<option value="">Select a Movie</option>';

    data.movies.forEach(movie => {
        let option = document.createElement("option");
        option.value = movie;
        option.textContent = movie;
        movieDropdown.appendChild(option);
    });
}

async function getRecommendations() {
    // Get movie from input field or dropdown
    const typedMovie = document.getElementById("movieInput").value.trim();
    const selectedMovie = document.getElementById("movieDropdown").value;
    
    // Priority: If user types a movie, use that; otherwise, use dropdown selection
    const movieName = typedMovie || selectedMovie;

    if (!movieName) {
        alert("Please select or type a movie name!");
        return;
    }

    const response = await fetch(`${API_URL}/recommend?title=${encodeURIComponent(movieName)}`);
    const recommendations = await response.json();
    
    const recommendationsDiv = document.getElementById("recommendations");
    recommendationsDiv.innerHTML = "";

    if (recommendations.error) {
        recommendationsDiv.innerHTML = `<p>${recommendations.error}</p>`;
        return;
    }

    recommendations.forEach(movie => {
        let div = document.createElement("div");
        div.classList.add("movie");
        div.innerHTML = `
            <img src="${movie.poster || 'https://via.placeholder.com/150'}" alt="${movie.title}">
            <h3>${movie.title}</h3>
            <p><strong>Genre:</strong> ${movie.genre}</p>
            <p><strong>Language:</strong> ${movie.language}</p>
            <p><strong>Release Date:</strong> ${movie.release_date}</p>
            <p><strong>Ratings:</strong> ${movie.rating}</p>
        `;
        recommendationsDiv.appendChild(div);
    });
}

// Load movies when page loads
window.onload = fetchMovies;
