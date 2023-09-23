from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
import fitz
import fitz
app = Flask(__name__)

# Define your database connection parameters
db_params = {
    "dbname": "pdf_data",  # Replace with your actual database name
    "user": "postgres",    # Replace with your actual database username
    "password": "Mannat@123",  # Replace with your actual database password
    "host": "localhost",
    "port": "5432"
}

try:
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    
    # Define the SQL statement to create the table if it doesn't exist
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS pdf_files (
        id SERIAL PRIMARY KEY,
        filename VARCHAR(255) NOT NULL,
        ocr VARCHAR(255) NOT NULL
    );
    """
    
    # Execute the SQL statement to create the table
    cursor.execute(create_table_sql)
    
    # Commit the transaction
    conn.commit()
    
    
    
    


except psycopg2.Error as e:
    print(f"Error: Unable to connect to the database or create the table - {e}")
    exit()


def convert_pdf_to_images(pdf_path, image_folder):
    pdf_document = fitz.open(pdf_path)
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image = page.get_pixmap()
        image_path = os.path.join(image_folder, f"page_{page_number + 1}.png")
        image.save(image_path)
    pdf_document.close()


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/upload', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST' and 'pdf' in request.files:
        pdf = request.files['pdf']
        if pdf:
            # Extract the filename from the uploaded file
            pdf_filename = pdf.filename
            
            # Save the PDF file to a directory (optional)
            pdf_path = os.path.join('uploads', pdf_filename)
            pdf.save(pdf_path)

            # Convert the PDF to images
            output_folder = os.path.join('uploads', 'output_images')
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            convert_pdf_to_images(pdf_path, output_folder)

            # Insert the filename into the database
            with conn.cursor() as cur:
                cur.execute("INSERT INTO pdf_files (filename) VALUES (%s)", (pdf_filename,))
                conn.commit()

            return 'PDF uploaded, converted to images, and stored successfully!'

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)





# # Define your database connection parameters
# db_params = {
#     "dbname": "pdf_data",  # Replace with your actual database name
#     "user": "postgres",    # Replace with your actual database username
#     "password": "Mannat@123",  # Replace with your actual database password
#     "host": "localhost",
#     "port": "5432"
# }

# try:
#     # Establish a connection to the PostgreSQL database
#     conn = psycopg2.connect(**db_params)
#     # Create a cursor object to execute SQL commands
#     cursor = conn.cursor()
    
#     # Define the SQL statement to create the table if it doesn't exist
#     create_table_sql = """
#     CREATE TABLE IF NOT EXISTS pdf_files (
#         id SERIAL PRIMARY KEY,
#         filename VARCHAR(255) NOT NULL,
#         ocr VARCHAR(255) NOT NULL
#     );
#     """
    
#     # Execute the SQL statement to create the table
#     cursor.execute(create_table_sql)
    
#     # Commit the transaction
#     conn.commit()
    
    
    
    


# except psycopg2.Error as e:
#     print(f"Error: Unable to connect to the database or create the table - {e}")
#     exit()







