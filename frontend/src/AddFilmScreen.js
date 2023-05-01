import React, { useState } from "react";
import "./styles/addfilm.css";
import { Form, Button } from "react-bootstrap";

import {addFIlm} from "./services/FilmService";


const ageRatings = ["3", "12", "15", "18"];

function AddFilmScreen() {
	const [title, setTitle] = useState("");
	const [ageRating, setAgeRating] = useState("");
	const [duration, setDuration] = useState("");
	const [shortTrailerDescription, setShortTrailerDescription] = useState("");
	const [imageUri, setImageUri] = useState("");

	const handleSubmit = async (event) => {
		event.preventDefault();

        //submit to server
		const data = await addFIlm({
			title: setTitle,
			age_rating: ageRating,
            duration: duration,
            short_trailer_description: shortTrailerDescription,
            image_uri: imageUri
		});
        console.log(data)

    }

    return (

		//submit to server
		<div className="container">
			<h2 style={{ marginTop: 10 }}>Add a new film</h2>
			<Form onSubmit={handleSubmit}>
				<Form.Group controlId="formUsername" style={{ marginBottom: 10 }}>
					<Form.Label>Title</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter title"
						value={title}
						onChange={(event) => setTitle(event.target.value)}
					/>
				</Form.Group>

				<Form.Group controlId="formAgeRating" style={{ marginBottom: 10 }}>
					<Form.Label>Age Rating</Form.Label>
					<Form.Select
						value={ageRating}
						onChange={(event) => setAgeRating(event.target.value)}
					>
						{ageRatings.map((rating, index) => (
							<option key={index} value={rating}>
								{rating}
							</option>
						))}
					</Form.Select>
				</Form.Group>

				<Form.Group controlId="formDuration" style={{ marginBottom: 10 }}>
					<Form.Label>Duration</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter film duration"
						value={duration}
						onChange={(event) => setDuration(event.target.value)}
					/>
				</Form.Group>

				<Form.Group controlId="formdescription" style={{ marginBottom: 10 }}>
					<Form.Label>Description</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter a short trailer description"
						value={shortTrailerDescription}
						onChange={(event) => setShortTrailerDescription(event.target.value)}
					/>
				</Form.Group>

				<Form.Group controlId="formLastName">
					<Form.Label>Image URI</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter image uri"
						value={imageUri}
						onChange={(event) => setImageUri(event.target.value)}
					/>
				</Form.Group>

				<Button variant="primary" type="submit" style={{ marginTop: 20 }}>
					Add Film
				</Button>
			</Form>
		</div>
    )

	
}

export default AddFilmScreen;
