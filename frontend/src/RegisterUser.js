import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { registerUser } from "./services/UserService";

const RegisterUser = () => {
	const [username, setUsername] = useState("");
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [firstName, setFirstName] = useState("");
	const [lastName, setLastName] = useState("");

	const handleSubmit = async (event) => {
		event.preventDefault();

		//submit to server
		const response = await registerUser({
			username: username,
			password: password,
			email: email,
			first_name: firstName,
			last_name: lastName,
		});
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
			><h2 style={{ marginTop: 10 }}>Create Account</h2>
				<Form.Group controlId="formUsername" style={{ marginBottom: 10, width: "90%" }}>
					<Form.Label>Username</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter username"
						value={username}
						onChange={(event) => setUsername(event.target.value)}
					/>
				</Form.Group>

				<Form.Group controlId="formEmail" style={{ marginBottom: 10, width: "90%" }}>
					<Form.Label>Email address</Form.Label>
					<Form.Control
						type="email"
						placeholder="Enter email"
						value={email}
						onChange={(event) => setEmail(event.target.value)}
					/>
				</Form.Group>

				<Form.Group controlId="formPassword" style={{ marginBottom: 10, width: "90%" }}>
					<Form.Label>Password</Form.Label>
					<Form.Control
						type="password"
						placeholder="Enter password"
						value={password}
						onChange={(event) => setPassword(event.target.value)}
					/>
				</Form.Group>

				<Form.Group controlId="formFirstName" style={{ marginBottom: 10, width: "90%" }}>
					<Form.Label>First name</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter first name"
						value={firstName}
						onChange={(event) => setFirstName(event.target.value)}
					/>
				</Form.Group>

				<Form.Group controlId="formLastName" style={{ marginBottom: 10, width: "90%" }}>
					<Form.Label>Last name</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter last name"
						value={lastName}
						onChange={(event) => setLastName(event.target.value)}
					/>
				</Form.Group>

				<Button variant="primary" type="submit" style={{ marginTop: 20, width: "90%" }}>
					Register
				</Button>
        <hr style={{width: '100%'}} />
				<a href="/login">Already got an account? Login!</a>
			</Form>
		</div>
	);
};

export default RegisterUser;
