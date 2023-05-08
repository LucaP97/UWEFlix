import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Showings from "./Showings";
import Booking from "./Booking";
import RegisterUser from "./RegisterUser";
import LoginUser from "./LoginUser";
import NavBar from "./Components/NavBar";
import FilmListScreen from "./FilmListScreen";
import AddFilmScreen from "./AddFilmScreen";
import ScreenListScreen from "./ScreenListScreen";
import PaymentScreen from "./PaymentScreen";
import AddShowing from "./AddShowing";

function App() {
	return (
		<Router>
			<html>
				<head>
					<meta charSet="UTF-8" />
					<meta
						name="viewport"
						content="width=device-width, initial-scale=1.0"
					/>
					<meta httpEquiv="X-UA-Compatible" content="ie=edge" />
					<title>Cinema Showings</title>
					<link
						rel="stylesheet"
						href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
						integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65"
						crossOrigin="anonymous"
					/>
				</head>

				<body>
					<NavBar />

					<Routes>
						<Route path="/" element={<LoginUser />} />
						<Route path="/register" element={<RegisterUser />} />
						<Route path="/login" element={<LoginUser />} />
						<Route path="/film_editing" element={<FilmListScreen />} />
						<Route path="/add_film" element={<AddFilmScreen />} />
						<Route path="/showings" element={<Showings />} />
						<Route path="/showings/booking" element={<Booking />} />
						<Route path="/showings/booking/payment"	element={<PaymentScreen />} />
						<Route path="/screens" element={<ScreenListScreen />} />
						<Route path="/add_showings" element={<AddShowing />} />
					</Routes>
				</body>
			</html>
		</Router>
	);
}

export default App;
