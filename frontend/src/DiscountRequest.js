import React, { useEffect, useState } from "react";
import { Button, Form } from "react-bootstrap";
import "./styles/discount.css";

import {
	requestDiscount,
	getPendingRequests,
	getApprovedRequests,
	getDiscountRequests,
} from "./services/ClubServices";

function DiscountRequest() {
	const [rate, setRate] = useState();
	const [pendingRequest, setPendingRequests] = useState([]);
	const [requests, setRequests] = useState([]);
	const [approvedRequests, setApprovedRequests] = useState([]);

	const handleSubmit = async (event) => {
		event.preventDefault();

		const response = await requestDiscount({
			amount: rate,
		});

		window.location.reload()
	};

	useEffect(() => {
		const fetchPendingRequests = async () => {
			const data = await getPendingRequests();
			setPendingRequests(data);
		};

		const fetchApprovedRequests = async () => {
			const data = await getApprovedRequests();
			setApprovedRequests(data);
		};

		const fetchRequests = async () => {
			const data = await getDiscountRequests();
			setRequests(data);
		};

		fetchPendingRequests();
		fetchApprovedRequests();
		fetchRequests();
	}, []);

	//check if last request was approved or rejected

	return pendingRequest.length !== 0 ? (
		<div className="container">
			<div className="row-disc">
				<h4>Pending Approval for a discount of {pendingRequest[0].amount}%</h4>
				<h6 style={{ opacity: 0.7 }}>
					Wait until approval or rejection to make a new request
				</h6>
			</div>
		</div>
	) : (
		<div className="container">
			{requests.length !== 0 ? (
				requests[requests.length - 1].request_status !== "P" ? (
					<div className="row-disc" style={{ marginTop: 20 }}>
						<h4>
							Your last request has been{" "}
							{requests[requests.length - 1].request_status === "A"
								? "approved"
								: "rejected"}
							!
						</h4>
						<h5 style={{ opacity: 0.7 }}>
							{approvedRequests.length === 0
								? "No discount has been granted yet"
								: `A discount of ${
										approvedRequests[approvedRequests.length - 1].amount
								  }% was last 
							 granted`}
						</h5>
					</div>
				) : (
					<></>
				)
			) : (
				<></>
			)}
			<Form
				onSubmit={handleSubmit}
				style={{
					display: "flex",
					flexDirection: "column",
					alignItems: "center",
				}}
			>
				<h2 style={{ marginTop: 10 }}>Request Discount</h2>
				<Form.Group
					controlId="formUsername"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Amount 1-100(%)</Form.Label>
					<Form.Control
						type="number"
						placeholder=""
						value={rate}
						onChange={(event) => setRate(event.target.value)}
					/>
				</Form.Group>
				<Button
					variant="primary"
					type="submit"
					style={{ marginTop: 20, width: "90%" }}
				>
					Send Request
				</Button>
			</Form>
		</div>
	);
}

export default DiscountRequest;
