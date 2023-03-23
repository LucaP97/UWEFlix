import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import "./styles/booking.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Dropdown from "react-bootstrap/Dropdown";
import $ from "jquery";
import Popper from "popper.js";
import "bootstrap/dist/js/bootstrap.bundle.min";

function ageRatingColor(age) {
	if (age <= 3) {
		return "green";
	} else if (age <= 9) {
		return "yellow";
	} else if (age <= 12) {
		return "orange";
	} else if (age <= 15) {
		return "pink";
	} else {
		return "red";
	}
}

function Booking() {
	const { state } = useLocation();
	console.log(state);
	const { showings, image, title, duration, age, description } = state;

	//Ticket costs
	const SPRICE = 8;
	const APRICE = 12;
	const CPRICE = 7;

	const [studentTickets, setStudentTickets] = useState(0);
	const [childTickets, setChildTickets] = useState(0);
	const [adultTickets, setAdultTickets] = useState(0);
	const [totalCost, setTotalCost] = useState(0);

	const [showingTime, setShowingTime] = useState('')
	const [showingID, setShowingID] = useState(0)

	function calculatePrice() {
		if (showingID == 0) {
			const tempS = showings[0]
			const cost =
			studentTickets * tempS.student_price + adultTickets * tempS.adult_price + childTickets * tempS.child_price;
			return cost
		} else {
			const showingSelected = showings.find((showing) => showing.id == showingID)
			const cost =
			studentTickets * showingSelected.student_price + adultTickets * showingSelected.adult_price + childTickets * showingSelected.child_price;
			return cost
		}
	}

	//calculate total cost on ticket quantity change
	useEffect(() => {
		setTotalCost(calculatePrice());
	}, [studentTickets, adultTickets, childTickets, showingTime, showingID]);

	return (
		<div style={{ height: "88vh" }}>
			{console.log(studentTickets)}
			<div className="film-container">
				<img
					className="image-booking"
					src={require("./imgs/" + image)}
					alt="Fight club poster"
				/>
				<div className="film-details">
					<h2 className="title">
						{title.charAt(0).toUpperCase() + title.slice(1)}
					</h2>
					<h5 style={{ opacity: 0.75 }}>
						{duration.toString().slice(0, -3)} minutes
					</h5>
					<h6>
						<span
							className="age-rating"
							style={{ backgroundColor: ageRatingColor(age) }}
						>
							{age}
						</span>
						<span style={{ opacity: 0.6 }}>Age rating</span>
					</h6>
					<p>{description}</p>
				</div>
			</div>
			<div className="booking-container">
				<div style={{ float: "left" }}>
					<p style={{ fontSize: 22, float: "left" }}>Students:</p>
					<div style={{ float: "left", marginLeft: "1vw", fontSize: 22 }}>
						{studentTickets}
						{"  "}
						<button
							className="btn btn-outline-success"
							style={{
								padding: 3,
								paddingLeft: 7,
								paddingRight: 7,
								marginBottom: 5,
							}}
							onClick={() => setStudentTickets(studentTickets + 1)}
						>
							+
						</button>
						{"   "}
						<button
							className="btn btn-outline-success"
							style={{
								padding: 3,
								paddingLeft: 10,
								paddingRight: 10,
								marginBottom: 5,
							}}
							onClick={() => setStudentTickets(studentTickets > 0 ? studentTickets - 1 : studentTickets)}
						>
							-
						</button>
					</div>
				</div>
				<div style={{ float: "left", marginLeft: "3vw" }}>
					<p style={{ fontSize: 22, float: "left" }}>Children:</p>
					<div style={{ float: "left", marginLeft: "1vw", fontSize: 22 }}>
						{childTickets}
						{"  "}
						<button
							className="btn btn-outline-success"
							style={{
								padding: 3,
								paddingLeft: 7,
								paddingRight: 7,
								marginBottom: 5,
							}}
							onClick={() => setChildTickets(childTickets + 1)}
						>
							+
						</button>
						{"   "}
						<button
							className="btn btn-outline-success"
							style={{
								padding: 3,
								paddingLeft: 10,
								paddingRight: 10,
								marginBottom: 5,
							}}
							onClick={() => setChildTickets(childTickets > 0 ? childTickets - 1 : childTickets)}
						>
							-
						</button>
					</div>
				</div>
				<div style={{ float: "left", marginLeft: "3vw" }}>
					<p style={{ fontSize: 22, float: "left" }}>Adults:</p>
					<div style={{ float: "left", marginLeft: "1vw", fontSize: 22 }}>
						{adultTickets}
						{"  "}
						<button
							className="btn btn-outline-success"
							style={{
								padding: 3,
								paddingLeft: 7,
								paddingRight: 7,
								marginBottom: 5,
							}}
							onClick={() => setAdultTickets(adultTickets + 1)}
						>
							+
						</button>
						{"   "}
						<button
							className="btn btn-outline-success"
							style={{
								padding: 3,
								paddingLeft: 10,
								paddingRight: 10,
								marginBottom: 5,
							}}
							onClick={() => setAdultTickets(adultTickets > 0 ? adultTickets - 1 : adultTickets)}
						>
							-
						</button>
					</div>
				</div>
				<div
					style={{
						float: "left",
						marginLeft: "2vw",
						marginTop: 0,
						width: 60,
						textAlign: "center",
					}}
				>
					<h4 style={{ padding: 2, backgroundColor: 'white', borderRadius: 10 }}>{totalCost}£</h4>
				</div>

				<button
					className={"btn btn-primary"}
					style={{ float: "right", marginLeft: "2vw" }}
					onClick={() => {}}
				>
					Confirm Booking
				</button>
				<div style={{ float: "right", marginLeft: "3vw" }}>
					{
						<Dropdown>
							<Dropdown.Toggle variant="success" id="dropdown-basic">
								{showingTime == '' ? 'Select Time' : showingTime.substring(0, 5)}
							</Dropdown.Toggle>

							<Dropdown.Menu>
								{showings.map((showing) => (
									<Dropdown.Item onClick={() => {
										setShowingTime(showing.showing_time)
										setShowingID(showing.id)
										}}
									>
										{showing.showing_time.substring(0, 5)}
									</Dropdown.Item>
								))}
							</Dropdown.Menu>
						</Dropdown>
					}
				</div>
			</div>
		</div>
	);
}

export default Booking;
