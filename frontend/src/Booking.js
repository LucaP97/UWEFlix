import React, { useState, useEffect } from "react";
import { json, useLocation } from "react-router-dom";
import "./styles/booking.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Dropdown from "react-bootstrap/Dropdown";
import $ from "jquery";
import Popper from "popper.js";
import "bootstrap/dist/js/bootstrap.bundle.min";

import Modal from 'react-bootstrap/Modal';

import { useNavigate } from "react-router-dom";

import {Elements} from '@stripe/react-stripe-js';
import {loadStripe} from '@stripe/stripe-js';

import PaymentForm from "./Components/PaymentForm";


const PUBLIC_KEY = "pk_test_51N4LoiLd0kDzPKsuvJc8mH6lamfaJhh0piWQOR6zwAAnGszWaSMblJmcdS63jXSQx4nI4cn4MesJgZvJvbuosYJp00kONN7cZ9"
const stripePromise = loadStripe(PUBLIC_KEY)


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

const CARD_OPTIONS = {
	iconStyle: "solid",
	style: {
		base: {
			iconColor: "#000000",
			color: "#000000",
			fontWeight: 500,
			fontFamily: "Roboto, Open Sans, Segoe UI, sans-serif",
			fontSize: "16px",
			fontSmoothing: "antialiased",
			":-webkit-autofill": { color: "#000000" },
			"::placeholder": { color: "#000000" }
		},
		invalid: {
			iconColor: "#000000",
			color: "#000000"
		}
	}
}

function Booking() {

	const { state } = useLocation();
	const { showings, image, title, duration, age, description } = state;

	const navigate = useNavigate();

	const [studentTickets, setStudentTickets] = useState(0);
	const [childTickets, setChildTickets] = useState(0);
	const [adultTickets, setAdultTickets] = useState(0);
	const [totalCost, setTotalCost] = useState(0);

	const [showingTime, setShowingTime] = useState('')
	const [showingID, setShowingID] = useState(0)

	const [show, setShow] = useState(false);

	const handleClose = () => {
		setShow(false)
	};

	const handlePayment = () => setShow(true);

	function calculatePrice() {
		if (showingID == 0) {
			const tempS = showings[0];
			const cost =
				studentTickets * tempS.price.student +
				adultTickets * tempS.price.adult +
				childTickets * tempS.price.child;
			return cost;
		} else {
			const showingSelected = showings.find(
				(showing) => showing.id == showingID
			);
			const cost =
				studentTickets * showingSelected.price.student +
				adultTickets * showingSelected.price.adult +
				childTickets * showingSelected.price.child;
			return cost;
		}
	}

	//calculate total cost on ticket quantity change
	useEffect(() => {
		setTotalCost(calculatePrice());
	}, [studentTickets, adultTickets, childTickets, showingTime, showingID]);

	useEffect(() => {

		localStorage.setItem('total_price', JSON.stringify({total_price: totalCost}));
		// Check to see if this is a redirect back from Checkout
		const query = new URLSearchParams(window.location.search);
	
		if (query.get("success")) {
		  console.log("Order placed! You will receive an email confirmation.");
		}
	
		if (query.get("canceled")) {
			console.log(
			"Order canceled -- continue to shop around and checkout when you're ready."
		  );
		}
	  }, []);


	//post booking
	const showModal = (e) =>{
		e.preventDefault();

		if(adultTickets === 0 && studentTickets === 0 && childTickets ===0){
			alert("Select ticket(s)")
			return;
		}
		else if(showingTime === ''){
			alert("Select time")
			return;
		}
		
		handlePayment()
	}
	
	//post order

	return (
		<div style={{ height: "88vh" }}>
			<div className="film-container">
				<>
					<Modal show={show} onHide={handleClose}>
						<Modal.Header>
							<Modal.Title><h1>Purchase Tickets</h1></Modal.Title>
						</Modal.Header>
						<Modal.Body>
							<div>
								<h3>
									Total Price: {totalCost}
								</h3>
							</div>

							<Elements stripe={stripePromise}>
								<PaymentForm totalCost={totalCost}/>	
							</Elements>
						</Modal.Body>

					</Modal>
				</>
				<img
					className="image-booking"
					src={image}
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
							onClick={() =>
								setStudentTickets(
									studentTickets > 0 ? studentTickets - 1 : studentTickets
								)
							}
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
							onClick={() =>
								setChildTickets(
									childTickets > 0 ? childTickets - 1 : childTickets
								)
							}
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
							onClick={() =>
								setAdultTickets(
									adultTickets > 0 ? adultTickets - 1 : adultTickets
								)
							}
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
					<h4
						style={{ padding: 2, backgroundColor: "white", borderRadius: 10 }}
					>
						{totalCost}£
					</h4>
				</div>

				<button
					className={"btn btn-primary"}
					style={{ float: "right", marginLeft: "2vw" }}
					onClick={showModal}
				>
					Confirm Booking
				</button>
				<div style={{ float: "right", marginLeft: "3vw" }}>
					{
						<Dropdown>
							<Dropdown.Toggle variant="success" id="dropdown-basic">
								{showingTime == ""
									? "Select Time"
									: showingTime.substring(0, 5)}
							</Dropdown.Toggle>

							<Dropdown.Menu>
								{showings.map((showing) => (
									<Dropdown.Item
										onClick={() => {
											setShowingTime(showing.showing_time);
											setShowingID(showing.id);
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
