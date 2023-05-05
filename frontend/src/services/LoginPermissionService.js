//ACCOUNT MANAGER?
export async function getAccountManager() {
	const token = localStorage.getItem("access_token");
	const headers = {
		"Content-Type": "application/json",
		Authorization: `JWT ${token}`,
	};
	try {
		const response = await fetch("http://127.0.0.1:8000/club/accounts/", {
			method: "GET",
			headers: headers,
		});
		const responseData = await response.json();
		try {
			if (
				responseData.detail ===
				"You do not have permission to perform this action."
			) {
				return null;
			}
		} catch (error) {}

		return responseData;
	} catch (error) {
		return "hello";
	}
}

//CLUBREP
export async function getClubAccounts() {
	const token = localStorage.getItem("access_token");
	const headers = {
		"Content-Type": "application/json",
		Authorization: `JWT ${token}`,
	};
	try {
		const response = await fetch("http://127.0.0.1:8000/club/accounts/", {
			method: "GET",
			headers: headers,
		});
		const responseData = await response.json();
		try {
			if (
				responseData.detail ===
				"You do not have permission to perform this action."
			) {
				return null;
			}
		} catch (error) {}
		return responseData;
	} catch (error) {
		return null;
	}
}

//CINEMA MANAGER
export async function getCinemaManager() {
	const token = localStorage.getItem("access_token");
	const headers = {
		"Content-Type": "application/json",
		Authorization: `JWT ${token}`,
	};
	try {
		const response = await fetch(
			"http://127.0.0.1:8000/uweflix/cinema-manager/",
			{
				method: "GET",
				headers: headers,
			}
		);
		const responseData = await response.json();
		try {
			if (
				responseData.detail ===
				"You do not have permission to perform this action."
			) {
				return null;
			}
		} catch (error) {}
		return responseData;
	} catch (error) {
		return null;
	}
}

//STUDENT
export async function getStudent() {
	const token = localStorage.getItem("access_token");
	const headers = {
		"Content-Type": "application/json",
		Authorization: `JWT ${token}`,
	};
	try {
		const response = await fetch("http://127.0.0.1:8000/uweflix/student/", {
			method: "GET",
			headers: headers,
		});
		const responseData = await response.json();
		try {
			if (
				responseData.detail ===
				"You do not have permission to perform this action."
			) {
				return null;
			}
		} catch (error) {}
		return responseData;
	} catch (error) {
		return null;
	}
}
