export async function registerUser(data) {
    try {
        const response = await fetch('http://127.0.0.1:8000//uweflix/auth/users/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)

        })
        const responseData = await response.json();
        if (response.ok) {
            return responseData;
        } else {
            throw new Error(responseData.message)
        }
    } catch (error) {
        return error.message
    }
}