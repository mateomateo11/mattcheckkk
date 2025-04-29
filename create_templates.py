import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter as report_letter
from reportlab.lib.units import inch
from reportlab.lib import colors

def create_bubble_sheet(filename, num_questions=20, title=None):
    """
    Create a bubble sheet template PDF with the specified number of questions.
    """
    c = canvas.Canvas(filename, pagesize=report_letter)
    width, height = report_letter

    # Set default title if not specified
    if title is None:
        title = f"MattChecker {num_questions}-Question Answer Sheet"

    # Draw logo (if exists)
    try:
        c.drawImage('static/img/logo.jpg', 1*inch, height - 1.3*inch, width=0.8*inch, height=0.8*inch)
    except:
        pass

    # Draw title only
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 1*inch, title)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - 1.3*inch, "Answer Sheet")

    # Draw student info section with rounded corners
    c.setFont("Helvetica-Bold", 12)
    c.roundRect(1*inch, height - 2.5*inch, width - 2*inch, 0.9*inch, 10, stroke=1, fill=0)

    # Student info with better spacing
    c.setFont("Helvetica", 11)
    name_y = height - 1.9*inch
    c.drawString(1.3*inch, name_y, "Student ID: ")
    c.drawString(2.5*inch, name_y, "_"*20)

    id_y = height - 2.2*inch
    c.drawString(1.3*inch, id_y, "Name:")
    c.drawString(2*inch, id_y, "_"*40)

    section_y = height - 1.9*inch
    c.drawString(width - 4*inch, section_y, "Section:")
    c.drawString(width - 3.3*inch, section_y, "_"*15)

    # Generate QR code with enhanced padding
    temp_qr_path = "temp_qr.png"
    qr_size = 1.2*inch  # Larger QR code
    qr_padding = 0.25*inch  # More padding
    qr_x = width - 2.8*inch  # More space from right edge
    qr_y = height - 2.6*inch  # More space from top

    # Draw white background for QR code
    c.setFillColor(colors.white)
    c.rect(qr_x - qr_padding, qr_y - qr_padding, 
           qr_size + 2*qr_padding, qr_size + 2*qr_padding, fill=1)
    c.setFillColor(colors.black)

    # Draw QR code
    c.drawImage(temp_qr_path, qr_x, qr_y, width=qr_size, height=qr_size)

    # Clean up temporary file
    #os.remove(temp_qr_path)


    # Calculate columns based on number of items
    items_per_column = 25
    num_columns = (num_questions + items_per_column - 1) // items_per_column
    column_width = (width - 2*inch) / num_columns

    # Draw answer bubbles
    start_y = height - 3.8*inch
    row_height = 0.3*inch
    bubble_spacing = 0.4*inch

    for col in range(num_columns):
        col_x = 1*inch + col * column_width

        # Draw column questions
        start_num = col * items_per_column + 1
        end_num = min((col + 1) * items_per_column, num_questions)

        for i in range(start_num, end_num + 1):
            y = start_y - ((i - start_num) * row_height)

            # Question number
            c.setFont("Helvetica-Bold", 10)
            c.drawRightString(col_x + 0.3*inch, y + 0.07*inch, f"{i}.")

            # Answer bubbles
            bubble_x = col_x + 0.5*inch
            bubble_radius = 7 if num_questions == 100 else 5
            bubble_y_offset = 0.08*inch

            for j, letter in enumerate(['A', 'B', 'C', 'D']):
                bubble_center_x = bubble_x + j * bubble_spacing
                c.circle(bubble_center_x, y + bubble_y_offset, bubble_radius, stroke=1, fill=0)
                c.setFont("Helvetica", 8)
                letter_height = 8
                vertical_offset = (bubble_radius * 2) / 2 - letter_height / 3
                c.drawCentredString(bubble_center_x, y + bubble_y_offset - vertical_offset, letter)

    c.save()
    print(f"Created {filename} with {num_questions} questions")

def main():
    output_dir = "static/templates"
    os.makedirs(output_dir, exist_ok=True)

    create_bubble_sheet(f"{output_dir}/standard_20.pdf", 20, "Standard 20-Question Answer Sheet")
    create_bubble_sheet(f"{output_dir}/extended_50.pdf", 50, "Extended 50-Question Answer Sheet")
    create_bubble_sheet(f"{output_dir}/comprehensive_100.pdf", 100, "Comprehensive 100-Question Answer Sheet")

if __name__ == "__main__":
    main()