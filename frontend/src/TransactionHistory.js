import React from "react";
import { useLocation } from "react-router-dom";
import "./styles/transactionhistory.css";

function formatDate(timestamp) {
	const dateObj = new Date(timestamp);
	const year = dateObj.getFullYear();
	const month = ("0" + (dateObj.getMonth() + 1)).slice(-2);
	const day = ("0" + dateObj.getDate()).slice(-2);
	const hour = ("0" + dateObj.getHours()).slice(-2);
	const minute = ("0" + dateObj.getMinutes()).slice(-2);

	const dateStr = `${day}/${month}/${year}`;
	const timeStr = `${hour}:${minute}`;

	return `${dateStr} ${timeStr}`;
}

function TransactionHistory() {
	const location = useLocation();

	const data = location.state?.data.statement;
	console.log(data.uweflix_statement_items);

	return (
		<div className={"list-conta"}>
			<h5 style={{ marginLeft: 20, marginTop: 20 }}>
				Total revenue from all accounts this month:{"  "}
				<span style={{ color: "green" }}>{data.total}£</span>
			</h5>
			<hr></hr>
			<h3 style={{ marginLeft: 20 }}>Student and Guest Transactions</h3>
			<hr></hr>
			<h5 style={{ marginLeft: 20 }}>
				Total revenue from students and guests this month:{"  "}
				<span style={{ color: "green" }}>{data.uweflix_total}£</span>
			</h5>
			<hr></hr>
			{data.uweflix_statement_items.map((item) => (
				<div className="row-conta">
					<h5>{formatDate(item.order_object.placed_at)}</h5>
					<div style={{ marginLeft: "auto" }}>
						<h3 style={{ color: "green" }}>
							+{item.order_object.total_price}£
						</h3>
					</div>
				</div>
			))}
			<hr></hr>
			<h3 style={{ marginLeft: 20 }}>Club Transactions</h3>
			<hr></hr>
			<h5 style={{ marginLeft: 20 }}>
				Total revenue from students and guests this month:{"  "}
				<span style={{ color: "green" }}>{data.club_total}£</span>
			</h5>
			<hr></hr>
			{data.club_statement_items.map((item) => (
				<div>
          <div className="row-conta">
          <h5 style={{marginLeft: 20}}>Transactions for club: {item.account_object.account_title} </h5>
							<div style={{ marginLeft: "auto" }}>
								<h4>Current balance: <span style={{ color: "red" }}>-{item.account_object.account_balance}£</span></h4>
							</div>
						</div>
          
					<hr></hr>{item.account_object.club_order.map((orders) => (
						<div className="row-conta">
							<h5>{formatDate(orders.placed_at)}</h5>
							<div style={{ marginLeft: "auto" }}>
								<h3 style={{ color: "green" }}>+{orders.total_paid}£</h3>
							</div>
						</div>
					))}
				</div>
			))}
		</div>
	);
}

export default TransactionHistory;
