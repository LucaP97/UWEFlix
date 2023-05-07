
import { CardElement, useElements, useStripe } from "@stripe/react-stripe-js"
import React, { useState } from 'react'
import Button from 'react-bootstrap/Button';
import Booking from "../Booking";
 


//  test card :
//  2424 2424 2424 2420
//  12/34
//  123




const CARD_OPTIONS = {
	iconStyle: "solid",
	style: {
		base: {
			iconColor: "#c2c2c2",
			color: "#c2c2c2",
			fontWeight: 500,
			fontFamily: "Roboto, Open Sans, Segoe UI, sans-serif",
			fontSize: "16px",
			fontSmoothing: "antialiased",
			":-webkit-autofill": { color: "#c2c2c2" },
			"::placeholder": { color: "#c2c2c2" }
		},
		invalid: {
			iconColor: "#c2c2c2",
			color: "#000000"
		}
	}
}

export default function PaymentForm() {
    const [success, setSuccess ] = useState(false)
    const stripe = useStripe()
    const elements = useElements()

    const [name, setName] = useState('');
    const [email, setEmail] = useState('');

    const [bookingId, setBookingId] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault()


        const {error, paymentMethod} = await stripe.createPaymentMethod({
            type: "card",
            card: elements.getElement(CardElement)
        })


        if(!error) {
            try {        
                //console.log(`T: `)
                const headers = {
                    'Content-Type': 'application/json'
                }

                const {id} = paymentMethod

                fetch("http://127.0.0.1:8000/uweflix/booking/",{
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                })
                .then(response => {
                    if(!response.ok){
                        throw new Error("Booking response was not good");
                    }
                    return response.json()
                })

                .then(data => {
                    setBookingId(data.id);

                	if(Booking.adultTickets > 0){
                		fetch(`http://127.0.0.1:8000/uweflix/booking/${data.id}/items/`,{
                			method: "POST",
                			headers: headers,
                			body: JSON.stringify(
                				{
                					"showing_id": Booking.showingID,
                					"ticket_type": "A",
                					"quantity": Booking.adultTickets
                				}
                			)
                            
                		})
                		.then(response => response.json())
                		.then(data => {console.log(`T: ${JSON.stringify(data)}}`)})
                	}
                	if(Booking.studentTickets > 0){
                		fetch(`http://127.0.0.1:8000/uweflix/booking/${data.id}/items/`,{
                			method: "POST",
                			headers: headers,
                			body: JSON.stringify(
                				{
                					"showing_id": Booking.showingID,
                					"ticket_type": "S",
                					"quantity": Booking.studentTickets
                				}
                			)
                            
                		})
                		.then(response => response.json())
                		.then(data => {console.log(`T: ${JSON.stringify(data)}}`)})
                	}
                	if(Booking.childTickets > 0){
                		fetch(`http://127.0.0.1:8000/uweflix/booking/${data.id}/items/`,{
                			method: "POST",
                			headers: headers,
                			body: JSON.stringify(
                				{
                					"showing_id": Booking.showingID,
                					"ticket_type": "C",
                					"quantity": Booking.childTickets
                				}
                			)
                            
                		})
                		.then(response => response.json())
                		.then(data => {console.log(`T: ${JSON.stringify(data)}}`)})
                	}
                })

                console.log(`T: ${bookingId}`)
                // const response = await axios.post("http://127.0.0.1:8000/uweflix/orders/", {
                //     booking_id : bookingId
                // })

                fetch("http://127.0.0.1:8000/uweflix/orders/", {
                    booking_id : bookingId
                })
                .then(response => {
                    if(!response.ok){
                        throw new Error("Orders response was not good");
                    }
                    return response.json()
                })
                .then(data =>{
                    if(data.success) {
                        console.log("Successful payment")
                        setSuccess(true)
                    }
                })

            } catch (error) {
                console.log("Error", error)
            }
        } else {
            console.log(error.message)
        }
    }

    return (
        <>
        {!success ? 
        <form onSubmit={handleSubmit}>
            <fieldset className="FormGroup">
                <div className="FormRow">
                <input
                    type="text"
                    value={name}
                    placeholder="Full name"
                    onChange={(e) => setName(e.target.value)}
                />
                <input
                    type="email"
                    value={email}
                    placeholder="Email address"
                    onChange={(e) => setEmail(e.target.value)}
                />
                </div>
                <div className="FormRow">
                    <CardElement options={CARD_OPTIONS}/>
                </div>
            </fieldset>
            <div>
                <Button variant="primary" type="submit">
                    Purchase
                </Button>
            </div>
        </form>
        :
       <div>
           <h2>You just bought a sweet spatula congrats this is the best decision of you're life</h2>
       </div> 
        }
            
        </>
    )
}