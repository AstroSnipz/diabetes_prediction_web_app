import streamlit as st
import numpy as np
import pickle
from reportlab.pdfgen import canvas
import base64
from io import BytesIO

# Loading the saved model
loaded_model = pickle.load(open('7th sem mini project/diabetes/trained_model.sav', 'rb'))

# Creating a function for Prediction
def diabetes_prediction(input_data):
    # Changing the input_data to a numpy array
    input_data_as_numpy_array = np.asarray(input_data)
    # Reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshaped)
    if prediction[0] == 0:
        return 'not diabetic'
    else:
        return 'diabetic'

def generate_pdf_report(patient_info, diagnosis):
    pdf = BytesIO()
    pdf_filename = "diabetes_test_report.pdf"

    # Create a PDF file
    pdf_file = canvas.Canvas(pdf)
    pdf_file.setTitle("Diabetes Test Report")

    # Adding patient information and diagnosis to the PDF
    pdf_file.drawString(50, 800, "Diabetes Test Report")
    pdf_file.drawString(50, 780, f"Number of Pregnancies: {patient_info['pregnancies']}")
    pdf_file.drawString(50, 760, f"Glucose Level: {patient_info['glucose']}")
    pdf_file.drawString(50, 740, f"Blood Pressure value: {patient_info['blood_pressure']}")
    pdf_file.drawString(50, 720, f"Skin Thickness value: {patient_info['skin_thickness']}")
    pdf_file.drawString(50, 700, f"Insulin Level: {patient_info['insulin']}")
    pdf_file.drawString(50, 680, f"BMI value: {patient_info['bmi']}")
    pdf_file.drawString(50, 660, f"Diabetes Pedigree Function value: {patient_info['pedigree_function']}")
    pdf_file.drawString(50, 640, f"Age of the Person: {patient_info['age']}")
    pdf_file.drawString(50, 620, f"Diagnosis: {diagnosis}")

    # Close the PDF file
    pdf_file.save()

    return pdf, pdf_filename

def main():
    # Set up page layout
    st.set_page_config(
        page_title='Diabetes Prediction Web App',
        page_icon=':heart:',
    )

    # Add title and image with fade-in animation
    st.title('Diabetes Prediction Web App')

    # Add an image
    st.image('diabetes/images/img1.jpg', caption='Your Image Caption', use_column_width=True)

    # Getting the input data from the user with fade-in animation
    st.subheader('Enter Patient Information:')
    with st.form(key='diabetes_form'):
        # Add hover effect to each field
        Pregnancies = st.text_input('Number of Pregnancies', key='pregnancies', help="Enter the number of pregnancies")
        Glucose = st.text_input('Glucose Level', key='glucose', help="Enter the glucose level")
        BloodPressure = st.text_input('Blood Pressure value', key='blood_pressure', help="Enter the blood pressure value")
        SkinThickness = st.text_input('Skin Thickness value', key='skin_thickness', help="Enter the skin thickness value")
        Insulin = st.text_input('Insulin Level', key='insulin', help="Enter the insulin level")
        BMI = st.text_input('BMI value', key='bmi', help="Enter the BMI value")
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value', key='pedigree_function', 
                                                help="Enter the diabetes pedigree function value")
        Age = st.text_input('Age of the Person', key='age', help="Enter the age of the person")

        # Code for Prediction
        diagnosis = ''
        
        # Creating a button for Prediction
        if st.form_submit_button('Diabetes Test Result'):
            diagnosis = diabetes_prediction([Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age])

    # Display result with fade-in animation
    st.subheader('Diabetes Test Result:')
    result_placeholder = st.empty()
    result_placeholder.markdown(f'<div class="result animated">{diagnosis}</div>', unsafe_allow_html=True)

    # Add download button for PDF report
    if st.button('Generate PDF Report'):
        patient_info = {
            'pregnancies': Pregnancies,
            'glucose': Glucose,
            'blood_pressure': BloodPressure,
            'skin_thickness': SkinThickness,
            'insulin': Insulin,
            'bmi': BMI,
            'pedigree_function': DiabetesPedigreeFunction,
            'age': Age
        }
        pdf, pdf_filename = generate_pdf_report(patient_info, diagnosis)

        # Display the PDF
        st.subheader('Generated PDF Report:')
        pdf_base64 = base64.b64encode(pdf.getvalue()).decode('utf-8')
        st.markdown(f'<a href="data:application/pdf;base64,{pdf_base64}" download="{pdf_filename}">Download Diabetes Test Report (PDF)</a>', 
                    unsafe_allow_html=True)

    # Apply additional styles and animations using CSS
    st.markdown(
        """
        <style>
            /* Add your custom styles here */
            body {
                background-color: #f5f5f5;
                color: #333;
            }
            .title {
                color: #4285f4;
                text-align: center;
                font-size: 36px;
                padding: 20px 0;
            }
            .input-label {
                font-size: 18px;
            }
            .result {
                font-size: 24px;
            }
            .footer {
                background-color: #4285f4;
                color: #fff;
                text-align: center;
                padding: 10px;
                margin-top: 30px;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            .animated {
                animation: fadeIn 2s;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add information about diabetes at the bottom
    st.markdown("<h2 class='footer animated'>Learn more about diabetes:</h2>", unsafe_allow_html=True)
    st.markdown("<p class='footer animated'>Diabetes is a chronic condition that affects the way your body processes blood sugar (glucose). " 
                "There are different types of diabetes, including Type 1 and Type 2. It's important to manage diabetes through a healthy lifestyle, "
                "medication, and regular check-ups. Consult with your healthcare provider for personalized advice.</p>",
                unsafe_allow_html=True)

if __name__ == '__main__':
    main()
