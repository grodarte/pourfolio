import { Formik, Form, Field, ErrorMessage } from "formik";
import { useContext } from "react";
import * as Yup from "yup";
import { SpiritContext } from "../context/SpiritContext";
import "../styles/formstyles.css";


function NewSpiritForm({ setShowSpiritForm }) {
    const { setSpirits } = useContext(SpiritContext)

    const SpiritSchema = Yup.object().shape({
        name: Yup.string().required("Spirit name required")
    })

    const initialValues = {
        name: ""
    }

    return (
        <div>
            <Formik
                initialValues={initialValues}
                validationSchema={SpiritSchema}
                onSubmit={(values, {resetForm}) => {
                    fetch(`/spirits`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(values)
                    })
                    .then(r => {
                        if (!r.ok) {
                            return r.text().then(errorText => {
                                return Promise.reject(errorText)
                            })
                        }
                        return r.json()
                    })
                    .then(newSpirit => {
                        setSpirits(prev => [...prev, newSpirit])
                        resetForm()
                        setShowSpiritForm(false)
                    })
                    .catch(errorText => {
                        console.log("Error:", errorText)
                    })

                }}
            >
                <Form>
                    <label htmlFor="name">Spirit Name</label>
                    <Field name="name" type="text"/>
                    <ErrorMessage name="name"/>
                    
                    <div className="centered-button">
                        <button type="submit">Add Spirit</button>
                    </div>
                </Form>
            </Formik>
            <div className="centered-button">
                <button onClick={() => setShowSpiritForm(false)}>Cancel</button>
            </div>
        </div>
    )
}

export default NewSpiritForm