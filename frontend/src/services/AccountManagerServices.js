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

export async function getClubAccounts() {
    const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`
	}
	try {
		const response = await fetch(
			"http://127.0.0.1:8000/club/clubs/", {
                method: "GET",
                headers: headers,
            }
		);
		return await response.json();
	} catch {
		return [];
	}
}

export async function getStudentAccounts() {
    const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`
	}
	try {
		const response = await fetch(
			"http://127.0.0.1:8000/uweflix/student/", {
                method: "GET",
                headers: headers,
            }
		);
		return await response.json();
	} catch {
		return [];
	}
}

export async function getEmployeeAccounts() {
    const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`
	}
	try {
		const response = await fetch(
			"http://127.0.0.1:8000/uweflix/employee/", {
                method: "GET",
                headers: headers,
            }
		);
		return await response.json();
	} catch {
		return [];
	}
}

export async function addEmployee(data) {
	const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`
	}
    try {
        const response = await fetch('http://localhost:8000/uweflix/employee/', {
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
export async function addStudent(data) {
	const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`
	}
    try {
        const response = await fetch('http://localhost:8000/uweflix/student/', {
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
