import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { loginUser } from "./services/UserService";
import axios from "axios";

const LoginUser = () => {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");


	const handleSubmit = async (event) => {
		event.preventDefault();

		//submit to server
		const data = await loginUser({
			username: username,
			password: password,
		});
        console.log(data)
		localStorage.clear();
		localStorage.setItem("access_token", data.access);
		localStorage.setItem("refresh_token", data.refresh);
        console.log(data.access)

		axios.defaults.headers.common["Authorization"] = `Bearer ${data["access"]}`;

		window.location.href = "/"
	};

	return (
		<div className="container">
			<h2 style={{ marginTop: 10 }}>Sign in</h2>
			<Form onSubmit={handleSubmit}>
				<Form.Group controlId="formUsername" style={{ marginBottom: 10 }}>
					<Form.Label>Username</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter username"
						value={username}
						onChange={(event) => setUsername(event.target.value)}
					/>
				</Form.Group>

				<Form.Group controlId="formPassword" style={{ marginBottom: 10 }}>
					<Form.Label>Password</Form.Label>
					<Form.Control
						type="password"
						placeholder="Enter password"
						value={password}
						onChange={(event) => setPassword(event.target.value)}
					/>
				</Form.Group>

				<Button variant="primary" type="submit" style={{ marginTop: 20 }}>
					Login
				</Button>
			</Form>
		</div>
	);
};

export default LoginUser;
