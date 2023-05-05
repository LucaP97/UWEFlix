import React, { useState } from "react";
import "./styles/addfilm.css";
import { Form, Button } from "react-bootstrap";

import { addFilm, addFilmImage } from "./services/FilmService";

const ageRatings = ["3", "12", "15", "18"];

function AddFilmScreen() {
	const [title, setTitle] = useState("");
	const [ageRating, setAgeRating] = useState("3");
	const [duration, setDuration] = useState("");
	const [shortTrailerDescription, setShortTrailerDescription] = useState("");
	const [imageUri, setImageUri] = useState("");
	const [selectedFile, setSelectedFile] = useState(null);

	const handleSubmit = async (event) => {
		event.preventDefault();

		//submit to server
		const data = await addFilm({
			title: title,
			age_rating: parseInt(ageRating),
			duration: duration,
			short_trailer_description: shortTrailerDescription,
			image_uri: imageUri,
		});

		const response = await addFilmImage(
			{
				image: selectedFile,
			},
			data.id
		);
		console.log(response)
	};

	return (
		//submit to server
		<div className="container">
			<h2 style={{ marginTop: 10 }}>Add a new film</h2>
			<Form onSubmit={handleSubmit} enctype="multipart/form-data">
				<Form.Group controlId="formTitle" style={{ marginBottom: 10 }}>
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
					<Form.Control
						as="select"
						value={ageRating}
						onChange={(event) => setAgeRating(event.target.value)}
					>
						{ageRatings.map((rating, index) => (
							<option key={index} value={rating}>
								{rating}
							</option>
						))}
					</Form.Control>
				</Form.Group>

				<Form.Group controlId="formDuration" style={{ marginBottom: 10 }}>
					<Form.Label>Duration</Form.Label>
					<Form.Control
						type="number"
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

				<Form.Group controlId="formImageURI">
					<Form.Label>Image URI</Form.Label>
					<Form.Control
						type="text"
						placeholder="Enter image uri"
						value={imageUri}
						onChange={(event) => setImageUri(event.target.value)}
					/>
				</Form.Group>
				<Form.Group controlId="formImage">
					<Form.Label>Image</Form.Label>
					<Form.Control
						type="file"
						
						onChange={(event) => {
							setSelectedFile(event.target.files[0]);
						}}
					/>
				</Form.Group>

				<Button variant="primary" type="submit" style={{ marginTop: 20 }}>
					Add Film
				</Button>
			</Form>
		</div>
	);
}

export default AddFilmScreen;
