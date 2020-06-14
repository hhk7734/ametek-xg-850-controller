from openpyxl import Workbook, load_workbook


class Xl:
    def __init__(self):
        pass

    def load_setup_data(self, file_path):
        wb = load_workbook(file_path)
        ws = wb[wb.sheetnames[0]]

        data = {}
        i = 2
        while True:
            num = ws.cell(row=i, column=1).value
            try:
                num = int(num)
            except (TypeError, ValueError) as e:
                print(e)
                break

            data[num] = [
                ws.cell(row=i, column=2).value,
                float(ws.cell(row=i, column=3).value),
                float(ws.cell(row=i, column=4).value),
                int(ws.cell(row=i, column=5).value),
            ]

            i += 1

        return data
