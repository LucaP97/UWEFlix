import React, { useState } from "react";
import { useLocation } from "react-router-dom";

import { Form, Button } from "react-bootstrap";

import { addEmployee } from "./services/AccountManagerServices";

function RegisterEmployee() {


	const [firstName, setFirstName] = useState('');
	const [lastName, setLastName] = useState('');
	const [email, setEmail] = useState('');
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')

    const handleSubmit = async (event) => {
        event.preventDefault();

		//submit to server
		const response = await addEmployee({
            user: {username: username,
			password: password,
			email: email,
			first_name: firstName,
			last_name: lastName,}
			
		});
		window.location.reload()
    }

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
				<h2 style={{ marginTop: 10 }}>Register Employee Account</h2>
				<Form.Group
					controlId="formUsername"
					style={{ marginBottom: 10, width: "90%" }}
				>
					<Form.Label>First Name</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter first name"
						value={firstName}
						onChange={(event) => setFirstName(event.target.value)}
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
						value={lastName}
						onChange={(event) => setLastName(event.target.value)}
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
						value={email}
						onChange={(event) => setEmail(event.target.value)}
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
						value={username}
						onChange={(event) => setUsername(event.target.value)}
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
						value={password}
						onChange={(event) => setPassword(event.target.value)}
					/>
				</Form.Group>
                
                

				<Button
					variant="primary"
					type="submit"
					style={{ marginTop: 20, width: "90%" }}
				>
					Create Employee Account
				</Button>
				<hr style={{ width: "100%" }} />
			</Form>
		</div>
	);

}

export default RegisterEmployee;
