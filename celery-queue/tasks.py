import os
from datetime import datetime
import requests
import json
from celery import Celery
import docker
#from celery.utils.log import get_task_logger

class LogFile:
    def __init__(self, session):
        self.file = open("{}/session.log".format(session), "w")
    def log(self, level, mess):
        self.file.write("{}) {} > {}\n".format(datetime.now(),level, mess))
    def __getattr__(self, level):
        return lambda mess: self.log(level.upper(), mess)
    def close(self):
        self.file.close()
    

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

docker_client = docker.DockerClient("unix:///var/run/docker.sock")


def download(url, dest, log=None):
    cmd = "wget -q -O {} {}".format(dest, url)
    if log: log.debug(f"command: {cmd}")
    os.system(cmd)

def clone_repo(url, dest, log=None):
    cmd = f"git clone {url} {dest}"
    if log: log.debug(f"Cloning repo: {url}")
    os.system(cmd)



@celery.task(name='start_job')
def start_job(user: str, session: int, conf_url: str) -> str:
    # Create the folder in the users_sessions storage
    session_basedir = "/storage/users_sessions/{}/{}".format(user, session)
    data_basedir = "/storage/datasets/{}".format(user)
    os.makedirs(session_basedir)
    os.makedirs(data_basedir, exist_ok=True)
    
    log = LogFile(session_basedir)
    # Download the conìfiguration file
    log.debug("Downloaded files...")
    download(conf_url, f"{session_basedir}/config.yaml", log)
    
    # Read the conf file
    conf = json.load(open(session_basedir+ "/config.yaml"))
    
    # Download dataset
    docker_volumes = {}
    for dataset_name, dataset_conf in conf["datasets"].items():
        dataset_basedir = f"{data_basedir}/{dataset_name}"
        os.makedirs(dataset_basedir, exist_ok=True)
        # Save volumes options for docker
        docker_volumes[dataset_basedir] = {"bind":f"/datasets/{dataset_name}", "mode":"ro"}
        baseurl = dataset_conf['baseurl']
        for file in dataset_conf["files"]:
            filepath = f"{dataset_basedir}/{file}"
            if not os.path.exists(filepath) or dataset_conf["refresh"]:
                log.info(f"Downloading file: {file}")
                download(f"{baseurl}/{file}", filepath, log)

    # Download code 
    code_basedir = f"{session_basedir}/code"
    clone_repo(conf["app"]["code"], code_basedir, log)
    docker_volumes[code_basedir] = {"bind":"/code", "mode":"rw"}

    # Create output folder
    output_basedir = f"{session_basedir}/output"
    os.makedirs(output_basedir)
    docker_volumes[output_basedir] = {"bind": f"/output", "mode":"rw"}
    
    # Create docker
    docker_image = conf["app"]["docker"]
    docker_command = conf["app"]["command"]

    options = { 
        "image":docker_image,
        "command":docker_command, 
        "volumes":docker_volumes,
        "working_dir":"/code"
    }
    if "gpu" in conf["app"] and conf["app"]["gpu"]:
        options["runtime"] = "nvidia"
    
    log.info(f"Launching docker with options: {options}")

    logs = docker_client.containers.run( **options )

    
    # Save logs on disk
    with open(f"{session_basedir}/docker.log","wb") as logs_out:
        logs_out.write(logs)

    log.info("Saved tar output")
    log.close()
    # Create tar with results
    os.system(f"cd {session_basedir};tar zcf output.tar.gz docker.log \
                        session.log output")
    

    return f"{session_basedir}/output.tar.gz"


'''
 { 
  "name" : "Test",
  "datasets" : 
        { "Full2017_v1": {
                "baseurl": "https://dmapelli.web.cern.ch/dmapelli/latinos/numpy/Full2017_v1_190920/",
                "files": ["Wjets.pkl"],
                "refresh": true
                }
        },
  "app": {
        "docker": "keras-base:0.1",
        "code" : "https://github.com/valsdav/TestTrainingConf.git",
        "command": "python test.py",
        "gpu": true
         }
        
}
'''