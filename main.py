import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

def generate_report_cards(file_path):
    try:
        # Load the data from the Excel file
        data = pd.read_excel(file_path)

        # Check for missing columns
        required_columns = {'Student ID', 'Name', 'Subject Score'}
        if not required_columns.issubset(data.columns):
            raise ValueError(f"Missing required columns: {required_columns - set(data.columns)}")

        # Handle missing or invalid data
        if data.isnull().any().any():
            raise ValueError("The dataset contains missing values. Please clean the data before proceeding.")

        # Group by Student ID and Name, calculate total and average scores
        grouped = data.groupby(['Student ID', 'Name'])['Subject Score']
        summary = grouped.agg(Total='sum', Average='mean').reset_index()

        # Generate PDF report cards for each student
        for _, row in summary.iterrows():
            student_id = row['Student ID']
            name = row['Name']
            total_score = row['Total']
            average_score = row['Average']

            # Filter subject-wise scores for the student
            student_data = data[data['Student ID'] == student_id]

            # Create the PDF report
            file_name = f"report_card_{student_id}.pdf"
            pdf = SimpleDocTemplate(file_name, pagesize=letter)

            # Styles and elements for the PDF
            styles = getSampleStyleSheet()
            elements = []

            # Title and student details
            elements.append(Paragraph(f"Report Card", styles['Title']))
            elements.append(Paragraph(f"Name: {name}", styles['Normal']))
            elements.append(Paragraph(f"Total Score: {total_score}", styles['Normal']))
            elements.append(Paragraph(f"Average Score: {average_score:.2f}", styles['Normal']))

            # Table of subject scores
            table_data = [['Subject', 'Score']]
            table_data += [[row.Subject, row['Subject Score']] for _, row in student_data.iterrows()]
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)

            # Build the PDF
            pdf.build(elements)

        print("Report cards generated successfully.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
file_path = 'student_scores.xlsx'
generate_report_cards(file_path)
