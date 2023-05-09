import {useLocation, useNavigate} from "react-router-dom";
import { useSelector } from "react-redux";
import Button from 'react-bootstrap/Button';



function PaymentSuccessView(){
    const location = useLocation();

	const userType = useSelector((state) => state.userType);

	const navigate = useNavigate();

    const booking_id = new URLSearchParams(location.search).get('id');
    const showingID = new URLSearchParams(location.search).get('showing_id');

    const at = new URLSearchParams(location.search).get('adult_ticket');
    const st = new URLSearchParams(location.search).get('student_ticket');
    const ct = new URLSearchParams(location.search).get('child_ticket');

    let token;
    let headers;

    if(userType === "GUEST"){
        headers = {"Content-Type": "application/json"}
    }
    else{
        token = localStorage.getItem('access_token')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${token}`
        }
    }

    const confirm = () => {        
       if(booking_id){
            if(parseInt(at) > 0){
                fetch(`http://127.0.0.1:8000/uweflix/booking/${booking_id}/items/`,{
                    method: "POST",
                    headers: headers,
                    body: JSON.stringify(
                        {
                            "showing_id": showingID,
                            "ticket_type": "A",
                            "quantity": at
                        }
                    )
                })
            }
            if(parseInt(st) > 0){
                fetch(`http://127.0.0.1:8000/uweflix/booking/${booking_id}/items/`,{
                    method: "POST",
                    headers: headers,
                    body: JSON.stringify(
                        {
                            "showing_id": showingID,
                            "ticket_type": "S",
                            "quantity": st
                        }
                    )
                })
            }
            if(parseInt(ct) > 0){
                fetch(`http://127.0.0.1:8000/uweflix/booking/${booking_id}/items/`,{
                    method: "POST",
                    headers: headers,
                    body: JSON.stringify(
                        {
                            "showing_id": showingID,
                            "ticket_type": "C",
                            "quantity": ct
                        }
                    )
                })
            }

            fetch("http://127.0.0.1:8000/uweflix/orders/",{
                method: "POST",
                headers: headers,
                body: JSON.stringify(
                    {
                        "booking_id": booking_id,
                    }
                )
            })
            .then(response => response.json())
            .then(data => console.log(`		O:${JSON.stringify(data)}`))
            .catch(error => console.error(error))
        }

        navigate(`/showings?bid=${booking_id}`)
    }
    
    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'center' }}>
                <h1>Thank you for your purchase!</h1>
            </div>
            <div style={{ display: 'flex', justifyContent: 'center' }}>
                <Button onClick={confirm} variant="primary">Primary</Button>
            </div>
        </div>
    );
    

}

export default PaymentSuccessView;
