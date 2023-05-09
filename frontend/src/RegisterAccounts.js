import React from "react";
import { useNavigate } from "react-router-dom";

import { Button } from "react-bootstrap";

function RegisterAccounts() {
	const navigateEmployee = useNavigate();

	return (
		<div
			style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
		>
            
            <hr style={{width: '100vw'}}></hr>
			<div style={{ margin: 40 }}>
				<Button
					onClick={() => {
						navigateEmployee("/register_account/employee");
					}}
				>
					Register new employee
				</Button>
                
			</div><hr style={{width: '100vw'}}></hr>
		</div>
	);
}

export default RegisterAccounts;
