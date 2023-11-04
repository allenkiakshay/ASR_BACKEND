from flask import Flask ,request,send_from_directory,send_file,Blueprint,current_app
import os
from werkzeug.utils import secure_filename
import shutil
import subprocess
from flask import Flask
from celery import Celery
from celery import uuid

asr_bp = Blueprint("Asr",__name__)
simple_app = Celery('simple_worker', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@asr_bp.route('/transcript',methods=["POST","GET"])
def call_method():
    current_app.logger.info("Invoking Method ")

    if request.method=="POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        filename_without_ext=os.path.splitext(filename)[0]
        source_lang = request.form.get('source_language','English')
        print(source_lang)

        isExist = os.path.exists("./uploads")
        if(isExist==False):
            os.makedirs("./uploads")
            
        folder_for_each_video="./uploads/"+filename_without_ext
        folder_for_each_video = folder_for_each_video.replace(' ','')
        folder_for_each_video = folder_for_each_video.replace('_','')
        isExist = os.path.exists(folder_for_each_video)
        if(isExist==False):
            os.makedirs(folder_for_each_video)
        
        file.save(os.path.join(folder_for_each_video+"/", filename))
        r = simple_app.send_task('tasks.longtime_add', kwargs={'folder_for_each_video':folder_for_each_video,'filename_without_ext':filename_without_ext,'filename':filename, 'source_lang':source_lang})
        current_app.logger.info(r.backend)
        return r.id
    else:
        return "get"


@asr_bp.route('/transcript/<task_id>')
def get_status(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)
    print("Invoking Method ")
    return str(status.state)


@asr_bp.route('/transcript/<task_id>/result')
def task_result(task_id):
    result = simple_app.AsyncResult(task_id).result
    return  str(result)

####################################################################                Translation                 ####################################################################




@asr_bp.route('/translation',methods=["POST","GET"])
def call_method2():
    current_app.logger.info("Invoking Method ")


    if request.method=="POST":
        task_id = uuid()
        source_lang=request.headers.get('source_language', 'english')
        destination_lang=request.headers.get('destination_language', 'hindi')
        file = request.files['file']
        filename = secure_filename(file.filename)
        filename_without_ext=os.path.splitext(filename)[0]
        
        isExist = os.path.exists("./uploads")
        if(isExist==False):
            os.makedirs("./uploads")
            
        folder_for_each_video="./uploads/"+filename_without_ext
        folder_for_each_video1="uploads/"+filename_without_ext
        folder_for_each_video = folder_for_each_video.replace(' ','')
        folder_for_each_video = folder_for_each_video.replace('_','')
        folder_for_each_video1 = folder_for_each_video1.replace(' ','')
        folder_for_each_video1 = folder_for_each_video1.replace('_','')
        isExist = os.path.exists(folder_for_each_video)
        if(isExist==False):
            os.makedirs(folder_for_each_video)
        
        file.save(os.path.join(folder_for_each_video+"/", filename))
        
        r = simple_app.send_task('tasks.getTranslation', kwargs={'folder_for_each_video':folder_for_each_video,'folder_for_each_video1':folder_for_each_video1,'filename':filename,'source_lang':source_lang,'destination_lang':destination_lang},task_id=task_id)
        current_app.logger.info(r.backend)
        return r.id
    else:
        return "get"




@asr_bp.route('/translation/<task_id>')
def get_status2(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)
    print("Invoking Method ")
    return str(status.state)


@asr_bp.route('/translation/<task_id>/result')
def task_result2(task_id):
    result = simple_app.AsyncResult(task_id).result
    return  str(result)





###############################################################          TTS                ##########################################################################





@asr_bp.route('/TTS',methods=["POST","GET"])
def call_method3():
    current_app.logger.info("Invoking Method ")


    if request.method=="POST":
        task_id = uuid()
        output_lang=request.headers.get('output_language', 'Hindi Male')
        file = request.files['file']
        filename = secure_filename(file.filename)
        filename_without_ext=os.path.splitext(filename)[0]
        
        isExist = os.path.exists("./uploads")
        if(isExist==False):
            os.makedirs("./uploads")
            
        folder_for_each_video="./uploads/"+filename_without_ext
        folder_for_each_video = folder_for_each_video.replace(' ','')
        folder_for_each_video = folder_for_each_video.replace('_','')
        isExist = os.path.exists(folder_for_each_video)
        if(isExist==False):
            os.makedirs(folder_for_each_video)
        
        file.save(os.path.join(folder_for_each_video+"/", filename))
        folder_for_each_video=os.path.abspath(folder_for_each_video) 
        r = simple_app.send_task('tasks.getTTS', kwargs={'folder_for_each_video':folder_for_each_video,'filename':filename,'output_lang':output_lang},task_id=task_id)
        current_app.logger.info(r.backend)
        return r.id
    else:
        return "get"




@asr_bp.route('/TTS/<task_id>')
def get_status3(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)
    print("Invoking Method ")
    return str(status.state)


@asr_bp.route('/TTS/<task_id>/result')
def task_result3(task_id):
    result = simple_app.AsyncResult(task_id).result
    return send_file(str(result), mimetype='audio/mp3')


@asr_bp.route('/tempDownload')
def download_file():
    file_path = "/home/IITMDADMIN/Asr_Backend/asr_backend/uploads/7971e1c3-6f96-470f-9b28-116caa5d3828/audio.zip"
    file_path= os.path.abspath(file_path)
    return send_file(file_path, as_attachment=True)
