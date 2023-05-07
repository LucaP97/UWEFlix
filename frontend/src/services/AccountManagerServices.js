export async function getAllStatements() {
    const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`
	}
	try {
		const response = await fetch(
			"http://127.0.0.1:8000/accounts/statements/", {
                method: "GET",
                headers: headers,
            }
		);
		return await response.json();
	} catch {
		return [];
	}
}