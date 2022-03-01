from flask import Blueprint, copy_current_request_context, request, jsonify
import os
import subprocess
import json
from werkzeug.utils import secure_filename
# from src.constants.constfunctions import 
import PyPDF2 as pypdf
import time
import threading
from flask import current_app as application
from src.constants.constfunctions import A3_BC, A3_C, A4_BC, A4_C, allowed_file

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

MIME = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword',
        'application/vnd.oasis.opendocument.text-master']

handle_files = Blueprint('handle_files',__name__,url_prefix="/api/v1/files")


@handle_files.post('multiple-files-upload')
def upload_files():
    try:
        if not os.path.exists(application.config['UPLOAD_FOLDER']):
            os.mkdir(application.config["UPLOAD_FOLDER"])
        print("In Upload API")
        fetch_file_start = time.perf_counter()
        # check if the post request has the file part
        size, typ = request.form['docFormat'].split('_')
        page_format = request.form['pageFormat']
        if 'files[]' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp

        files = request.files.getlist('files[]')
        fetch_file_end = time.perf_counter()
        print("Estimated Time Taken By Fetching files:", fetch_file_end - fetch_file_start)
        num_dict = {'numbers': []}

        check_extension_start = time.perf_counter()
        if False in [allowed_file(file.filename) for file in files]:
            return jsonify({"message": "check your file type", "allowed":list(ALLOWED_EXTENSIONS)}),422
        total_pages = 0
        print("Checking file extension as Taken time:", time.perf_counter()-check_extension_start)

        traverse_files = time.perf_counter()
        for file in files:
            
            filename = secure_filename(file.filename)
            print(file.mimetype)

            if file.mimetype == "application/pdf":
                npath = os.path.join(application.config['UPLOAD_FOLDER'], filename)
                file.save(npath)
                with open(npath, 'rb') as fpath:
                    read_pdf = pypdf.PdfFileReader(fpath)
                    num_pages = read_pdf.getNumPages()
                    num_dict['numbers'].append({"filename": filename, 'pages': num_pages})
                    print("NUM DICT +++", num_dict)
                    total_pages += num_pages

            if file.mimetype == "image/jpeg" or file.mimetype == "image/png" or file.mimetype == "image/jpg":
                file.save(os.path.join(application.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                if 'Total_Images' in num_dict.keys():
                    num_dict['Total_Images'] += 1
                else:
                    num_dict['Total_Images'] = 1
                total_pages += 1

            if file.mimetype in MIME:
                file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
                source = os.path.join(application.config['UPLOAD_FOLDER'], filename)
                destination = application.config['UPLOAD_FOLDER']
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
    
        print("Estimated Time Taken By File Traversal and Page Calculation is: ", time.perf_counter()-traverse_files)
        num_dict['Total_Pages'] = total_pages
        if size == "A4" and typ.lower() == 'color':
            num_dict['Total_cost'] = round(A4_C(total_pages), 2)
        if size == "A4" and typ.lower() == 'bw':
            num_dict['Total_cost'] = round(A4_BC(total_pages), 2)
        if size == "A3" and typ.lower() == 'color':
            num_dict['Total_cost'] = round(A3_C(total_pages), 2)
        if size == "A3" and typ.lower() == 'bw':
            num_dict['Total_cost'] = round(A3_BC(total_pages), 2)
        num_dict['page_format'] = page_format
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


@handle_files.post('/file-cart-upload')
def cart_upload():
    @copy_current_request_context
    def travers_file(final_result,files, size, typ, side):
        num_dict = {"numbers":[]}
        total_pages = 0
        for file in files:
            print(">}>}"*20, file)
            print(file.mimetype)
            filename = secure_filename(file.filename)

            if file.mimetype == "application/pdf":
                npath = os.path.join(application.config['UPLOAD_FOLDER'], filename)
                file.save(npath)
                with open(npath, 'rb') as fpath:
                    read_pdf = pypdf.PdfFileReader(fpath)
                    num_pages = read_pdf.getNumPages()
                    num_dict['numbers'].append({"filename": filename, 'pages': num_pages})
                    print("NUM DICT +++", num_dict)
                    total_pages += num_pages

            if file.mimetype == "image/jpeg" or file.mimetype == "image/png" or file.mimetype == "image/jpg":
                file.save(os.path.join(application.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                if 'Total_Images' in num_dict.keys():
                    num_dict['Total_Images'] += 1
                else:
                    num_dict['Total_Images'] = 1
                total_pages += 1

            if file.mimetype in MIME:
                file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
                source = os.path.join(application.config['UPLOAD_FOLDER'], filename)
                destination = application.config['UPLOAD_FOLDER']
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

        num_dict['Total_Pages'] = total_pages
        if size == "A4" and typ.lower() == 'color':
            num_dict['Total_cost'] = round(A4_C(total_pages), 2)
        if size == "A4" and typ.lower() == 'bw':
            num_dict['Total_cost'] = round(A4_BC(total_pages), 2)
        if size == "A3" and typ.lower() == 'color':
            num_dict['Total_cost'] = round(A3_C(total_pages), 2)
        if size == "A3" and typ.lower() == 'bw':
            num_dict['Total_cost'] = round(A3_BC(total_pages), 2)
        num_dict['page_format'] = side
        print(num_dict)
        final_result.append(num_dict)


    meta_data = json.loads(request.form.get('metadata'))['metadata']
    traverse_files = time.perf_counter()
    thread_list = []
    final_result = []
    for data in meta_data:
        num_dict = {"numbers":[]}
        size, typ = request.form[data['docFormat']].split('_')
        #TODO: check for every attributes and vaule is not null
        #TODO: fetch files and check for extension
        #TODO: Travers files and calculate page numbers and do ohter perfomantion -- done
        #TODO: calculate price and numbers and file details for current iteration and append it to global response
        files = request.files.getlist(data["files"])
        side = request.form.get(data['sides'],"")
        check_extension_start = time.perf_counter()

        if False in [allowed_file(file.filename) for file in files]:
            return jsonify({"message": "check your file type", "allowed":list(ALLOWED_EXTENSIONS)}),422
        print("Checking file extension as Taken time:", time.perf_counter()-check_extension_start)
    
        th = threading.Thread(target=travers_file, args=(final_result, files, size, typ, side))
        th.start()
        thread_list.append(th)
    
    for thread in thread_list:
        thread.join()
    end_traversal = time.perf_counter()
    print(final_result)
    print("Estimated Time Taken By File Traversal and Page Calculation is: ", end_traversal-traverse_files)
    return {"traversl_time": (end_traversal-traverse_files)}


