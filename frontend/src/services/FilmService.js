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

export async function editFilm(data, id) {
	const token = localStorage.getItem("access_token");
	const headers = {
		"Content-Type": "application/json",
		Authorization: `JWT ${token}`,
	};
	try {
		const response = await fetch(
			`http://127.0.0.1:8000//uweflix/films/${id}/`,
			{
				method: "PUT",
				headers: headers,
				body: JSON.stringify(data)
			}
		);
		return await response.json();
	} catch {
		return [];
	}
}

export async function deleteFilmShowings(id) {
	const token = localStorage.getItem("access_token");
	const headers = {
		"Content-Type": "application/json",
		Authorization: `JWT ${token}`,
	};
	try {
		const response = await fetch(
			`http://127.0.0.1:8000//uweflix/showings/${parseInt(id)}`,
			{
				method: "PUT",
				headers: headers,
				data: { is_active: false },
			}
		);
		return await response.json();
	} catch {
		return [];
	}
}

export async function addFilm(data) {
	const token = localStorage.getItem("access_token");
	const headers = {
		"Content-Type": "application/json",
		Authorization: `JWT ${token}`,
	};
	try {
		const response = await fetch("http://127.0.0.1:8000//uweflix/films/", {
			method: "POST",
			headers: headers,
			body: JSON.stringify(data),
		});
		const responseData = await response.json();

		return responseData;
	} catch (error) {
		console.log("not auth");
	}
}

export async function addFilmImage(data, id) {
	const token = localStorage.getItem("access_token");
	const headers = {
		enctype: "multipart/form-data",
		Authorization: `JWT ${token}`,
	};
	const formData = new FormData();
	formData.append("image", data.image);
	try {
		const response = await fetch(
			`http://127.0.0.1:8000/uweflix/films/${id}/images/`,
			{
				method: "POST",
				headers: headers,
				body: formData,
			}
		);
		const responseData = await response.json();
		console.log(responseData);

		return responseData;
	} catch (error) {}
}
