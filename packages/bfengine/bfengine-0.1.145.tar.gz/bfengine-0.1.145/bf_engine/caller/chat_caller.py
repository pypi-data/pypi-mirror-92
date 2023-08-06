import requests

from .base import CallerBase
from ..config import Config
from ..entity.enums import ChatModel
from ..entity.enums import ChatConfig
from ..entity.enums import ChatType
from ..entity.exception import BfEngineException

class ChatCaller(CallerBase):
    """
    chat api调用
    """
    def __init__(self, app_id):
        super().__init__(app_id)
        self.app_id = app_id
        self.module = 'qa'
        self.header = {
            "X-locale": "zh-cn",
            "app_id": app_id,
            "X-Appid": app_id,
            "user_id": "bf-engine-sdk",
            "X-Userid": "bf-engine-sdk",
            "Authorization": "Bearer EMOTIBOTDEBUGGER",
            "Accept": "application/json,text/plain, */*"
        }
        self.upload_chat_upload_url = Config.base_url + "/chat/chat_qa_api/dac/upload"
        self.upload_chat_upload_sync_url = Config.base_url+"/chat/chat_qa_api/dac/sync"

        self.upload_chat_custom_question_url    = Config.base_url + "/api/v1/customchat/import/question"
        self.upload_chat_custom_extend_url      = Config.base_url + "/api/v1/customchat/import/extend"

        self.download_chat_download_url = Config.base_url + "/chat/chat_qa_api/dac/download"
        self.download_chat_export_url = Config.base_url + "/chat/ssm/dac/common/minio/excelfile"
        self.open_chat_config_url = Config.base_url + "/api/v1/robot/config"


    """
    客制化闲聊
    """
    def upload_custom(self, chat_type: ChatType, file_path: str) -> str:
        """
        上传标注问/语料
        :param data_model: 上传模型 (全量|增量)
        :param file_path: 上传文件路径
        :return 上传id
        """
        # 上传问题$答案
        files = {"file": (self.app_id + ".xlsx", open(file_path, 'rb'))}
        request_url = self.upload_chat_custom_question_url
        if chat_type == ChatType.TQ:
            request_url = self.upload_chat_custom_extend_url
        resp = requests.request("POST", request_url, headers=self.header, data={}, files=files).json()

        # 问题$答案上传进度
        code = int(resp["status"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return str(resp["result"])
    """
    专属闲聊
    """
    def upload(self, data_model: ChatModel, file_path: str) -> str:
        """
        上传标注问/语料
        :param data_model: 上传模型 (全量|增量)
        :param file_path: 上传文件路径
        :return 上传id
        """
        # 上传问题$答案
        files = {"file": (self.app_id + ".xlsx", open(file_path, 'rb'))}
        data = { "type": data_model}
        resp = requests.request("POST", self.upload_chat_upload_url, headers=self.header, data=data, files=files).json()

        # 问题$答案上传进度
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return str(resp["data"])
    """
    专属闲聊发布
    """
    def publish(self):
        """
        开始发布
        :return 发布id
        """
        resp = requests.get(self.upload_chat_upload_sync_url, headers=self.header, json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return 100
    """
    打开机器人设置闲聊开关
    """
    def open(self,config:ChatConfig=None) -> bool:
        """
        打开闲聊
        """
        data = {
            "configName": config,
            "module": "controller",
            "value": "on"
        }
        resp = requests.put(self.open_chat_config_url, headers=self.header, data=data).json()
        code = int(resp["status"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return True

    def download_launch(self) -> str:
        """
        发起导出标注问/语料
        :param data_type: 下载类型 (SQ_ANS|LQ|TQ)
        :param file_path: 下载文件路径
        :return 服务器文件下载路径
        """
        resp = requests.get(self.download_chat_download_url, headers=self.header, json={}).json()
        code = int(resp["code"])
        msg = str(resp["message"])
        if code != 0:
            raise BfEngineException(code=code, msg=msg)
        return resp["data"]

    def download(self, file_path: str, service_file_path: str, is_log: bool = True):
        """
        从服务获取文件
        :param is_log: 是否打日志
        :param file_path: 本地文件保存路径
        :param service_file_path: 服务文件路径
        :return 上传进度
        """
        resp = requests.get(self.download_chat_export_url + "?filename=" + service_file_path, stream=True)
        with open(file_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=512):
                f.write(chunk)