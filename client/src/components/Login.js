import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup"
import { useContext } from "react";
import { UserContext } from "../context/UserContext";
import { NavLink, useNavigate } from "react-router-dom";
import "../styles/auth.css";

function Login() {
    const { setUser, setUserSpirits, setLoggedIn } = useContext(UserContext)
    const navigate = useNavigate()

    const LoginSchema = Yup.object().shape({
        username: Yup.string().required("Username required"),
        password: Yup.string().required("Password required")
    })

    const initialValues = {
        username: "",
        password: ""
    }

    return (
        <div className="auth-container">
            <h1 onClick={() => navigate("/")}>pourfolio</h1>
            <br/>
            <Formik
                initialValues={initialValues}
                validationSchema={LoginSchema}
                onSubmit={(values, {resetForm}) => {
                    fetch(`/login`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(values)
                    })
                    .then(r => {
                        if (!r.ok) throw new Error('Invalid username or password')
                            // don't want to error out on invalid username/password - add proper error messaging
                        return r.json()
                    })
                    .then(userData => {
                        setUser({
                            id: userData.id,
                            username: userData.username
                        })
                        setUserSpirits(userData.spirits)
                        setLoggedIn(true)
                        navigate("/")
                        resetForm()
                    })
                }}
            >
                <Form className="auth-form">
                    <label htmlFor="username">Username</label>
                    <Field name="username" type="text"/>
                    <ErrorMessage name="username" component="div" className="error"/>

                    <label htmlFor="password">Password</label>
                    <Field name="password" type="password"/>
                    <ErrorMessage name="password" component="div" className="error"/>

                    <button type="submit">Log In</button>
                </Form>
            </Formik>
        <p>
            Don't have an account? {" "}
            <NavLink to="/signup">Sign up</NavLink>
        </p>
        </div>
    )
}

export default Login