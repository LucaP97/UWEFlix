import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAllStatements } from "./services/AccountManagerServices";
import "./styles/statements.css";
import { Button } from "react-bootstrap";

function statementRow(props) {}

function Statements() {
	const [statements, setStatements] = useState([]);
	const navigate = useNavigate();

	useEffect(() => {
		const fetchStatements = async () => {
			const data = await getAllStatements();
			setStatements(data);
		};
		fetchStatements();
	}, []);

	const handleNavigate = (data) => {
		navigate("/statements/transactions", { state: { data } });
	};

	return (
		<div className={"list-cont"} style={{ justifyContent: "flex-start" }}>
			{statements.map((statement) => (
				<div className="row-cont">
					<h3>
						ID {statement.id} —{" "}
						{statement.name.substring(statement.name.length - 6)}{" "}
					</h3>
					<div style={{ marginLeft: "auto" }}>
						<Button
							onClick={() =>
								handleNavigate({
									uweflix_items: statement.uweflix_statement_items,
									club_items: statement.club_statement_items,
								})
							}
						>
							Transaction History
						</Button>
					</div>
				</div>
			))}
		</div>
	);
}

export default Statements;
