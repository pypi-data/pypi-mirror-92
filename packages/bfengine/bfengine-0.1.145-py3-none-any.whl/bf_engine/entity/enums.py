from enum import Enum

"""
问答管理
"""
class QuestionType:
    SQ_ANS = "SQ_ANS"
    LQ = "LQ"
    TQ = "TQ"
class QuestionField:
    SQ = "SQ"
    LQ = "lq"
    ALL = ""

"""
闲聊
"""
class ChatType:
    LQ = "question"
    TQ = "extend"
class ChatModel:
    FULL = "full"
    INCRE = "incre"
class QuestionMode:
    FULL = "full"
    INCRE = "incre"
class ChatConfig(Enum):
    #客制化闲聊
    CHAT_EDITORIAL_CUSTOM   = "chat-editorial-custom"
    #平台寒暄
    CHAT_DOMAIN_GREETING    = "chat-domain-greeting"
    #平台闲聊
    CHAT_EDITORIAL          = "chat-editorial"
    #平台形象
    CHAT_ROBOT              = "chat-robot"

    @staticmethod
    def list():
        return list(map(str,ChatConfig))