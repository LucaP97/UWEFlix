import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { loginUser } from "./services/UserService";
import axios from "axios";

import store from "./store";
import {
	getAccountManager,
	getClubAccounts,
	getCinemaManager,
	getStudent,
} from "./services/LoginPermissionService";

const LoginUser = () => {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");

	const getUserType = async () => {
		//ACCOUNT MANAGER?
		const accountmanager = await getAccountManager();
		if (accountmanager) {
			return "ACCOUNTMANAGER";
		}

		//CLUB REP?
		const clubrep = await getClubAccounts();
		if (clubrep) {
			return "CLUBREP";
		}

		//cinema man?
		const cinemamanager = await getCinemaManager();
		if (cinemamanager) {
			return "CINEMAMANAGER";
		}

		//student?
		const student = await getStudent();
		if (student) {
			return "STUDENT";
		}

		return "GUEST";
	};

	const handleSubmit = async (event) => {
		event.preventDefault();

		//submit to server
		const data = await loginUser({
			username: username,
			password: password,
		});
		console.log(data);
		localStorage.clear();
		localStorage.setItem("access_token", data.access);
		localStorage.setItem("refresh_token", data.refresh);

		axios.defaults.headers.common["Authorization"] = `Bearer ${data["access"]}`;

		const userType = await getUserType();
		localStorage.setItem("user_type", userType);
		store.dispatch({ type: userType });

		if (userType === "STUDENT" || userType === "GUEST") {
			window.location.href = "/showings";
		}
		if (userType === "CINEMAMANAGER") {
			window.location.href = "/film_editing";
		}
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
				<h2 style={{ marginTop: 10 }}>Sign in</h2>
				<Form.Group
					controlId="formUsername"
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
					controlId="formPassword"
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
					Login
				</Button>
				<Button
					variant="success"
					onClick={() => {
						localStorage.setItem("user_type", "GUEST");
						store.dispatch({ type: "GUEST" });
						window.location.href = "/showings";
					}}
					style={{ marginTop: 20, width: "90%" }}
				>
					Continue as Guest
				</Button>

				<hr style={{ width: "100%" }} />
				<a href="/register">Create a new Account</a>
			</Form>
		</div>
	);
};

export default LoginUser;
