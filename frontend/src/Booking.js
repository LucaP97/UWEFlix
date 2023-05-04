import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import "./styles/booking.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Dropdown from "react-bootstrap/Dropdown";
import $ from "jquery";
import Popper from "popper.js";
import "bootstrap/dist/js/bootstrap.bundle.min";

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import { useNavigate } from "react-router-dom";
// import "./styles/payment.css";

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
	const { showings, image, title, duration, age, description } = state;

	const [studentTickets, setStudentTickets] = useState(0);
	const [childTickets, setChildTickets] = useState(0);
	const [adultTickets, setAdultTickets] = useState(0);
	const [totalCost, setTotalCost] = useState(0);

	const [showingTime, setShowingTime] = useState('')
	const [showingID, setShowingID] = useState(0)

	const navigate = useNavigate();

	//// bootstrap modal variables
	const [show, setShow] = useState(false);

	const confirmDetails = () => {
		setShow(false)
		navigate("/showings")
	};

	const handleClose = () => {
		setShow(false)
	};

	const handleShow = () => setShow(true);
	////


	function calculatePrice() {
		console.log(showings[0])
		if (showingID == 0) {
			const tempS = showings[0]
			const cost =
			studentTickets * tempS.price.student + adultTickets * tempS.price.adult + childTickets * tempS.price.child;
			return cost
		} else {
			const showingSelected = showings.find((showing) => showing.id == showingID)
			const cost =
			studentTickets * showingSelected.price.student + adultTickets * showingSelected.price.adult + childTickets * showingSelected.price.child;
			return cost
		}
	}

	//calculate total cost on ticket quantity change
	useEffect(() => {
		setTotalCost(calculatePrice());
	}, [studentTickets, adultTickets, childTickets, showingTime, showingID]);

	//post booking

	// create tickets
	// pay for tickets
	const bookShowing = (e) =>{
		e.preventDefault();

		// pay
		if(adultTickets === 0 && studentTickets === 0 && childTickets ===0){
			alert("Select ticket(s)")
			return;
		}
		else if(showingTime === ''){
			alert("Select time")
			return;
		}

		fetch("http://127.0.0.1:8000/uweflix/booking/",{
			method: "POST",
			headers: {"Content-Type": "application/json"},
		})
		.then(response => response.json())
        .then(data => {
			const token = localStorage.getItem('access_token')
        	const headers = {
				'Content-Type': 'application/json',
				'Authorization': `JWT ${token}`
        	}
            //console.log(`T: ${JSON.stringify(data.id)}`);
			if(adultTickets > 0){
				fetch(`http://127.0.0.1:8000/uweflix/booking/${data.id}/items/`,{
					method: "POST",
					headers: headers,
					body: JSON.stringify(
						{
							"showing_id": showingID,
							"ticket_type": "A",
							"quantity": adultTickets
						}
					)
					
				})
				.then(response => response.json())
				.then(data => {console.log(`T: ${JSON.stringify(data)}}`)})
			}
			if(studentTickets > 0){
				fetch(`http://127.0.0.1:8000/uweflix/booking/${data.id}/items/`,{
					method: "POST",
					headers: headers,
					body: JSON.stringify(
						{
							"showing_id": showingID,
							"ticket_type": "S",
							"quantity": studentTickets
						}
					)
					
				})
				.then(response => response.json())
				.then(data => {console.log(`T: ${JSON.stringify(data)}}`)})
			}
			if(childTickets > 0){
				fetch(`http://127.0.0.1:8000/uweflix/booking/${data.id}/items/`,{
					method: "POST",
					headers: headers,
					body: JSON.stringify(
						{
							"showing_id": showingID,
							"ticket_type": "C",
							"quantity": childTickets
						}
					)
					
				})
				.then(response => response.json())
				.then(data => {console.log(`T: ${JSON.stringify(data)}}`)})
			}

        })
		handleShow()
	}
	//post order
	

	return (
		<div style={{ height: "88vh" }}>
			<div className="film-container">
				<>
					<Modal show={show} onHide={handleClose}>
						<Modal.Header closeButton>
							<Modal.Title>Enter Details</Modal.Title>
						</Modal.Header>
						<Modal.Body>
							<Form>
								<Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
									<Form.Label>Full Name</Form.Label>
									<Form.Control
										type="text"
										placeholder="e.g. Jeff Winger"
										autoFocus
									/>
									<Form.Label>Email address</Form.Label>
									<Form.Control
										type="email"
										placeholder="name@example.com"
										autoFocus
									/>
								</Form.Group>
								<Form.Group
									className="mb-3"
									controlId="exampleForm.ControlTextarea1"
								>
									<Form.Label>Card Details</Form.Label>
									<div class="form-group">
										<input type="text" id="card-number" name="cardNumber" class="form-input" placeholder="Enter card number" required />
									</div>
									<Form.Label>Expiration Date</Form.Label>
									<div class="form-group">
										<input type="text" id="expiration-date" name="expirationDate" class="form-input" placeholder="MM/YY" required />
									</div>
									<Form.Label>Security Code</Form.Label>
									<div class="form-group">
										<input type="text" id="security-code" name="securityCode" class="form-input" placeholder="Enter security code" required />
									</div>
								</Form.Group>
						</Form>
						</Modal.Body>
						<Modal.Footer>
							<Button variant="secondary" onClick={handleClose}>
								Back
							</Button>
							<Button variant="primary" onClick={confirmDetails}>
								Confirm Details
							</Button>
						</Modal.Footer>
					</Modal>
				</>

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
					onClick={bookShowing}
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
