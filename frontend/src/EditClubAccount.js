import React, { useState } from "react";
import { useLocation } from "react-router-dom";

import { Form, Button } from "react-bootstrap";
import { registerUser } from "./services/UserService";

function EditClubAccount() {
	const location = useLocation();
	const data = location.state?.data.club;

	const [name, setName] = useState(data.name);
	const [clubNumber, setClubNumber] = useState(data.club_number);
	//address
	const [streetNumber, setStreetNumber] = useState(data.address.street_number);
	const [street, setStreet] = useState(data.address.street);
	const [city, setCity] = useState(data.address.city);
	const [postCode, setPostCode] = useState(data.address.post_code);
	//contact details
	const [landlineNumber, setLandlineNumber] = useState(
		data.contact_details.landline_number
	);
	const [mobileNumber, setMobileNumber] = useState(
		data.contact_details.mobile_number
	);
	const [clubEmail, setClubEmail] = useState(data.contact_details.club_email);

	return (
		<div className="container">
			<Form
				onSubmit={() => {}}
				style={{
					display: "flex",
					flexDirection: "column",
					alignItems: "center",
				}}
			>
				<h2 style={{ marginTop: 10 }}>Edit Club Account</h2>
				<Form.Group
					controlId="formUsername"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Club Name</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter club name"
						value={name}
						onChange={(event) => setName(event.target.value)}
					/>
				</Form.Group>
                <Form.Group
					controlId="formUsername"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Club Number</Form.Label>
					<Form.Control
						type="number"
						placeholder="Enter club number"
						value={clubNumber}
						onChange={(event) => setClubNumber(event.target.value)}
					/>
				</Form.Group>

				<Form.Group
					controlId="formEmail"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Street Number</Form.Label>
					<Form.Control
						type="number"
						placeholder="Enter street number"
						value={streetNumber}
						onChange={(event) => setStreetNumber(event.target.value)}
					/>
				</Form.Group>

				<Form.Group
					controlId="formPassword"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Street</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter street name"
						value={street}
						onChange={(event) => setStreet(event.target.value)}
					/>
				</Form.Group>

				<Form.Group
					controlId="formFirstName"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>City</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter city"
						value={city}
						onChange={(event) => setCity(event.target.value)}
					/>
				</Form.Group>

				<Form.Group
					controlId="formLastName"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Post Code</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter post code"
						value={postCode}
						onChange={(event) => setPostCode(event.target.value)}
					/>
				</Form.Group>

                <Form.Group
					controlId="formLastName"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Landline Number</Form.Label>
					<Form.Control
						type="number"
						placeholder="Enter landline number"
						value={landlineNumber}
						onChange={(event) => setLandlineNumber(event.target.value)}
					/>
				</Form.Group>
                <Form.Group
					controlId="formLastName"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Mobile Number</Form.Label>
					<Form.Control
						type="number"
						placeholder="07594444444"
						value={mobileNumber}
						onChange={(event) => setMobileNumber(event.target.value)}
					/>
				</Form.Group>
                <Form.Group
					controlId="formLastName"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>email</Form.Label>
					<Form.Control
						type="email"
						placeholder="example@gmail.com"
						value={clubEmail}
						onChange={(event) => setClubEmail(event.target.value)}
					/>
				</Form.Group>

				<Button
					variant="primary"
					type="submit"
					style={{ marginTop: 20, width: "90%" }}
				>
					Update Details
				</Button>
				<hr style={{ width: "100%" }} />
				<a href="/accounts/edit_club" style={{marginBottom: 20}}>Refresh to old data</a>
			</Form>
		</div>
	);

	return <div>EditClubAccount</div>;
}

export default EditClubAccount;
