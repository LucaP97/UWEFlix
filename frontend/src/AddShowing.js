import React, { useState, useEffect } from "react";
import { Form, Button } from "react-bootstrap";
import { getAllFilms } from "./services/FilmService";
import { event } from "jquery";
import { useNavigate } from "react-router-dom";

// NEED TO INSTALL DATE PICKER: npm install react-date-picker
// NEED TO INSTALL TIME PICKER: npm install react-time-picker
import DatePicker from "react-date-picker";
import "react-date-picker/dist/DatePicker.css";
import "react-calendar/dist/Calendar.css";

import TimePicker from "react-time-picker";
import "react-time-picker/dist/TimePicker.css";
import "react-clock/dist/Clock.css";

// ONLY CINEMA MANAGER HAS AUTHORITY TO POST NEW SHOWINGS

function AddShowing() {
	const navigate = useNavigate();
	const [screenList, setScreenList] = useState([]);
	const [screen, setScreen] = useState("");

	const [filmsList, setFilmsList] = useState([]);
	const [film, setFilm] = useState("");
	const [date, setDate] = useState();
	const [time, setTime] = useState(null);
	const [studentPrice, setStudentPrice] = useState("");
	const [adultPrice, setAdultPrice] = useState("");
	const [childPrice, setChildPrice] = useState("");

	useEffect(() => {
		const fetchScreens = async () => {
			const response = await fetch("http://127.0.0.1:8000/uweflix/screens/");
			const data = await response.json();
			setScreenList(data);
		};
		const fetchFilms = async () => {
			const data = await getAllFilms();
			setFilmsList(data);
		};

		fetchScreens();
		fetchFilms();
	}, []);

	const handleSubmit = (e) => {
		e.preventDefault();

		const token = localStorage.getItem("access_token");
		const headers = {
			"Content-Type": "application/json",
			Authorization: `JWT ${token}`,
		};

		fetch("http://127.0.0.1:8000/uweflix/showings/", {
			method: "POST",
			headers: headers,
			body: JSON.stringify({
				screen: screen,
				film: film,
				showing_date: date,
				showing_time: time,
				price: {
					student: studentPrice,
					adult: adultPrice,
					child: childPrice,
				},
			}),
		})
			.then((response) => response.json())
			.then((data) => {
				console.log(`T: ${JSON.stringify(data)}`);
			});

		window.location.reload();
	};

	return (
		<div className="container">
			<Form
				onSubmit={handleSubmit}
				style={{
					display: "flex",
					flexDirection: "column",
					alignItems: "center",
				}}
			>
				<h2 style={{ marginTop: 10 }}>Add a new Showing</h2>
				<Form.Group
					controlId="screens"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Screen</Form.Label>
					<Form.Select
						value={screen?.id}
						onChange={(event) => setScreen(event.target.value)}
						required
					>
						<option value="">--Select a screen--</option>
						{screenList.map((screen) => (
							<option key={screen.id} value={screen.id}>
								{screen.screen_name}
							</option>
						))}
					</Form.Select>
				</Form.Group>
				<Form.Group
					controlId="films"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Film</Form.Label>
					<Form.Select
						value={film?.id}
						onChange={(event) => setFilm(event.target.value)}
						required
					>
						<option value="">--Select a film--</option>
						{filmsList.map((film) => (
							<option key={film.id} value={film.id}>
								{film.title}
							</option>
						))}
					</Form.Select>
				</Form.Group>
				<Form.Group
					controlId="formFirstName"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Date</Form.Label>
					<Form.Control
						type="date"
						placeholder="mm/dd/yy"
						value={date}
						onChange={(event) => setDate(event.target.value)}
					/>
				</Form.Group>
				<Form.Group
					controlId="formFirstName"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Time</Form.Label>
					<Form.Control
						type="time"
						placeholder="hh:mm"
						value={time}
						onChange={(event) => setTime(event.target.value)}
					/>
				</Form.Group>

				<Form.Group
					controlId="formFirstName"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Student Ticket Price</Form.Label>
					<Form.Control
						type="number"
						placeholder=""
						value={studentPrice}
						onChange={(event) => setStudentPrice(event.target.value)}
					/>
				</Form.Group>
				<Form.Group
					controlId="formFirstName"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Adult Ticket Price</Form.Label>
					<Form.Control
						type="number"
						placeholder=""
						value={adultPrice}
						onChange={(event) => setAdultPrice(event.target.value)}
					/>
				</Form.Group>
				<Form.Group
					controlId="formFirstName"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Child Ticket Price</Form.Label>
					<Form.Control
						type="number"
						placeholder=""
						value={childPrice}
						onChange={(event) => setChildPrice(event.target.value)}
					/>
				</Form.Group>

				<Button variant="primary" type="submit" style={{ marginTop: 20 }}>
					Add Showing
				</Button>
			</Form>
		</div>
	);
}
export default AddShowing;
