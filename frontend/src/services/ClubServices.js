export async function addClub(data) {
	const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`
	}
    try {
        const response = await fetch('http://127.0.0.1:8000/club/clubs/', {
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

export async function addClubRep(data) {
	const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`
	}
    try {
        const response = await fetch('http://127.0.0.1:8000/club/club_representative/', {
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

export async function requestDiscount(data) {
	const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`
	}
    try {
        const response = await fetch('http://127.0.0.1:8000/club/discount-request/', {
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

export async function getPendingRequests() {
	const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`
	}
    try {
        const response = await fetch('http://127.0.0.1:8000/club/discount-request/?request_status=P', {
            method: 'GET',
            headers: headers,

        })
        const responseData = await response.json();
        
        return responseData

    } catch (error) {
        console.log('not auth')
    }
}

export async function getApprovedRequests() {
	const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`
	}
    try {
        const response = await fetch('http://127.0.0.1:8000/club/discount-request/?request_status=A', {
            method: 'GET',
            headers: headers,

        })
        const responseData = await response.json();
        
        return responseData

    } catch (error) {
        console.log('not auth')
    }
}

export async function getRejectedRequests() {
	const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`
	}
    try {
        const response = await fetch('http://127.0.0.1:8000/club/discount-request/?request_status=R', {
            method: 'GET',
            headers: headers,

        })
        const responseData = await response.json();
        
        return responseData

    } catch (error) {
        console.log('not auth')
    }
}

export async function getDiscountRequests() {
	const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`
	}
    try {
        const response = await fetch('http://127.0.0.1:8000/club/discount-request/', {
            method: 'GET',
            headers: headers,

        })
        const responseData = await response.json();
        
        return responseData

    } catch (error) {
        console.log('not auth')
    }
}

export async function processRequest(data, id) {
	const token = localStorage.getItem('access_token')
	const headers = {
		'Content-Type': 'application/json',
  		'Authorization': `JWT ${token}`,

	}
    try {
        const response = await fetch(`http://127.0.0.1:8000/club/discount-request/${id}/`, {
            method: 'PUT',
            headers: headers,
            body: JSON.stringify(data)

        })
        const responseData = await response.json();
        
        return responseData

    } catch (error) {
        console.log('not auth')
    }
}

