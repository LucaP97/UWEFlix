import React, { useState } from "react";
import { useLocation } from "react-router-dom";

import { Form, Button } from "react-bootstrap";

function EditStudentAccount() {
	const location = useLocation();
	const data = location.state?.data.student;

	const [firstName, setFirstName] = useState(data.user.first_name);
	const [lastName, setLastName] = useState(data.user.last_name);
	
	
	const [email, setEmail] = useState(data.user.email);
    const [username, setUsername] = useState(data.user.username)
    const [password, setPassword] = useState('')
    const [birthDate, setBirthDate] = useState(data.birth_date)

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
				<h2 style={{ marginTop: 10 }}>Edit Student Account</h2>
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
					<Form.Label>Date of Birth</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter birth date"
						value={birthDate}
						onChange={(event) => setBirthDate(event.target.value)}
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
				<a href="/accounts/edit_student" style={{marginBottom: 20}}>Refresh to old data</a>
			</Form>
		</div>
	);

}

export default EditStudentAccount;
