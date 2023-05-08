import React, { useEffect, useState, useCallback } from "react";
import {
	getClubAccounts,
	getEmployeeAccounts,
	getStudentAccounts,
} from "./services/AccountManagerServices";
import { Container, Form, ListGroup } from "react-bootstrap";

import { useNavigate } from "react-router-dom";
import "./styles/accounts.css";
import { chevronDown, chevronUp, pencilOutline } from "ionicons/icons";
import { IonIcon } from "@ionic/react";

function AccountList() {
	const [clubSearch, setClubSearch] = useState("");
	const [clubs, setClubs] = useState([]);
	const [fclubs, setfClubs] = useState([]);

	const [studentSearch, setStudentSearch] = useState("");
	const [students, setStudents] = useState([]);
	const [fstudents, setfStudents] = useState([]);

	const [staffSearch, setStaffSearch] = useState("");
	const [staff, setStaff] = useState([]);
	const [fstaff, setfStaff] = useState([]);

	const [clubIsCollapsed, setClubIsCollapsed] = useState(true);
	const [studentsIsCollapsed, setStudentsIsCollapsed] = useState(true);
	const [staffIsCollapsed, setStaffIsCollapsed] = useState(true);

	const navigateClub = useNavigate();
    const navigateEmployee = useNavigate()

	useEffect(() => {
		const fetchClub = async () => {
			const clubData = await getClubAccounts();
			setClubs(clubData);
			setfClubs(clubData);
		};
		const fetchStudent = async () => {
			const studentData = await getStudentAccounts();
			setStudents(studentData);
			setfStudents(studentData);
		};
		const fetchEmployee = async () => {
			const employeeData = await getEmployeeAccounts();
			setStaff(employeeData);
			setfStaff(employeeData);
		};

		fetchClub();
		fetchStudent();
		fetchEmployee();
	}, []);

	const handleClubSearchChange = (event) => {
		const query = event.target.value;
		setClubSearch(query);

		const filteredData = clubs.filter((club) => {
			return club.name.toLowerCase().includes(query.toLowerCase());
		});

		setfClubs(filteredData);
	};

	const handleStaffSearchChange = (event) => {
		const query = event.target.value;
		setStaffSearch(query);

		const filteredData = staff.filter((employee) => {
			return employee.user.username.toLowerCase().includes(query.toLowerCase());
		});

		setfStaff(filteredData);
	};

	const toggleCollapseClub = useCallback(() => {
		setClubIsCollapsed(!clubIsCollapsed);
	}, [clubIsCollapsed]);

	const toggleCollapseStudent = useCallback(() => {
		setStudentsIsCollapsed(!studentsIsCollapsed);
	}, [studentsIsCollapsed]);

	const toggleCollapseStaff = useCallback(() => {
		setStaffIsCollapsed(!staffIsCollapsed);
	}, [staffIsCollapsed]);

    const handleNavigateClub = useCallback((data) => {
		navigateClub("/accounts/edit_club", { state: { data } });
	}, [navigateClub]);

    const handleNavigateEmployee = useCallback((data) => {
		navigateEmployee("/accounts/edit_employee", { state: { data } });
	}, [navigateEmployee]);

	return (
		<div className="list">
			<div className="row-title-container" style={{ marginTop: 20 }}>
				<h3 className="acc-title">Club Accounts</h3>
				<div
					className="row-title-container"
					onClick={toggleCollapseClub}
					style={{ marginLeft: "auto", opacity: 0.7 }}
				>
					<h4 style={{}}>{clubIsCollapsed ? "unhide" : "hide"}</h4>
					<IonIcon
						icon={clubIsCollapsed ? chevronDown : chevronUp}
						color="black"
						size="large"
						style={{ marginRight: 20 }}
					/>
				</div>
			</div>
			{clubIsCollapsed ? null : (
				<div>
					<Form.Control
						type="text"
						style={{ marginLeft: 20 }}
						value={clubSearch}
						onChange={handleClubSearchChange}
						placeholder="Search..."
					/>
					{fclubs.map((club) => (
						<div className="row-container">
							<h3>{club.name} |</h3>
							<h3 style={{ opacity: 0.4 }}> {club.club_number}</h3>
							<div style={{ marginLeft: "auto" }}>
								<IonIcon
									icon={pencilOutline}
									color="black"
									size="large"
									style={{ marginRight: 20 }}
                                    onClick={() =>
                                        handleNavigateClub({
                                            club: club
                                        })
                                    }
								/>

							</div>
						</div>
					))}
				</div>
			)}

			<hr></hr>
			
			
			<div className="row-title-container" style={{ marginTop: 20 }}>
				<h3 className="acc-title">Staff Accounts</h3>
				<div
					className="row-title-container"
					onClick={toggleCollapseStaff}
					style={{ marginLeft: "auto", opacity: 0.7 }}
				>
					<h4 style={{}}>{staffIsCollapsed ? "unhide" : "hide"}</h4>
					<IonIcon
						icon={staffIsCollapsed ? chevronDown : chevronUp}
						color="black"
						size="large"
						style={{ marginRight: 20 }}
					/>
				</div>
			</div>
			{staffIsCollapsed ? null : (
				<div>
					<Form.Control
						type="text"
						style={{ marginLeft: 20 }}
						value={staffSearch}
						onChange={handleStaffSearchChange}
						placeholder="Search..."
					/>
					{fstaff.map((employee) => (
						<div className="row-container">
							<h3>{employee.user.username} |</h3>
							<h3 style={{ opacity: 0.4 }}>
								{employee.user.first_name + " " + employee.user.last_name}
							</h3>
							<div style={{ marginLeft: "auto" }}>
                            <IonIcon
									icon={pencilOutline}
									color="black"
									size="large"
									style={{ marginRight: 20 }}
                                    onClick={() =>
                                        handleNavigateEmployee({
                                            employee: employee
                                        })
                                    }
								/>
                            </div>
						</div>
					))}
				</div>
			)}

			<hr></hr>
		</div>
	);
}

export default AccountList;
