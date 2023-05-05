import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
//import hasAccess from '../helpers/hasAccess';

import { useSelector } from "react-redux";

function NavBar() {
	const [showNav, setShowNav] = useState(false);
	const userType = useSelector((state) => state.userType);

	function handleNavToggle() {
		setShowNav(!showNav);
	}
	console.log(userType);

	return (
		<nav className="navbar navbar-expand-lg navbar-light bg-light">
			<div className="container-fluid">
				<button
					className="navbar-toggler"
					type="button"
					onClick={handleNavToggle}
				>
					<span className="navbar-toggler-icon"></span>
				</button>
				<ul className={`navbar-nav ${showNav ? "show" : ""}`}>
					{userType === "STUDENT" || userType === "GUEST" ? (
						<li className="nav-item">
							<a
								className="nav-link active"
								aria-current="page"
								href="/showings"
							>
								Showings
							</a>
						</li>
					) : (
						<></>
					)}

					{userType === "CINEMAMANAGER" ? (
						<li className="nav-item">
							<a className="nav-link" href="/film_editing">
								Edit Films
							</a>
						</li>
					) : (
						<></>
					)}
					{userType === "CINEMAMANAGER" ? (
						<li className="nav-item">
							<a className="nav-link" href="/screens">
								Screens
							</a>
						</li>
					) : (
						<></>
					)}
				</ul>
				{/* Change login to logout if user is logged in */}
				<ul className="navbar-nav">
					<li className="nav-item">
						<a
							className="nav-link"
							href={"/login"}
							style={{ fontWeight: "bold" }}
							onClick={() => {
								localStorage.clear();
							}}
						>
							{userType === "" || userType === "GUEST" ? "Login" : "Logout"}
						</a>
					</li>
					{userType === "" || userType === "GUEST" ? (
						<ul className="navbar-nav">
							<li className="nav-item">
								<a
									className="nav-link"
									href="/register"
									style={{ fontWeight: "bold" }}
								>
									Register
								</a>
							</li>
						</ul>
					) : (
						<></>
					)}
				</ul>
			</div>
		</nav>
	);
}

export default NavBar;
