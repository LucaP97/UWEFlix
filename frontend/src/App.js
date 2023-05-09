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
import Statements from "./Statements";
import TransactionHistory from "./TransactionHistory";
import AccountList from "./AccountList";
import EditClubAccount from "./EditClubAccount";
import EditStudentAccount from "./EditStudentAccount";
import EditEmployeeAccount from "./EditEmployeeAccount";
import RegisterAccounts from "./RegisterAccounts";
import RegisterEmployee from "./RegisterEmployee";
import RegisterStudent from "./RegisterStudent";
import RegisterClub from "./RegisterClub"
import DiscountRequest from "./DiscountRequest";
import DiscountApproval from "./DiscountApproval";
import EditFilm from "./EditFilm";

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
						<Route path="/register" element={<RegisterStudent />} />
						<Route path="/login" element={<LoginUser />} />
						<Route path="/film_editing" element={<FilmListScreen />} />
						<Route path="/add_film" element={<AddFilmScreen />} />
						<Route path="/showings" element={<Showings />} />
						<Route path="/showings/booking" element={<Booking />} />
						<Route
							path="/showings/booking/payment"
							element={<PaymentScreen />}
						/>
						<Route path="/screens" element={<ScreenListScreen />} />
						<Route path="/film_editing/edit_film" element={<EditFilm />} />
						<Route path="/add_showings" element={<AddShowing />} />
						<Route path="/accounts" element={<AccountList />} />
						<Route path="/accounts/edit_club" element={<EditClubAccount />} />
						<Route
							path="/accounts/edit_student"
							element={<EditStudentAccount />}
						/>
						<Route
							path="/accounts/edit_employee"
							element={<EditEmployeeAccount />}
						/>
						<Route
							path="/register_account/club"
							element={<RegisterClub />}
						/>
						<Route path="/register_account" element={<RegisterAccounts />} />
						<Route path="/register_account/employee" element={<RegisterEmployee />} />
						<Route path="/register_account/student" element={<RegisterStudent />} />

						<Route path="/statements" element={<Statements />} />
						<Route path="/discount_request" element={<DiscountRequest />} />
						<Route path="/discount_approval" element={<DiscountApproval />} />
						<Route
							path="/statements/transactions"
							element={<TransactionHistory />}
						/>
					</Routes>
				</body>
			</html>
		</Router>
	);
}

export default App;
