export async function getAllShowings() {
    try {
        const response = await fetch('http://127.0.0.1:8000/showings/?format=json')
        return await response.json();
    } catch {
        return []
    }
}