import xlsxwriter
from io import BytesIO
import tempfile
import base64

GET_TEACHERS_NAME = lambda course: ', '.join([teacher.name for teacher in course.teacher_ids])

def generate_html_string(data):
    student = data['student']
    results = data['results']

    rows = "".join(
        f"""
        <tr>
            <td style="padding: 12px; border: 1px solid #e0e0e0; color: #212121;">{result['course'].name}</td>
            <td style="padding: 12px; border: 1px solid #e0e0e0; color: #212121;">{GET_TEACHERS_NAME(result['course'])}</td>
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
                    <th style="padding: 12px; text-align: left;">Faculty Name</th>
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
    COL_OFFSET = 1
    ROW_OFFSET = 1
    PALLETE = ['#22223b', '#4a4e69', '#9a8c98', '#c9ada7', '#f2e9e4']
    student = data['student']
    results = data['results']

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    common_styles_config = {
        'align': 'center',
        'valign': 'vcenter',
        'font_name': 'Montserrat',
        'border': 1,
        'border_color': '#4a4e69',
        'color': PALLETE[1],
    }
    school_info_style_config = {
        **common_styles_config,
        'bold': True,
        'font_size': 20,
        'border': 0,
        'bg_color': PALLETE[-1],
        'color': PALLETE[0],
    }
    header_style_config = {
        **common_styles_config,
        'bold': True,
        'font_color': PALLETE[-1],
        'bg_color': PALLETE[1],
    }
    cell_style_config = {
        **common_styles_config,
    }
    spanning_cell_style_config = {
        **common_styles_config,
        'bold': True,
        'bg_color': PALLETE[-1],
    }
    student_info_style_config = {
        **common_styles_config,
        'bold': True,
        'italic': True,
        'bg_color': PALLETE[2],
        'align': 'left',
        'indent': 1,
        'color': PALLETE[-1],
    }

    header_style = workbook.add_format(header_style_config)
    cell_style = workbook.add_format(cell_style_config)
    date_cell_style = workbook.add_format({**cell_style_config, 'num_format': 'dd/mm/yyyy'})
    spanning_cell_style = workbook.add_format(spanning_cell_style_config)
    student_info_style = workbook.add_format(student_info_style_config)


    # if student.school_id:
    #     logo_data = base64.b64decode(student.school_id.logo)
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_logo_file:
    #         temp_logo_file.write(logo_data)
    #         file_path = temp_logo_file.name
    #         worksheet.insert_image('B2', file_path, {
    #             'x_scale': 0.1,  # Scale the image down (50%)
    #             'y_scale': 0.1,
    #         })

    def insert_school_info(worksheet):
        worksheet.merge_range(f"A1:F1", student.school_id.name, workbook.add_format(school_info_style_config))
        worksheet.merge_range(f"A2:F2", 'Student Report', workbook.add_format(
            {**school_info_style_config, 'font_size': 15, 'color': PALLETE[1]}
        ))
        worksheet.set_row(0, 30)
        worksheet.set_row(1, 30)

    def insert_student_info(worksheet):
        worksheet.write(2, 0, 'Student Name:', header_style)
        worksheet.merge_range(f"B3:F3", student.name, student_info_style)
        worksheet.write(3, 0, 'Student ID:', header_style)
        worksheet.merge_range(f"B4:F4", student.id, student_info_style)
        worksheet.write(4, 0, 'Standard:', header_style)
        worksheet.merge_range(f"B5:F5", student.standard, student_info_style)
        worksheet.set_column('A:A', 20)
        worksheet.merge_range(f"A6:A{len(results)+6}", "Results", spanning_cell_style)

    insert_school_info(worksheet)
    insert_student_info(worksheet)
    header_data = ['Course', 'Faculty Name', 'Marks', 'Grade', 'Result Date']
    for col, header in enumerate(header_data):
        worksheet.write(4+ROW_OFFSET, col+COL_OFFSET, header, header_style)
    for result_row, result in enumerate(results, start=5):
        worksheet.write(result_row+ROW_OFFSET, 0+COL_OFFSET, result['course'].name, cell_style)
        worksheet.write(result_row+ROW_OFFSET, 1+COL_OFFSET, GET_TEACHERS_NAME(result['course']), cell_style)
        worksheet.write(result_row+ROW_OFFSET, 2+COL_OFFSET, result['marks'], cell_style)
        worksheet.write(result_row+ROW_OFFSET, 3+COL_OFFSET, result['grade'].upper(), cell_style)
        worksheet.write(result_row+ROW_OFFSET, 4+COL_OFFSET, result['result_date'], date_cell_style)
    worksheet.set_column('B:B', 25)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 15)
    worksheet.set_column('E:E', 15)
    worksheet.set_column('F:F', 15)
    workbook.close()
    output.seek(0)
    return output.read()