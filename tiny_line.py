import usocket as socket
import ussl as ssl

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ---- percent encoding
def RFC3986_encode(s):
    ret = ''
    bts = s.encode('utf-8')
    for c in bts :
        if c in range(0x30, 0x39 + 1) or \
           c in range(0x41, 0x5a + 1) or \
           c in range(0x61, 0x7a + 1) or \
           c in (0x2d, 0x2e, 0x5f, 0x7e):
            ret += chr(c)
        else :
            ret += '%%%02X' % (c)
    return ret

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class tiny_line :
    def __init__(self, access_token, debug=False) :
        # パラメータチェック
        if type(access_token) is not str:
            raise ValueError("access key must be string")
        
        self.access_token      = access_token
        self.__DEBUG__         = debug

    def __debug_print(self, str) :
        if self.__DEBUG__ :
            print(str)
    
    def __makeRequestMessage(self, method, host, message) :
        method = method.upper()                                     # to upper
        
        # make request
        request = method + ' ' + host['endpoint'] + ' HTTP/1.0\n'   # HTTP/1.0 を指定するとChunked Transferにならないので、レスポンスが1行で済む
        
        # make message body
        body = 'message=' + RFC3986_encode(message)
        
        # make message header
        header  = 'Host: ' + host['host'] + '\n'                        \
                + 'User-Agent: micropython line Bot v0.1\n'             \
                + 'Accept: */*\n'                                       \
                + 'Authorization: Bearer ' + self.access_token +'\n'    \
                + 'Content-Type: application/x-www-form-urlencoded\n'   \
                + 'Content-Length: ' + str(len(body)) + '\n'
                # HTTP/1.0の場合は以下は要らない
                #+ 'Connection: close\n'                                 \

        # request message
        ret = request + header + '\n' + body + '\n'
        return(ret)
    
    def __sendmessage(self, host, msg) :
        sock = socket.socket()
        addr = socket.getaddrinfo(host['host'], host['port'])[0][-1]
        
        # connect socket
        sock.connect(addr)
        try :
            # SSL wrap
            ssl_sock = ssl.wrap_socket(sock)
            
            # send data
            ssl_sock.write(msg)
            
            # 受信データの最初の1行
            rcv_line = ssl_sock.readline()
            # print('rcv_line = ' + str(rcv_line))
            protover, status = rcv_line.split(None, 2)
            # status, msg = rcv_line.split(None, 2)
            # protover, status, msg = rcv_line.split(None, 2)
            # print('protover = ' + str(protover))
            # print('status = ' + str(status))
            # print('msg = ' + str(msg))
            # self.__debug_print('%s::::%s::::%s' % (protover, status, msg))
            # status 200以外はエラー
            if status != b"200":
                raise ValueError(status)
            # それ以外のレスポンスヘッダを読む
            while True:
                rcv_line = ssl_sock.readline()
                # self.__debug_print(rcv_line)
                if not rcv_line:
                    # なんらかの異常なレスポンス(ヘッダが終わる前にデータがなくなった)
                    raise ValueError("Unexpected EOF in HTTP headers")
                if rcv_line == b'\r\n':
                    # 空行でヘッダ終了
                    break
        except Exception as e:
            # エラーが発生したらクローズして上位へ例外通知
            ssl_sock.close()
            raise e
        # メッセージ本体を受信(とりあえず読み捨て)
        # 制限回数を超えた場合なんかはここでチェックが必要？
        rcv_line = b''
        while True :
            try :
                l = ssl_sock.readline()
            except Exception as e:              # エラーが発生したらクローズして上位へ例外通知
                ssl_sock.close()
                raise e
           
            if not l:                           # データがない → 終了
                break
            
            # 読み込んだデータをためる
            rcv_line += l
        
        # self.__debug_print("@@@@" + str(rcv_line))
        self.__debug_print("close!!")
        ssl_sock.close()
    
    # ######## notify API ################################
    def notify(self, msg) : 
        host = { 'host': 'notify-api.line.me', 'port': 443, 'endpoint': '/api/notify'}
        
        reqMessage = self.__makeRequestMessage('POST', host, msg)
        self.__debug_print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        self.__debug_print(reqMessage)
        self.__debug_print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        
        self.__sendmessage(host, reqMessage)