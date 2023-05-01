export async function getAllFilms() {
	try {
		const response = await fetch(
			"http://127.0.0.1:8000//uweflix/films/?format=json"
		);
		return await response.json();
	} catch {
		return [];
	}
}

export async function deleteFilm(id) {
	try {
		const response = await fetch(`http://127.0.0.1:8000//uweflix/films/${parseInt(id)}`, {
			method: "DELETE",
		});
		return await response.json();
	} catch {
		return [];
	}
}

export async function deleteFilmShowings(id) {
	try {
		const response = await fetch(`http://127.0.0.1:8000//uweflix/showings/${parseInt(id)}`, {
			method: "DELETE",
		});
		return await response.json();
	} catch {
		return [];
	}
}

