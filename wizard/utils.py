import xlsxwriter
from io import BytesIO

def generate_html_string(data):
    student = data['student']
    results = data['results']

    rows = "".join(
        f"""
        <tr>
            <td style="padding: 12px; border: 1px solid #e0e0e0; color: #212121;">{result['course'].name}</td>
            <td style="padding: 12px; border: 1px solid #e0e0e0; color: #212121;">{result['marks']}</td>
            <td style="padding: 12px; border: 1px solid #e0e0e0; color: #212121;">{result['grade']}</td>
            <td style="padding: 12px; border: 1px solid #e0e0e0; color: #212121;">{result['result_date']}</td>
        </tr>
        """
        for result in results
    )

    html = f"""
    <div class="table-container border p-3" style="margin: 20px 0; font-family: 'Roboto', sans-serif; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-radius: 8px;">
        <h3 style="color: #3f51b5; margin-bottom: 20px;">Student Results</h3>
        <p><strong style="color: #757575;">Student Name:</strong> <span style="color: #212121;">{student.name}</span></p>
        <p><strong style="color: #757575;">Student ID:</strong> <span style="color: #212121;">{student.id}</span></p>

        <table class="table" style="width: 100%; border-collapse: collapse; text-align: left; background-color: #fafafa; overflow: hidden; border-radius: 8px;">
            <thead style="background-color: #3f51b5; color: #ffffff;">
                <tr>
                    <th style="padding: 12px; text-align: left;">Course</th>
                    <th style="padding: 12px; text-align: left;">Marks</th>
                    <th style="padding: 12px; text-align: left;">Grade</th>
                    <th style="padding: 12px; text-align: left;">Result Date</th>
                </tr>
            </thead>
            <tbody>
            {rows}
            </tbody>
        </table>
    </div>
    """
    return html



def generate_excel_file(data):
    student = data['student']
    results = data['results']

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})

    worksheet.write('A1', 'Student Name', bold)
    worksheet.write('B1', student.name)

    worksheet.write('A2', 'Student ID', bold)
    worksheet.write('B2', student.id)

    worksheet.write('A4', 'Course', bold)
    worksheet.write('B4', 'Marks', bold)
    worksheet.write('C4', 'Grade', bold)
    worksheet.write('D4', 'Result Date', bold)

    row = 5
    for result in results:
        worksheet.write(row, 0, result['course'].name)
        worksheet.write(row, 1, result['marks'])
        worksheet.write(row, 2, result['grade'])
        worksheet.write(row, 3, result['result_date'].strftime('%d-%m-%Y'))
        row += 1

    workbook.close()

    output.seek(0)
    return output.read()