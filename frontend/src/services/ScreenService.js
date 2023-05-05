export async function getAllScreens() {
	try {
		const response = await fetch(
			"http://127.0.0.1:8000//uweflix/screens/?format=json"
		);
		return await response.json();
	} catch {
		return [];
	}
}

export async function addScreen(data) {
	const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`
	}
    try {
        const response = await fetch('http://127.0.0.1:8000//uweflix/screens/', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(data)

        })
        const responseData = await response.json();
        
        return responseData

    } catch (error) {
        console.log('not auth')
    }
}