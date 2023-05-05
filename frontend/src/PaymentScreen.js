import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./styles/payment.css";
import { Form, Button } from "react-bootstrap";

import { IonIcon } from "@ionic/react";
import { checkmarkCircleOutline } from "ionicons/icons";

function PaymentScreen() {
	const navigate = useNavigate()
	const { state } = useLocation();

	let STickets,
		ATickets,
		CTickets,
		totalCost,
		showingTime,
		showingID,
		image,
		title,
		duration;
	if (state) {
		({
			STickets,
			ATickets,
			CTickets,
			totalCost,
			showingTime,
			showingID,
			image,
			title,
			duration,
		} = state);
	}

	const [cardNum, setCardNum] = useState();
	const [cardName, setCardName] = useState();
	const [expDate, setExpDate] = useState();

	const [bookingConfirmed, setBookingConfirmed] = useState(false);

	return (
		<div  onClick={bookingConfirmed ? () => navigate("/showings") : () => {}}>
			{bookingConfirmed && (
				<div className="booking-confirmation-popup">
					<IonIcon icon={checkmarkCircleOutline} size="large" />
					<p style={{color: 'white'}}>Your booking has been confirmed!</p>
				</div>
			)}
			<div className="container" style={{opacity: bookingConfirmed ? 0.06 : 1 }}>
				<div
					style={{
						display: "flex",
						flexDirection: "row",
						alignItems: "center",
						justifyContent: "center",
					}}
				>
					<div className="row-container">
						<div class="image-container">
							<img
								className="image-film"
								src={require("./imgs/" + image)}
								alt="Fight club poster"
							/>
						</div>
						<div
							style={{
								display: "flex",
								flexDirection: "column",
								alignItems: "center",
							}}
						>
							<h3 className="film-title">
								{title.charAt(0).toUpperCase() + title.slice(1)}
							</h3>
							<h5 className="film-title">{showingTime.substring(0, 5)}</h5>
						</div>
					</div>
					<div>
						<h4 className="row-container">Total Cost: {totalCost}£</h4>
					</div>
				</div>
				<Form
					onSubmit={(event) => {
						event.preventDefault();
						setBookingConfirmed(true);
					}}
					style={{
						display: "flex",
						flexDirection: "column",
						alignItems: "center",
					}}
				>
					<h3 style={{ marginTop: 10 }}>Payment Details</h3>
					<Form.Group
						controlId="formCardholderName"
						style={{ marginBottom: 10, width: "90%" }}
					>
						<Form.Label>Cardholder Name</Form.Label>
						<Form.Control
							type="text"
							placeholder="Enter cardholder's name"
							value={cardName}
							onChange={(event) => setCardName(event.target.value)}
						/>
					</Form.Group>

					<Form.Group
						controlId="formCardName"
						style={{ marginBottom: 10, width: "90%" }}
					>
						<Form.Label>Card Number</Form.Label>
						<Form.Control
							type="number"
							placeholder="Enter cardholders name"
							value={cardNum}
							onChange={(event) => setCardNum(event.target.value)}
						/>
					</Form.Group>
					<Form.Group
						controlId="formExpiryDate"
						style={{ marginBottom: 10, width: "90%" }}
					>
						<Form.Label>Expiry Date</Form.Label>
						<Form.Control
							type="month"
							placeholder="Enter expiry date"
							value={expDate}
							onChange={(event) => setExpDate(event.target.value)}
						/>
					</Form.Group>

					<Button
						variant="primary"
						type="submit"
						style={{ marginTop: 20, width: "90%" }}
					>
						Confirm Booking
					</Button>
				</Form>
			</div>
		</div>
	);
}

export default PaymentScreen;
