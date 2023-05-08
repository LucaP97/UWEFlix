import React, { useState, useEffect } from "react";
import "./styles/approval.css";
import { getPendingRequests, processRequest } from "./services/ClubServices";

import { IonIcon } from "@ionic/react";
import { checkmarkCircleOutline, closeCircleOutline } from "ionicons/icons";

function DiscountApproval() {
	const [pendingRequests, setPendingRequests] = useState([]);

	useEffect(() => {
		const fetchPendingRequests = async () => {
			const data = await getPendingRequests();
			setPendingRequests(data);
		};

		fetchPendingRequests();
	}, []);

	const handleSubmit = async (decision, id) => {
		const data = {
			request_status: decision,
		};

		const response = await processRequest(data, id);
		const updatedRequests = pendingRequests.filter((request) => id !== request.id);
		setPendingRequests(updatedRequests);
	};

	return (
		<div className="list-requests" style={{ justifyContent: "flex-start" }}>
			{pendingRequests.map((request) => (
				<div className="row-request">
					<h3>
						{request.club}
						<h4>- {request.amount}% -</h4>
					</h3>
					<div
						style={{
							marginLeft: "auto",
							flexDirection: "row",
							display: "flex",
						}}
					>
						<IonIcon
							onClick={(event) => {
								event.preventDefault();

								handleSubmit("A", request.id);
							}}
							icon={checkmarkCircleOutline}
							color="green"
							size="large"
							style={{ marginRight: 10, marginLeft: 40, cursor: "pointer" }}
						/>

						<IonIcon
							onClick={() => {
								handleSubmit("R", request.id);
							}}
							icon={closeCircleOutline}
							color="red"
							size="large"
							style={{ marginRight: 5, marginLeft: 5, cursor: "pointer" }}
						/>
					</div>
				</div>
			))}
		</div>
	);
}

export default DiscountApproval;
