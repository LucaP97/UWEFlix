import React, { useEffect, useState } from "react";
import jwt from "jsonwebtoken";

const hasAccess = (WrappedComponent, accessLevels) => {
	const HasAccess = (props) => {
		const [access, setAccess] = useState(null);
		useEffect(() => {
			const token = localStorage.getItem("token");
			const decodedToken = jwt.decode(token);
			setAccess(decodedToken.access_level);
			console.log('hey')
		}, []);

		if (accessLevels.includes(access)) {
			return <WrappedComponent {...props} />;
		} else {
			return null;
		}
	};
	return HasAccess
};

export default hasAccess;
