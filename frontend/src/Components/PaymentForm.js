import { API_URL } from "../config/index";

const PaymentForm = (props) =>
(
    <section>
        <form action= {`${API_URL}/uweflix/create-checkout-session`} method="POST">
            <input type="hidden" name="total_price" value={props.total_price}/>
            <input type="hidden" name="showing_id" value={props.showing_id}/>
            <input type="hidden" name="student_ticket" value={props.student_ticket}/>
            <input type="hidden" name="adult_ticket" value={props.adult_ticket}/>
            <input type="hidden" name="child_ticket" value={props.child_ticket}/>
            
            <button type="submit">
                Checkout
            </button>
        </form>
  </section>
);

export default PaymentForm