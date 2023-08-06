import time
import traceback
import os

from tqdm import tqdm

from .module import Module
from ..entity.enums import ChatModel
from ..entity.enums import ChatConfig
from ..entity.enums import ChatType
from ..logger import log
from ..entity.answer import Answer
from ..caller.chat_caller import ChatCaller
from ..entity.exception import BfEngineException, ErrorCode

class ChatService(Module):
    """
    问答
    """
    tmp_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    chat_empty_path = tmp_dir + "/data/闲聊上传模板.xlsx"
    def __init__(self, app_id, set, init):
        super().__init__(app_id, 'config', set)
        self.app_id = app_id
        self.caller = ChatCaller(app_id)
        if init:
            self.init()

    def query(self, text: str, online: bool = True) -> Answer:
        """
        :param online: 线上线下, 部分模块会需要线上线下的状态区分
        :param text: 用户问
        :return: 机器人回答
        """
        return self.caller.call_module('chat', text, online)

    def train(self,lq_path: str = None,tq_path: str = None):
        """
        :param chat_path: 闲聊路径
        :return: 训练是否成功
        """
        try:
            log.info('chat: prepare train')
            if lq_path:
                self.upload_custom_chat(chat_type=ChatType.LQ,chat_path=lq_path)
            if tq_path:
                self.upload_custom_chat(chat_type=ChatType.TQ,chat_path=tq_path)
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error('unknown exception')
            log.error(e)
            traceback.print_exc()
            return False
    def open(self,config: ChatConfig=None):
        if config:
            self.caller.open(config)
        else:
            for val in ChatConfig.list():
                self.caller.open(val)
        return True
    def publish(self):
        """
        :发布
        :return: 机器人回答
        """
        self._pulish()
    """
    客制化闲聊
    """
    def upload_custom_chat(self, chat_type: ChatType,chat_path):
        if not chat_path:
            raise BfEngineException(ErrorCode.argument_missing_error, 'missing chat path')
        data_id = self.caller.upload_custom(chat_type=chat_type,file_path=chat_path)
        return data_id;
    """
    专属闲聊
    """
    def upload_chat(self, chat_path, is_log=True, append: bool = False):
        if not chat_path:
            raise BfEngineException(ErrorCode.argument_missing_error, 'missing chat path')

        data_id = self.caller.upload(ChatModel.INCRE if append else ChatModel.FULL,
                                     chat_path)
        return data_id;
    def _upload_json(self, content):
        """
        获取从路径中json
        """
        try:
            data = content["data"]
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            return None

    def _pulish(self):
        log.info('chat: start release')
        progress = 0
        with tqdm(total=100) as bar:
            bar.set_description("chat release...")
            while progress < 100:
                old_progress = progress
                progress = self.caller.publish()
                bar.update(progress - old_progress)
                time.sleep(1)
            bar.set_description("chat release finished")
        time.sleep(5)

    def export(self,chat_path: str = None):
        """
        导出问答和语料文件
        :param sq_path 问答文件路径
        :param lq_path 语料文件路径
        """
        self._export(chat_path)

    def _export(self,chat_path: str = None):
        """
        导出问答和语料文件
        :param chat_path 问答文件路径
        :param lq_path 语料文件路径
        """
        try:
            if chat_path:
                data_path = self.caller.download_launch()
                self.caller.download(file_path=chat_path,service_file_path=data_path)
        except BfEngineException as bfe:
            log.error(bfe)
        except Exception as e:
            log.error(e)
    def _config(self,chat_config: ChatConfig =None):
        """
        打开机器人闲聊设置
        """
