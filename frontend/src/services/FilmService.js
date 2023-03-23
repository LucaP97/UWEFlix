export async function getAllFilms() {
    try {
        const response = await fetch('http://127.0.0.1:8000//uweflix/films/?format=json')
        return await response.json();
    } catch {
        return []
    }
}