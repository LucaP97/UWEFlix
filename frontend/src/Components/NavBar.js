import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
//import hasAccess from '../helpers/hasAccess';

import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

import { useSelector } from "react-redux";

function NavBar() {
	const [showNav, setShowNav] = useState(false);
	const userType = useSelector((state) => state.userType);

	function handleNavToggle() {
		setShowNav(!showNav);
	}
	console.log(userType);

	return (
		<>
		<Navbar collapseOnSelect expand="lg" bg="light" variant="light">
			<div>
				<Navbar.Brand href="/login">UWEFlix</Navbar.Brand>
				<Navbar.Collapse id="responsive-navbar-nav">
				<Nav className="me-auto">
					{userType === "STUDENT" ||
					userType === "GUEST" ||
					userType === "CLUBREP" ? (
						<Nav.Link href="/showings">Showings</Nav.Link>
					) : (
						<></>
					)}

					{userType === "CINEMAMANAGER" ? (
						<Nav.Link href="/film_editing">Edit Film</Nav.Link>
					) : (
						<></>
					)}

					{userType === "ACCOUNTMANAGER" ? (
						<Nav.Link href="/statements">Statement</Nav.Link>
					) : (
						<></>
					)}

					{userType === "ACCOUNTMANAGER" ? (
						<Nav.Link href="/accounts">Accounts</Nav.Link>
					) : (
						<></>
					)}

					{userType === "ACCOUNTMANAGER" ? (						
						<Nav.Link  href="/register_account">Accounts</Nav.Link>
					) : (
						<></>
					)}

					{userType === "CINEMAMANAGER" ? (
						<Nav.Link  href="/add_showings">Add Showings</Nav.Link>
					) : (
						<></>
					)}

					{userType === "CINEMAMANAGER" ? (
						<Nav.Link  href="/screens">Screens</Nav.Link>
					) : (
						<></>
					)}
	 				{userType === "CINEMAMANAGER" ? (						
						<Nav.Link  href="/register_account/club">Register Club</Nav.Link>
					) : (
						<></>
					)}
	 				{userType === "CINEMAMANAGER" ? (
						<Nav.Link href="/discount_approval">Discount Requests</Nav.Link>
					) : (
						<></>
					)}
					{userType === "CLUBREP" ? (
						<Nav.Link href="/discount_request">Discount</Nav.Link>
					) : (
						<></>
					)}
				</Nav>
			
				<Nav>

					 <Nav.Link href={"/login"} onClick={() => {
						localStorage.clear();
						}}
						>{userType === "" || userType === "GUEST" ? "Login" : "Logout"}
					</Nav.Link>
					{userType === "" || userType === "GUEST" ? (
						<Nav.Link href="/register">Register</Nav.Link>
					) : (
						<></>
					)}
				</Nav>
				</Navbar.Collapse>
			</div>
			
			<Navbar.Toggle aria-controls="responsive-navbar-nav" />
		</Navbar>
		</>
	);
}

export default NavBar;
