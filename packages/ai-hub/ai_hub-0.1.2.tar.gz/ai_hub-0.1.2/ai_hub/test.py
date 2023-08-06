from inferServer import inferServer
#import ai_hub.globalvar as gl
import json
import ai_hub.log

class myserver(inferServer):
    def __init__(self,model):
        super().__init__(model)
        log.i("init_myserver")

    def pre_process(self, data):
        log.i("my_pre_process.")
        #json process
        json_data = json.loads(data.decode('utf-8'))
        img = json_data.get("img")
        log.i("data: ", img)
        return img

    #pridict default run as follow：
    # def predict(self, data):
    #     ret = self.model(data)
    #     return ret

    def post_process(self, data):
        return data



if __name__ == '__main__':
    mymodel = lambda x: x * 2
    myserver = myserver(mymodel)
    #run your server, defult ip=localhost port=8080 debuge=false
    myserver.run(debuge=True) #myserver.run("127.0.0.1", 1234)
