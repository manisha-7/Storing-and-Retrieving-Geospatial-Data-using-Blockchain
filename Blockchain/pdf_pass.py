from PyPDF2 import PdfFileReader, PdfFileWriter

from fpdf import FPDF
 
 
# save FPDF() class into a
# variable pdf
def convtpdf(username, password):
    pdf = FPDF()
    
    # Add a page
    pdf.add_page()
    
    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size = 15)
    
    # create a cell
    # pdf.cell(200, 10, txt = "Use your username to unlock the PDF!",
    #         ln = 1, align = 'C')
    
    # add another cell
    pdf.cell(200, 10, txt = str(f'Your new password is: {password} '),
            ln = 2, align = 'C')
    
    # save the pdf with name .pdf
    pdf.output("password.pdf")  

    with open("password.pdf", "rb") as in_file:
        input_pdf = PdfFileReader(in_file)

        output_pdf = PdfFileWriter()
        output_pdf.appendPagesFromReader(input_pdf)
        output_pdf.encrypt(f"{username}")

        with open("password1.pdf", "wb") as out_file:
            output_pdf.write(out_file)
        
        