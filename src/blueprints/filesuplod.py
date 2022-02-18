from flask import Blueprint, app, request, jsonify
import os
import subprocess
from werkzeug.utils import secure_filename
from src.constants.constfunctions import allowed_file
import PyPDF2 as pypdf

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

MIME = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword',
        'application/vnd.oasis.opendocument.text-master']

handle_files = Blueprint('handle_files',__name__,url_prefix="/api/v1/files")


@handle_files.post('multiple-files-upload')
def upload_files():
    try:
        print("In Upload API")
        # check if the post request has the file part
        size, typ = request.form['docFormat'].split('_')
        page_format = request.form['pageFormat']
        if 'files[]' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp

        files = request.files.getlist('files[]')

        num_dict = {'numbers': []}
        if False in [allowed_file(file.filename) for file in files]:
            return jsonify({"message": "check your file type", "allowed":list(ALLOWED_EXTENSIONS)}),422
        total_pages = 0
        for file in files:

            filename = secure_filename(file.filename)
            print(file.mimetype)

            if file.mimetype == "application/pdf":
                npath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(npath)
                with open(npath, 'rb') as fpath:
                    read_pdf = pypdf.PdfFileReader(fpath)
                    num_pages = read_pdf.getNumPages()
                    num_dict['numbers'].append({"filename": filename, 'pages': num_pages})
                    print("NUM DICT +++", num_dict)
                    total_pages += num_pages

            if file.mimetype == "image/jpeg" or file.mimetype == "image/png" or file.mimetype == "image/jpg":
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                if 'Total_Images' in num_dict.keys():
                    num_dict['Total_Images'] += 1
                else:
                    num_dict['Total_Images'] = 1
                total_pages += 1

            if file.mimetype in MIME:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                source = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                destination = app.config['UPLOAD_FOLDER']
                output = subprocess.run(
                    ["libreoffice", '--headless', '--convert-to', 'pdf', source, '--outdir', destination])
                print(output)
                new_dest = os.path.splitext(destination + f'/{filename}')[0] + ".pdf"
                with open(new_dest, 'rb') as fpath:
                    read_pdf = pypdf.PdfFileReader(fpath)
                    num_pages = read_pdf.getNumPages()
                    num_dict['numbers'].append({"filename": filename, 'pages': num_pages})
                    print(num_pages)
                    total_pages += num_pages
                print("On Going")
    

        # num_dict['Total_Pages'] = total_pages
        # if size == "A4" and typ.lower() == 'color':
        #     num_dict['Total_cost'] = round(A4_C(total_pages), 2)
        # if size == "A4" and typ.lower() == 'bw':
        #     num_dict['Total_cost'] = round(A4_BC(total_pages), 2)
        # if size == "A3" and typ.lower() == 'color':
        #     num_dict['Total_cost'] = round(A3_C(total_pages), 2)
        # if size == "A3" and typ.lower() == 'bw':
        #     num_dict['Total_cost'] = round(A3_BC(total_pages), 2)
        # num_dict['page_format'] = page_format
        # if success and errors:
        #     errors['message'] = 'File(s) successfully uploaded'
        #     resp = jsonify({"errors": errors, "number": num_dict})
        #     resp.status_code = 500
        #     return resp

        resp = jsonify({'message': 'Files successfully uploaded', "numbers": num_dict})
        resp.status_code = 201
        return resp
    except Exception as e:
        print(e)
        return {"message": "There was an error"}, 500
