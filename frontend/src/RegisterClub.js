import React, { useState } from "react";
import { useLocation } from "react-router-dom";

import { Form, Button } from "react-bootstrap";
import { addClub, addClubRep } from "./services/ClubServices";

function RegisterClub() {
	//CLUB INFO
	const [name, setName] = useState("");
	const [clubNumber, setClubNumber] = useState("");
	//address
	const [streetNumber, setStreetNumber] = useState("");
	const [street, setStreet] = useState("");
	const [city, setCity] = useState("");
	const [postCode, setPostCode] = useState("");
	//contact details
	const [landlineNumber, setLandlineNumber] = useState("");
	const [mobileNumber, setMobileNumber] = useState("");
	const [clubEmail, setClubEmail] = useState("");

	//CLUB REP INFO
	const [firstNameR, setFirstNameR] = useState("");
	const [lastNameR, setLastNameR] = useState("");
	const [emailR, setEmailR] = useState("");
	const [usernameR, setUsernameR] = useState("");
	const [passwordR, setPasswordR] = useState("");
	const [birthDateR, setBirthDateR] = useState("");

	const handleSubmit = async (event) => {
		event.preventDefault();

		const response = await addClub({
			name: name,
			address: {
				street_number: streetNumber,
				street: street,
				city: city,
				post_code: postCode,
			},
			contact_details: {
				landline_number: landlineNumber,
				mobile_number: mobileNumber,
				club_email: clubEmail,
			},
			club_number: clubNumber,
		});

		const response2 = await addClubRep({
			date_of_birth: birthDateR,
			user: {
				first_name: firstNameR,
				last_name: lastNameR,
				email: emailR,
				password: passwordR,
			},
			club: 4,
		});
		window.location.reload()
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
				<h2 style={{ marginTop: 10 }}>Register New Club</h2>
				<Form.Group
					controlId="formUsername"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Club Name</Form.Label>
					<Form.Control
						type="text"
						placeholder=""
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
						placeholder=""
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
						placeholder=""
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
						placeholder=""
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
						placeholder=""
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
						placeholder="BS10AB"
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
						placeholder="0759444444"
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
						placeholder="0759444444"
						value={mobileNumber}
						onChange={(event) => setMobileNumber(event.target.value)}
					/>
				</Form.Group>
				<Form.Group
					controlId="formLastName"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Email</Form.Label>
					<Form.Control
						type="email"
						placeholder="example@gmail.com"
						value={clubEmail}
						onChange={(event) => setClubEmail(event.target.value)}
					/>
				</Form.Group>
				<hr style={{ width: "100vw" }}></hr>
				<h5>Club Representative</h5>
				<Form.Group
					controlId="formUsername"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>First Name</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter first name"
						value={firstNameR}
						onChange={(event) => setFirstNameR(event.target.value)}
					/>
				</Form.Group>

				<Form.Group
					controlId="formEmail"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Last Name</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter last name"
						value={lastNameR}
						onChange={(event) => setLastNameR(event.target.value)}
					/>
				</Form.Group>

				<Form.Group
					controlId="formPassword"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Email</Form.Label>
					<Form.Control
						type="email"
						placeholder="Enter email"
						value={emailR}
						onChange={(event) => setEmailR(event.target.value)}
					/>
				</Form.Group>

				<Form.Group
					controlId="formFirstName"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Username</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter username"
						value={usernameR}
						onChange={(event) => setUsernameR(event.target.value)}
					/>
				</Form.Group>
				<Form.Group
					controlId="formFirstName"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Password</Form.Label>
					<Form.Control
						type="password"
						placeholder="Enter password"
						value={passwordR}
						onChange={(event) => setPasswordR(event.target.value)}
					/>
				</Form.Group>
				<Form.Group
					controlId="formFirstName"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>Date of Birth</Form.Label>
					<Form.Control
						type="date"
						placeholder="mm/dd/yy"
						value={birthDateR}
						onChange={(event) => setBirthDateR(event.target.value)}
					/>
				</Form.Group>
				<hr style={{ width: "100vw" }}></hr>

				<Button
					variant="primary"
					type="submit"
					style={{ marginTop: 20, width: "90%" }}
				>
					Create Club
				</Button>
			</Form>
		</div>
	);
}

export default RegisterClub;
