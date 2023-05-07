import React from "react";
import { useLocation } from "react-router-dom";


function TransactionHistory() {
	const location = useLocation();

  const data = location.state?.data;
  console.log(data)

	return <div>TransactionHistory</div>;
}

export default TransactionHistory;
